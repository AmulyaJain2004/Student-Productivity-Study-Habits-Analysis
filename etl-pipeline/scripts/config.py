"""
Configuration file for ETL Pipeline
===================================

This file manages database connections and configuration settings.
For production, use environment variables instead of hardcoded values.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ETLConfig:
    """Centralized configuration management for ETL pipeline."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.load_config()
    
    def load_config(self):
        """Load all configuration settings."""
        
        # Neon DB Configuration
        self.neon_config = {
            "host": os.getenv("NEON_HOST", ""),
            "database": os.getenv("NEON_DATABASE", ""),
            "username": os.getenv("NEON_USERNAME", ""),
            "password": os.getenv("NEON_PASSWORD", ""),
            "port": int(os.getenv("NEON_PORT", "5432")),
            "sslmode": os.getenv("NEON_SSLMODE", "require")
        }
        
        # Google Sheets Configuration
        self.google_sheets_config = {
            "spreadsheet_id": os.getenv("GOOGLE_SHEETS_ID", ""),
            "sheet_name": os.getenv("GOOGLE_SHEET_NAME", "Form Responses 1"),
            "credentials_file": os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json"),
            "scopes": ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        }
        
        # ETL Pipeline Settings
        self.etl_settings = {
            "batch_size": int(os.getenv("ETL_BATCH_SIZE", "100")),
            "table_name": os.getenv("ETL_TABLE_NAME", "student_survey_responses"),
            "max_retries": int(os.getenv("ETL_MAX_RETRIES", "3")),
            "retry_delay": int(os.getenv("ETL_RETRY_DELAY", "5"))
        }
        
        # ML Pipeline Settings
        self.ml_settings = {
            "model_version": os.getenv("ML_MODEL_VERSION", "v1.0"),
            "processing_batch_size": int(os.getenv("ML_BATCH_SIZE", "500")),
            "model_storage_path": os.getenv("ML_MODEL_PATH", "./models/"),
            "preprocessed_data_path": os.getenv("ML_DATA_PATH", "./data/processed/")
        }
    
    def get_neon_connection_string(self) -> str:
        """
        Get formatted Neon DB connection string.
        
        Returns:
            PostgreSQL connection string for Neon DB
        """
        from urllib.parse import quote_plus
        
        if not all([self.neon_config["host"], self.neon_config["database"], 
                   self.neon_config["username"], self.neon_config["password"]]):
            raise ValueError(
                "Missing required Neon DB credentials. "
                "Please set NEON_HOST, NEON_DATABASE, NEON_USERNAME, and NEON_PASSWORD environment variables."
            )
        
        encoded_password = quote_plus(self.neon_config["password"])
        return (
            f"postgresql://{self.neon_config['username']}:"
            f"{encoded_password}@{self.neon_config['host']}:"
            f"{self.neon_config['port']}/{self.neon_config['database']}"
            f"?sslmode={self.neon_config['sslmode']}"
        )
    
    def validate_config(self) -> Dict[str, Any]:
        """
        Validate configuration settings.
        
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "is_valid": True,
            "missing_configs": [],
            "warnings": []
        }
        
        # Check Neon DB config
        required_neon_vars = ["NEON_HOST", "NEON_DATABASE", "NEON_USERNAME", "NEON_PASSWORD"]
        for var in required_neon_vars:
            if not os.getenv(var):
                validation_results["is_valid"] = False
                validation_results["missing_configs"].append(var)
        
        # Check Google Sheets config
        if not os.getenv("GOOGLE_SHEETS_ID"):
            validation_results["warnings"].append("GOOGLE_SHEETS_ID not set - Google Sheets integration will not work")
        
        # Check credentials file
        credentials_file = self.google_sheets_config["credentials_file"]
        if not os.path.exists(credentials_file):
            validation_results["warnings"].append(f"Google credentials file not found: {credentials_file}")
        
        return validation_results
    
    def create_env_template(self, file_path: str = ".env.template") -> None:
        """
        Create a template .env file with all required variables.
        
        Args:
            file_path: Path to create the template file
        """
        template_content = """# Neon DB Configuration
NEON_HOST=your-host.neon.tech
NEON_DATABASE=your_database_name
NEON_USERNAME=your_username
NEON_PASSWORD=your_password
NEON_PORT=5432
NEON_SSLMODE=require

# Google Sheets Configuration
GOOGLE_SHEETS_ID=your_google_sheets_id
GOOGLE_SHEET_NAME=Form Responses 1
GOOGLE_CREDENTIALS_FILE=credentials.json

# ETL Pipeline Settings
ETL_BATCH_SIZE=100
ETL_TABLE_NAME=student_survey_responses
ETL_MAX_RETRIES=3
ETL_RETRY_DELAY=5

# ML Pipeline Settings
ML_MODEL_VERSION=v1.0
ML_BATCH_SIZE=500
ML_MODEL_PATH=./models/
ML_DATA_PATH=./data/processed/
"""
        
        with open(file_path, 'w') as f:
            f.write(template_content)
        
        print(f"✅ Environment template created: {file_path}")
        print("📝 Please copy to .env and fill in your actual values")


# Global configuration instance
config = ETLConfig()

def get_config() -> ETLConfig:
    """Get the global configuration instance."""
    return config

def validate_environment() -> bool:
    """
    Validate that all required environment variables are set.
    
    Returns:
        True if configuration is valid, False otherwise
    """
    validation = config.validate_config()
    
    if not validation["is_valid"]:
        print("❌ Configuration validation failed!")
        print(f"Missing required variables: {validation['missing_configs']}")
        print("\n🔧 To fix this:")
        print("1. Create a .env file in your project root")
        print("2. Add the missing environment variables")
        print("3. Or run: python config.py to create a template")
        return False
    
    if validation["warnings"]:
        print("⚠️ Configuration warnings:")
        for warning in validation["warnings"]:
            print(f"  - {warning}")
    
    print("✅ Configuration validation passed!")
    return True


if __name__ == "__main__":
    # Create environment template when run directly
    config.create_env_template()
    print("\n🔍 Current configuration status:")
    
    validation = config.validate_config()
    if validation["is_valid"]:
        print("✅ All required configurations are set")
    else:
        print("❌ Missing configurations:")
        for missing in validation["missing_configs"]:
            print(f"  - {missing}")
    
    if validation["warnings"]:
        print("⚠️ Warnings:")
        for warning in validation["warnings"]:
            print(f"  - {warning}")