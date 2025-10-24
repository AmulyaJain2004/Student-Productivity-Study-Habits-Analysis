# etl_pipeline/dags/student_etl_dag.py
from __future__ import annotations
from datetime import datetime, timedelta
import logging
import json
from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
from airflow.exceptions import AirflowFailException

# Import ETL classes from scripts folder
from pathlib import Path
import sys

# add scripts folder to import path
ROOT = Path(__file__).resolve().parents[1]  # etl_pipeline/
SCRIPTS_DIR = str(ROOT / "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from extract_data import GoogleSheetsExtractor
from transform_data import DataTransformer
from load_data import StudentSurveyDataLoader

DEFAULT_ARGS = {
    "owner": "amulya",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="student_habits_etl",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",  # configurable
    catchup=False,
    max_active_runs=1,
    tags=["etl", "student-habits"],
) as dag:

    @task()
    def extract_from_sheets() -> str:
        """
        Fetch raw sheet and return JSON-serialized dataframe (to pass via XCom).
        Uses Airflow Variable: GOOGLE_SHEETS_CREDENTIALS (JSON string) and SHEET_ID
        """
        try:
            creds_json = Variable.get("GOOGLE_SHEETS_CREDENTIALS")  # service account JSON (string)
            sheet_id = Variable.get("SHEET_ID")
        except KeyError as e:
            logging.error("Missing Airflow Variable: %s", e)
            raise AirflowFailException(f"Missing Airflow Variable: {e}")

        # Use GoogleSheetsExtractor class
        extractor = GoogleSheetsExtractor(creds_json, sheet_id)
        df = extractor.fetch_data()
        
        if df.empty:
            raise AirflowFailException("No data extracted from Google Sheets")
        
        # we store as JSON records string to XCom
        records_json = df.to_json(orient="records", date_format="iso")
        logging.info("Extracted %d rows from Google Sheet", len(df))
        return records_json

    @task()
    def transform_data(records_json: str) -> str:
        """
        Normalize schema and standardize categorical options.
        Input/Output are JSON records strings to keep XCom small and simple.
        """
        import pandas as pd
        df_raw = pd.read_json(records_json, orient="records")
        
        # Use DataTransformer class
        transformer = DataTransformer()
        df_clean = transformer.transform(df_raw)
        
        logging.info("Transformed to standardized schema with columns: %s", df_clean.columns.tolist())
        return df_clean.to_json(orient="records", date_format="iso")

    @task()
    def load_to_postgres(records_json: str) -> dict:
        """
        Upsert transformed rows into Postgres.
        Uses Airflow Variable: POSTGRES_DATABASE_URL  (SQLAlchemy URL)
        Uses StudentSurveyDataLoader class for comprehensive loading.
        Returns dictionary with counts for logging.
        """
        import pandas as pd
        try:
            database_url = Variable.get("POSTGRES_DATABASE_URL")
        except KeyError:
            raise AirflowFailException("Missing Airflow Variable: POSTGRES_DATABASE_URL")

        df = pd.read_json(records_json, orient="records")
        
        # Use StudentSurveyDataLoader class
        loader = StudentSurveyDataLoader(database_url, table_name="student_survey_responses")
        
        try:
            result = loader.load_data(df, create_table=True, batch_size=100)
            logging.info("Load result: %s", result)
            
            # Return simplified result for XCom
            return {
                "status": result["status"],
                "inserted": result["upsert"]["inserted"],
                "updated": result["upsert"]["updated"],
                "total_records": result["table_stats"]["total_records"]
            }
        finally:
            loader.close_connection()

    # DAG task ordering
    raw = extract_from_sheets()
    transformed = transform_data(raw)
    loaded = load_to_postgres(transformed)
