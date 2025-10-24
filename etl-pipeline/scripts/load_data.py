"""
Data Loading Module for Student Survey ETL Pipeline
==================================================

This module provides a comprehensive class-based solution for loading transformed 
survey data into PostgreSQL database (specifically designed for Neon DB).

Key Features:
- Complete class-based architecture
- Dynamic schema creation based on transformed data
- Upsert operations with conflict resolution
- Comprehensive data validation and error handling
- Database connection management
- Batch processing capabilities
- Detailed logging and metrics

Author: Survey Analysis Team
Version: 4.0
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text, MetaData, Table, Column, String, Integer, Float, DateTime, Boolean, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import os
from urllib.parse import quote_plus
import psycopg2
from contextlib import contextmanager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StudentSurveyDataLoader:
    """
    Comprehensive data loader for student survey responses.
    
    This class handles the complete data loading pipeline from transformed
    DataFrames to PostgreSQL database with proper schema management,
    validation, and error handling.
    """
    
    def __init__(self, database_url: str, table_name: str = "student_survey_responses"):
        """
        Initialize the data loader.
        
        Args:
            database_url: PostgreSQL connection string (Neon DB format)
            table_name: Target table name for survey responses
        """
        self.database_url = database_url
        self.table_name = table_name
        self.engine: Optional[Engine] = None
        self.metadata = MetaData()
        
        # Expected schema from transform_data.py
        self.expected_columns = [
            "response_id", "timestamp", "year_of_study", "school",
            "study_hours_daily", "study_schedule_type", "study_environment", 
            "focus_level", "gpa", "sleep_hours_nightly", "sleep_quality", 
            "sleep_productivity_rating", "sleep_disruptions", "stress_level", 
            "stress_factors", "academic_overwhelm_frequency", "stress_relief_activity",
            "social_media_hours_daily", "social_media_academic_impact", 
            "primary_social_platforms", "extracurricular_type", 
            "extracurricular_hours_weekly", "extracurricular_wellbeing_impact",
            "career_preparedness", "career_experience", "job_confidence", 
            "career_motivation_level", "ingested_at"
        ]
        
        # Column type mappings
        self.column_types = {
            "response_id": String(64),
            "timestamp": DateTime,
            "year_of_study": String(10),
            "school": String(50),
            "study_hours_daily": String(50),
            "study_schedule_type": String(50),
            "study_environment": String(50),
            "focus_level": Integer,
            "gpa": Float,
            "sleep_hours_nightly": String(50),
            "sleep_quality": String(50),
            "sleep_productivity_rating": Integer,
            "sleep_disruptions": String(50),
            "stress_level": Integer,
            "stress_factors": String(500),  # Multi-select field
            "academic_overwhelm_frequency": String(50),
            "stress_relief_activity": String(100),
            "social_media_hours_daily": String(50),
            "social_media_academic_impact": String(50),
            "primary_social_platforms": String(500),  # Multi-select field
            "extracurricular_type": String(50),
            "extracurricular_hours_weekly": String(50),
            "extracurricular_wellbeing_impact": String(50),
            "career_preparedness": String(50),
            "career_experience": String(10),
            "job_confidence": Integer,
            "career_motivation_level": Integer,
            "ingested_at": DateTime
        }
        
        self._initialize_connection()
    
    def _initialize_connection(self) -> None:
        """Initialize database connection and validate connectivity."""
        try:
            logger.info("Initializing database connection...")
            self.engine = create_engine(
                self.database_url,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False  # Set to True for SQL debugging
            )
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info("✅ Database connection established successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize database connection: {str(e)}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        if not self.engine:
            raise RuntimeError("Database engine not initialized")
        
        connection = self.engine.connect()
        try:
            yield connection
        finally:
            connection.close()
    
    def create_table_schema(self) -> None:
        """
        Create the survey responses table with proper schema.
        
        This method creates a comprehensive table schema that matches
        the output from the DataTransformer class.
        """
        logger.info(f"Creating table schema for '{self.table_name}'...")
        
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id SERIAL PRIMARY KEY,
            response_id VARCHAR(64) UNIQUE NOT NULL,
            timestamp TIMESTAMP WITH TIME ZONE,
            year_of_study VARCHAR(10),
            school VARCHAR(50),
            study_hours_daily VARCHAR(50),
            study_schedule_type VARCHAR(50),
            study_environment VARCHAR(50),
            focus_level INTEGER,
            gpa DECIMAL(4,2),
            sleep_hours_nightly VARCHAR(50),
            sleep_quality VARCHAR(50),
            sleep_productivity_rating INTEGER,
            sleep_disruptions VARCHAR(50),
            stress_level INTEGER,
            stress_factors TEXT,
            academic_overwhelm_frequency VARCHAR(50),
            stress_relief_activity VARCHAR(100),
            social_media_hours_daily VARCHAR(50),
            social_media_academic_impact VARCHAR(50),
            primary_social_platforms TEXT,
            extracurricular_type VARCHAR(50),
            extracurricular_hours_weekly VARCHAR(50),
            extracurricular_wellbeing_impact VARCHAR(50),
            career_preparedness VARCHAR(50),
            career_experience VARCHAR(10),
            job_confidence INTEGER,
            career_motivation_level INTEGER,
            ingested_at TIMESTAMP WITH TIME ZONE,
            processed BOOLEAN DEFAULT FALSE,
            ml_processed_at TIMESTAMP WITH TIME ZONE,
            model_version VARCHAR(50),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create indexes for better query performance
        CREATE INDEX IF NOT EXISTS idx_{self.table_name}_response_id ON {self.table_name}(response_id);
        CREATE INDEX IF NOT EXISTS idx_{self.table_name}_timestamp ON {self.table_name}(timestamp);
        CREATE INDEX IF NOT EXISTS idx_{self.table_name}_school ON {self.table_name}(school);
        CREATE INDEX IF NOT EXISTS idx_{self.table_name}_year_study ON {self.table_name}(year_of_study);
        CREATE INDEX IF NOT EXISTS idx_{self.table_name}_ingested_at ON {self.table_name}(ingested_at);
        CREATE INDEX IF NOT EXISTS idx_{self.table_name}_processed ON {self.table_name}(processed);
        CREATE INDEX IF NOT EXISTS idx_{self.table_name}_ml_processed_at ON {self.table_name}(ml_processed_at);
        
        -- Create trigger for updated_at
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        
        DROP TRIGGER IF EXISTS update_{self.table_name}_updated_at ON {self.table_name};
        CREATE TRIGGER update_{self.table_name}_updated_at
            BEFORE UPDATE ON {self.table_name}
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
        """
        
        try:
            with self.get_connection() as conn:
                conn.execute(text(create_table_sql))
                conn.commit()
            
            logger.info(f"✅ Table '{self.table_name}' schema created successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to create table schema: {str(e)}")
            raise
    
    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Comprehensive validation of the input DataFrame.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary with detailed validation results
        """
        logger.info("Validating input DataFrame...")
        
        validation_results = {
            "is_valid": True,
            "total_rows": len(df),
            "issues": [],
            "warnings": [],
            "column_analysis": {}
        }
        
        # Check for response_id column (critical)
        if 'response_id' not in df.columns:
            validation_results["is_valid"] = False
            validation_results["issues"].append(
                "Missing 'response_id' column - ensure transform step completed"
            )
        else:
            # Analyze response_id column
            null_count = df['response_id'].isna().sum()
            duplicate_count = df['response_id'].duplicated().sum()
            
            if null_count > 0:
                validation_results["is_valid"] = False
                validation_results["issues"].append(f"Found {null_count} null response_id values")
            
            if duplicate_count > 0:
                validation_results["warnings"].append(f"Found {duplicate_count} duplicate response_ids")
            
            validation_results["column_analysis"]["response_id"] = {
                "null_count": null_count,
                "duplicate_count": duplicate_count,
                "unique_count": df['response_id'].nunique()
            }
        
        # Check for ingested_at column
        if 'ingested_at' not in df.columns:
            validation_results["warnings"].append(
                "Missing 'ingested_at' column - will be auto-generated"
            )
        
        # Analyze expected columns
        missing_columns = set(self.expected_columns) - set(df.columns)
        extra_columns = set(df.columns) - set(self.expected_columns)
        
        if missing_columns:
            validation_results["warnings"].append(
                f"Missing expected columns: {list(missing_columns)}"
            )
        
        if extra_columns:
            validation_results["warnings"].append(
                f"Extra columns found: {list(extra_columns)}"
            )
        
        # Analyze data quality for key columns
        for col in ["gpa", "focus_level", "stress_level", "job_confidence", "career_motivation_level"]:
            if col in df.columns:
                validation_results["column_analysis"][col] = {
                    "null_count": df[col].isna().sum(),
                    "min_value": df[col].min() if df[col].notna().any() else None,
                    "max_value": df[col].max() if df[col].notna().any() else None,
                    "data_type": str(df[col].dtype)
                }
        
        logger.info(f"Validation completed: {'✅ PASSED' if validation_results['is_valid'] else '❌ FAILED'}")
        
        return validation_results
    
    def prepare_dataframe_for_loading(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare DataFrame for database loading.
        
        Args:
            df: Raw transformed DataFrame
            
        Returns:
            DataFrame ready for database insertion
        """
        logger.info("Preparing DataFrame for database loading...")
        
        df_prepared = df.copy()
        
        # Ensure ingested_at is present
        if 'ingested_at' not in df_prepared.columns:
            df_prepared['ingested_at'] = pd.Timestamp.now(tz='UTC')
        
        # Handle missing expected columns
        for col in self.expected_columns:
            if col not in df_prepared.columns:
                df_prepared[col] = None
                logger.warning(f"Added missing column '{col}' with None values")
        
        # Clean and format data
        for col in df_prepared.columns:
            if col in ["gpa", "focus_level", "stress_level", "job_confidence", "career_motivation_level"]:
                # Ensure numeric columns are properly typed
                df_prepared[col] = pd.to_numeric(df_prepared[col], errors='coerce')
            
            elif col in ["timestamp", "ingested_at"]:
                # Ensure datetime columns are properly formatted
                df_prepared[col] = pd.to_datetime(df_prepared[col], errors='coerce')
            
            elif df_prepared[col].dtype == 'object':
                # Clean string columns
                df_prepared[col] = df_prepared[col].astype(str).replace('nan', None)
        
        # Select only the columns we need for the database
        final_columns = [col for col in self.expected_columns if col in df_prepared.columns]
        df_final = df_prepared[final_columns]
        
        logger.info(f"DataFrame prepared: {len(df_final)} rows, {len(df_final.columns)} columns")
        
        return df_final
    
    def upsert_data(self, df: pd.DataFrame, batch_size: int = 100) -> Dict[str, int]:
        """
        Upsert data into the database with batch processing.
        
        Args:
            df: Prepared DataFrame for insertion
            batch_size: Number of rows to process in each batch
            
        Returns:
            Dictionary with insert/update statistics
        """
        if df.empty:
            logger.warning("Empty DataFrame provided for upsert")
            return {"inserted": 0, "updated": 0, "total": 0, "errors": 0}
        
        logger.info(f"Starting upsert operation for {len(df)} records...")
        
        inserted = 0
        updated = 0
        errors = 0
        
        # Prepare column lists for SQL
        columns = [col for col in self.expected_columns if col in df.columns]
        column_placeholders = ", ".join([f":{col}" for col in columns])
        column_names = ", ".join(columns)
        
        # Build update clause for ON CONFLICT
        update_clauses = ", ".join([
            f"{col} = EXCLUDED.{col}" for col in columns if col != 'response_id'
        ])
        
        upsert_sql = text(f"""
            INSERT INTO {self.table_name} (
                {column_names}, created_at, updated_at
            )
            VALUES (
                {column_placeholders}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
            )
            ON CONFLICT (response_id)
            DO UPDATE SET
                {update_clauses},
                updated_at = CURRENT_TIMESTAMP
            RETURNING (xmax = 0) AS is_insert;
        """)
        
        try:
            with self.get_connection() as conn:
                # Process in batches
                for i in range(0, len(df), batch_size):
                    batch_df = df.iloc[i:i + batch_size]
                    logger.info(f"Processing batch {i//batch_size + 1}: rows {i+1}-{min(i+batch_size, len(df))}")
                    
                    for _, row in batch_df.iterrows():
                        try:
                            # Convert row to dict and handle NaN values
                            row_dict = {}
                            for col in columns:
                                value = row[col]
                                if pd.isna(value):
                                    row_dict[col] = None
                                else:
                                    row_dict[col] = value
                            
                            result = conn.execute(upsert_sql, **row_dict)
                            is_insert = result.fetchone()[0]
                            
                            if is_insert:
                                inserted += 1
                            else:
                                updated += 1
                                
                        except Exception as e:
                            errors += 1
                            logger.error(f"Error processing row {row.get('response_id', 'unknown')}: {str(e)}")
                            continue
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Batch upsert operation failed: {str(e)}")
            raise
        
        result = {
            "inserted": inserted,
            "updated": updated,
            "total": len(df),
            "errors": errors
        }
        
        logger.info(f"Upsert completed: {result}")
        return result
    
    def get_table_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the loaded data.
        
        Returns:
            Dictionary with table statistics
        """
        logger.info("Gathering table statistics...")
        
        stats_sql = text(f"""
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT response_id) as unique_responses,
                COUNT(DISTINCT school) as unique_schools,
                MIN(timestamp) as earliest_response,
                MAX(timestamp) as latest_response,
                MIN(ingested_at) as first_ingested,
                MAX(ingested_at) as last_ingested,
                AVG(gpa) as avg_gpa,
                AVG(stress_level) as avg_stress_level,
                AVG(focus_level) as avg_focus_level
            FROM {self.table_name}
        """)
        
        try:
            with self.get_connection() as conn:
                result = conn.execute(stats_sql).fetchone()
                
                stats = {
                    "total_records": result[0],
                    "unique_responses": result[1],
                    "unique_schools": result[2],
                    "earliest_response": result[3],
                    "latest_response": result[4],
                    "first_ingested": result[5],
                    "last_ingested": result[6],
                    "avg_gpa": float(result[7]) if result[7] else None,
                    "avg_stress_level": float(result[8]) if result[8] else None,
                    "avg_focus_level": float(result[9]) if result[9] else None
                }
                
                logger.info("Table statistics gathered successfully")
                return stats
                
        except Exception as e:
            logger.error(f"Failed to gather table statistics: {str(e)}")
            raise
    
    def load_data(self, df: pd.DataFrame, create_table: bool = True, batch_size: int = 100) -> Dict[str, Any]:
        """
        Main method to load transformed data into the database.
        
        Args:
            df: Transformed DataFrame from DataTransformer
            create_table: Whether to create/update table schema
            batch_size: Number of rows to process in each batch
            
        Returns:
            Dictionary with comprehensive loading results
        """
        logger.info("🚀 Starting data loading process...")
        
        try:
            # Step 1: Create table schema if needed
            if create_table:
                self.create_table_schema()
            
            # Step 2: Validate input data
            validation_results = self.validate_dataframe(df)
            if not validation_results["is_valid"]:
                raise ValueError(f"Data validation failed: {validation_results['issues']}")
            
            # Step 3: Prepare data for loading
            df_prepared = self.prepare_dataframe_for_loading(df)
            
            # Step 4: Upsert data
            upsert_results = self.upsert_data(df_prepared, batch_size=batch_size)
            
            # Step 5: Get final statistics
            table_stats = self.get_table_stats()
            
            # Compile results
            loading_results = {
                "status": "success",
                "validation": validation_results,
                "upsert": upsert_results,
                "table_stats": table_stats,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ Data loading completed successfully!")
            return loading_results
            
        except Exception as e:
            logger.error(f"❌ Data loading failed: {str(e)}")
            error_results = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            raise Exception(f"Data loading failed: {str(e)}") from e
    
    def get_unprocessed_data(self, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Retrieve unprocessed records for ML pipeline.
        
        Args:
            limit: Maximum number of records to fetch (None for all)
            
        Returns:
            DataFrame with unprocessed records
        """
        logger.info("Fetching unprocessed records for ML processing...")
        
        limit_clause = f"LIMIT {limit}" if limit else ""
        
        query_sql = text(f"""
            SELECT * FROM {self.table_name}
            WHERE processed = FALSE
            ORDER BY created_at ASC
            {limit_clause}
        """)
        
        try:
            with self.get_connection() as conn:
                df = pd.read_sql(query_sql, conn)
                logger.info(f"Retrieved {len(df)} unprocessed records")
                return df
                
        except Exception as e:
            logger.error(f"Failed to fetch unprocessed data: {str(e)}")
            raise
    
    def mark_as_processed(self, response_ids: List[str], model_version: str = None) -> int:
        """
        Mark records as processed after ML pipeline completion.
        
        Args:
            response_ids: List of response IDs to mark as processed
            model_version: Version of the model used for processing
            
        Returns:
            Number of records updated
        """
        if not response_ids:
            logger.warning("No response IDs provided for marking as processed")
            return 0
        
        logger.info(f"Marking {len(response_ids)} records as processed...")
        
        # Create placeholders for parameterized query
        placeholders = ",".join([f":id_{i}" for i in range(len(response_ids))])
        
        update_sql = text(f"""
            UPDATE {self.table_name}
            SET processed = TRUE,
                ml_processed_at = CURRENT_TIMESTAMP,
                model_version = :model_version,
                updated_at = CURRENT_TIMESTAMP
            WHERE response_id IN ({placeholders})
        """)
        
        # Create parameter dictionary
        params = {f"id_{i}": response_id for i, response_id in enumerate(response_ids)}
        params["model_version"] = model_version
        
        try:
            with self.get_connection() as conn:
                result = conn.execute(update_sql, **params)
                rows_updated = result.rowcount
                conn.commit()
                
                logger.info(f"Successfully marked {rows_updated} records as processed")
                return rows_updated
                
        except Exception as e:
            logger.error(f"Failed to mark records as processed: {str(e)}")
            raise
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """
        Get statistics about processed vs unprocessed records.
        
        Returns:
            Dictionary with processing statistics
        """
        logger.info("Gathering processing statistics...")
        
        stats_sql = text(f"""
            SELECT 
                COUNT(*) as total_records,
                COUNT(CASE WHEN processed = TRUE THEN 1 END) as processed_records,
                COUNT(CASE WHEN processed = FALSE THEN 1 END) as unprocessed_records,
                MIN(CASE WHEN processed = TRUE THEN ml_processed_at END) as first_processed_at,
                MAX(CASE WHEN processed = TRUE THEN ml_processed_at END) as last_processed_at,
                COUNT(DISTINCT model_version) as unique_model_versions,
                MAX(model_version) as latest_model_version
            FROM {self.table_name}
        """)
        
        try:
            with self.get_connection() as conn:
                result = conn.execute(stats_sql).fetchone()
                
                stats = {
                    "total_records": result[0],
                    "processed_records": result[1],
                    "unprocessed_records": result[2],
                    "processing_rate": (result[1] / result[0] * 100) if result[0] > 0 else 0,
                    "first_processed_at": result[3],
                    "last_processed_at": result[4],
                    "unique_model_versions": result[5],
                    "latest_model_version": result[6]
                }
                
                logger.info(f"Processing stats: {stats['processed_records']}/{stats['total_records']} processed ({stats['processing_rate']:.1f}%)")
                return stats
                
        except Exception as e:
            logger.error(f"Failed to gather processing statistics: {str(e)}")
            raise
    
    def reset_processing_status(self, response_ids: List[str] = None) -> int:
        """
        Reset processing status for records (useful for reprocessing).
        
        Args:
            response_ids: Specific response IDs to reset (None for all)
            
        Returns:
            Number of records reset
        """
        if response_ids:
            placeholders = ",".join([f":id_{i}" for i in range(len(response_ids))])
            where_clause = f"WHERE response_id IN ({placeholders})"
            params = {f"id_{i}": response_id for i, response_id in enumerate(response_ids)}
            logger.info(f"Resetting processing status for {len(response_ids)} specific records...")
        else:
            where_clause = ""
            params = {}
            logger.warning("Resetting processing status for ALL records...")
        
        reset_sql = text(f"""
            UPDATE {self.table_name}
            SET processed = FALSE,
                ml_processed_at = NULL,
                model_version = NULL,
                updated_at = CURRENT_TIMESTAMP
            {where_clause}
        """)
        
        try:
            with self.get_connection() as conn:
                result = conn.execute(reset_sql, **params)
                rows_updated = result.rowcount
                conn.commit()
                
                logger.info(f"Reset processing status for {rows_updated} records")
                return rows_updated
                
        except Exception as e:
            logger.error(f"Failed to reset processing status: {str(e)}")
            raise
    
    def close_connection(self):
        """Clean up database connections."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")


def create_neon_connection_string(
    host: str,
    database: str,
    username: str,
    password: str,
    port: int = 5432,
    sslmode: str = "require"
) -> str:
    """
    Create a properly formatted Neon DB connection string.
    
    Args:
        host: Neon database host
        database: Database name
        username: Database username
        password: Database password
        port: Database port (default: 5432)
        sslmode: SSL mode (default: require)
        
    Returns:
        Formatted connection string
    """
    encoded_password = quote_plus(password)
    return f"postgresql://{username}:{encoded_password}@{host}:{port}/{database}?sslmode={sslmode}"


def load_survey_data_to_neon(
    df: pd.DataFrame,
    neon_config: Dict[str, str],
    table_name: str = "student_survey_responses"
) -> Dict[str, Any]:
    """
    Convenience function to load survey data to Neon DB.
    
    Args:
        df: Transformed DataFrame from DataTransformer
        neon_config: Dictionary with Neon DB configuration
        table_name: Target table name
        
    Returns:
        Loading results dictionary
    """
    # Create connection string
    connection_string = create_neon_connection_string(**neon_config)
    
    # Initialize loader and load data
    loader = StudentSurveyDataLoader(connection_string, table_name)
    
    try:
        results = loader.load_data(df)
        return results
    finally:
        loader.close_connection()


# Example usage
if __name__ == "__main__":
    # Example configuration for Neon DB
    neon_config = {
        "host": "your-neon-host.neon.tech",
        "database": "your_database_name",
        "username": "your_username",
        "password": "your_password"
    }
    
    # Example usage with transformed data
    from transform_data import DataTransformer
    
    # Load and transform data
    csv_path = "path/to/your/survey_data.csv"
    df = pd.read_csv(csv_path)
    
    transformer = DataTransformer()
    transformed_df = transformer.transform(df)
    
    # Load to Neon DB
    results = load_survey_data_to_neon(transformed_df, neon_config)
    
    print("Loading Results:")
    print(f"Status: {results['status']}")
    print(f"Inserted: {results['upsert']['inserted']}")
    print(f"Updated: {results['upsert']['updated']}")
    print(f"Total records in table: {results['table_stats']['total_records']}")
