"""
This module provides a comprehensive ETL transformation layer for survey data,
specifically designed for Google Forms responses. 
It handles data cleaning, normalization, categorical mapping, and schema enforcement.

does: 
- Flexible column mapping configuration
- Multi-select field handling
- Unicode normalization and text cleaning
- Categorical value standardization
- Data type casting and validation
- Deduplication and schema enforcement
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import hashlib
import unicodedata
import re
from abc import ABC, abstractmethod


class FieldProcessor(ABC):
    """Abstract base class for field-specific processing strategies."""
    
    @abstractmethod
    def process(self, value: Any) -> Any:
        """Process a single field value."""
        pass


class TextFieldProcessor(FieldProcessor):
    """Processes text fields with normalization and cleaning."""
    
    def process(self, value: Any) -> Any:
        if pd.isna(value):
            return pd.NA
        
        # Normalize and clean text
        text = str(value).strip()
        text = unicodedata.normalize("NFKC", text) # Unicode normalization
        
        # Handle empty strings and null equivalents
        if text.lower() in ['', 'nan', 'null', 'none', 'n/a', 'na']:
            return pd.NA
            
        return text


class NumericFieldProcessor(FieldProcessor):
    """Processes numeric fields with range validation."""
    
    def __init__(self, min_val: Optional[float] = None, max_val: Optional[float] = None):
        self.min_val = min_val
        self.max_val = max_val
    
    def process(self, value: Any) -> Any:
        if pd.isna(value):
            return pd.NA
            
        # Extract numeric value from text (handles "8/10", "8 out of 10", etc.)
        if isinstance(value, str):
            match = re.search(r'(\d+\.?\d*)', value.strip())
            if match:
                value = float(match.group(1))
            else:
                return pd.NA
        
        try:
            numeric_val = float(value)
            
            # Validate range if specified
            if self.min_val is not None and numeric_val < self.min_val:
                return pd.NA
            if self.max_val is not None and numeric_val > self.max_val:
                return pd.NA
                
            return int(numeric_val) if numeric_val.is_integer() else numeric_val
            
        except (ValueError, TypeError):
            return pd.NA


class CategoricalFieldProcessor(FieldProcessor):
    """Processes categorical fields with mapping and multi-select support."""
    
    def __init__(self, mapping: Dict[str, str], is_multi_select: bool = False):
        # Apply Unicode normalization to mapping keys for better matching
        self.mapping = {}
        for k, v in mapping.items():
            normalized_key = unicodedata.normalize("NFKC", k.lower().strip())
            self.mapping[normalized_key] = v
        self.is_multi_select = is_multi_select
    
    def process(self, value: Any) -> Any:
        if pd.isna(value):
            return pd.NA
            
        text = str(value).strip()
        text = unicodedata.normalize("NFKC", text)
        
        if self.is_multi_select:
            return self.process_multi_select(text)
        else:
            return self.process_single_select(text)

    def process_single_select(self, text: str) -> str:
        """Process single-select categorical value."""
        key = unicodedata.normalize("NFKC", text.lower().strip())
        return self.mapping.get(key, text)  # Return original if not mapped
    
    def process_multi_select(self, text: str) -> str:
        """Process comma-separated multi-select values."""
        parts = [p.strip() for p in text.split(",") if p.strip()]
        mapped_parts = []
        
        for part in parts:
            key = unicodedata.normalize("NFKC", part.lower().strip())
            mapped_value = self.mapping.get(key, part)
            mapped_parts.append(mapped_value)
            
        return ", ".join(mapped_parts)


class GPAFieldProcessor(FieldProcessor):
    """Specialized processor for GPA values on 10-point scale."""
    
    def process(self, value: Any) -> Any:
        if pd.isna(value):
            return pd.NA
            
        text = str(value).lower().strip()
        
        # Handle explicit NA values
        if text in ['na', 'n/a', 'not known', 'unknown', 'null', 'none', '']:
            return pd.NA
        
        # Extract numeric GPA value
        match = re.search(r'(\d+\.?\d*)', text)
        if match:
            gpa_val = float(match.group(1))
                
            # Validate GPA range (only 0-10 inclusive on 10-point scale)
            if 0 <= gpa_val <= 10.0:
                return round(gpa_val, 2)
            else:
                return pd.NA
            
        return pd.NA


class DataTransformer:
    """
    Main transformer class for survey data processing.
    
    This class orchestrates the transformation of raw survey responses into
    a clean, standardized format suitable for analysis and ML pipelines.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the transformer with configuration.
        
        Args:
            config: Optional configuration dictionary for custom mappings
        """
        self.config = config or {}
        self.setup_field_mappings()
        self.setup_processors()
    
    def setup_field_mappings(self):
        """Configure field mappings and schema definitions."""
        
        # Column name mappings from survey questions to clean field names
        self.column_mappings = {
            "Timestamp": "timestamp",
            "1. What is your year of study?": "year_of_study",
            "2. Which School you belong to?": "school",
            "3. On average, how many hours do you spend studying per day?": "study_hours_daily",
            "4. How do you typically organize your study schedule?": "study_schedule_type",
            "5. What is your typical study environment like?": "study_environment",
            "6. On a scale of 1 to 10, how focused do you feel during study sessions?": "focus_level",
            "7. What is your current GPA if known? (Write NA if not known)": "gpa",
            "8. On average, how many hours do you sleep per night?": "sleep_hours_nightly",
            "9. How do you feel about your sleep quality?": "sleep_quality",
            "10. How productive do you feel on average after a full night of sleep (1-10 scale)?": "sleep_productivity_rating",
            "11. Do you often experience disruptions in your sleep (e.g., waking up during the night)?": "sleep_disruptions",
            "12. On a scale of 1 to 10, how would you rate your general stress level?": "stress_level",
            "13. What are the main factors contributing to your stress?": "stress_factors",
            "14. How often do you feel overwhelmed by academic responsibilities (e.g., assignments, exams)?": "academic_overwhelm_frequency",
            "15. What activity do you most often turn to when you're feeling stressed or need to unwind?": "stress_relief_activity",
            "16. On average, how many hours do you spend on social media per day?": "social_media_hours_daily",
            "17. Do you feel that social media affects your academic performance?": "social_media_academic_impact",
            "18. Which social media platforms do you use most frequently?": "primary_social_platforms",
            "19. Which of the following extracurricular areas do you primarily participate in?": "extracurricular_type",
            "20. How many hours per week do you spend on extracurricular activities?": "extracurricular_hours_weekly",
            "21. How does participating in extracurricular activities affect your overall academic and personal well-being?": "extracurricular_wellbeing_impact",
            "22. Do you feel prepared for your future career based on your current academic and extracurricular experience?": "career_preparedness",
            "23. Have you participated in any internships, co-op programs, or career development activities?": "career_experience",
            "24. How confident are you in finding a job after graduation?": "job_confidence",
            "25. On a scale of 1–10, how motivated do you currently feel toward your academics and career goals?": "career_motivation_level",
        }
        
        # Categorical value mappings
        self.categorical_mappings = {
            "year_of_study": {str(i): str(i) for i in range(1, 6)},
            "school": {k: k for k in ["SOCS", "SOAE", "SOB", "SOL", "SOD", "SOHST", "SOLS"]},
            "study_hours_daily": {
                "1-2 hours": "1_2_hours", "3-4 hours": "3_4_hours", 
                "5-6 hours": "5_6_hours", "More than 6 hours": "more_than_6_hours"
            },
            "study_schedule_type": {
                "Daily study routine": "daily",
                "Weekdays only (Monday - Friday)": "weekdays_only",
                "Weekends only (Saturday - Sunday)": "weekends_only",
                "Sporadic, depending on assignments/tests": "sporadic",
            },
            "study_environment": {
                "Quiet (Library, study room alone, etc.)": "quiet",
                "Noisy or Distracting (Café, shared hostel, etc.)": "noisy",
                "I don't have a dedicated study space": "no_dedicated_space",  # ASCII apostrophe
                "I don\u2019t have a dedicated study space": "no_dedicated_space",  # Unicode apostrophe
                "In Groups": "group_study",
            },
            "sleep_hours_nightly": {
                "Less than 4 hours": "<4_hours", "4-5 hours": "4_5_hours", 
                "6-7 hours": "6_7_hours", "8 or more hours": "8+_hours"
            },
            "sleep_quality": {"Poor": "poor", "Fair": "fair", "Good": "good", "Excellent": "excellent"},
            "sleep_disruptions": {"Yes, always": "always", "Sometimes": "sometimes", "Never": "never"},
            "stress_factors": {
                "Academic pressure": "academics", "Financial concerns": "finance",
                "Personal/Family issues": "personal", "Time management": "time_management", "Other": "other"    
            },
            "academic_overwhelm_frequency": {
                "Always": "always", "Often": "often", "Sometimes": "sometimes", 
                "Rarely": "rarely", "Never": "never"
            },
            "stress_relief_activity": {
                "Watching movies, web series or YouTube": "movies_youtube",
                "Instagram, Reels or other social media": "social_media",
                "Listening to music or podcasts": "music_podcasts",
                "Playing online games or outdoor sports": "games_sports",
                "Talking or hanging out with friends/family": "talking_friends",
                "Exercising, yoga or going for a walk": "exercise_yoga",
                "Reading or journaling": "reading",
                "Shopping": "shopping",
                "Meditating or deep breathing": "meditation",
                "Sleeping or taking naps": "sleeping",
                "I usually don't do anything specific": "none",  # ASCII apostrophe
                "I usually don\u2019t do anything specific": "none",  # Unicode apostrophe
                "Other": "other"
            },
            "social_media_hours_daily": {
                "Less than 1 hour": "<1_hour", "1-2 hours": "1_2_hours", 
                "3-4 hours": "3_4_hours", "More than 4 hours": "4+_hours"
            },
            "social_media_academic_impact": {
                "Positively (It improves my academic performance)": "positive",
                "Negatively (It degrades my academic performance)": "negative",
                "No, it doesn't affect my academic performance": "no_effect",  # ASCII apostrophe
                "No, it doesn\u2019t affect my academic performance": "no_effect",  # Unicode apostrophe
                "Maybe": "maybe",
            },
            "primary_social_platforms": {
                "Facebook": "facebook", "Instagram": "instagram", "X (Twitter)": "twitter",
                "Snapchat": "snapchat", "Reddit": "reddit", "Whatsapp": "whatsapp", 
                "Telegram": "telegram", "YouTube": "youtube", "Discord": "discord", "LinkedIn": "linkedin", "Other": "other"
            },
            "extracurricular_type": {
                "Indoor Sports": "indoor_sports", "Outdoor Sports": "outdoor_sports",
                "Music": "music", "Dancing/ Drama": "dance_drama", "Art": "art", "Other": "other"
            },
            "extracurricular_hours_weekly": {
                "Less than 1 hour": "<1_hour", "1-3 hours": "1_3_hours", 
                "4-6 hours": "4_6_hours", "More than 6 hours": "6+_hours"
            },
            "extracurricular_wellbeing_impact": {
                "Positively (helps me academically and reduces stress)": "positive",
                "Mixed impact (helps in some ways, stressful in others)": "mixed",
                "Negatively (hurts academics or increases stress)": "negative",
                "No noticeable effect": "no_effect",
                "Not sure": "unsure"
            },
            "career_preparedness": {
                "Yes, fully prepared": "fully_prepared", "Somewhat prepared": "somewhat_prepared", 
                "Not prepared at all": "not_prepared"
            },
            "career_experience": {"Yes": "yes", "No": "no"},
        }
        
        # Multi-select fields that allow comma-separated values
        self.multi_select_fields = ["stress_factors", "primary_social_platforms"]
        
        # Final schema columns in desired order
        self.required_columns = [
            "response_id", "timestamp", "year_of_study", "school",
            "study_hours_daily", "study_schedule_type", "study_environment", "focus_level", "gpa",
            "sleep_hours_nightly", "sleep_quality", "sleep_productivity_rating", "sleep_disruptions",
            "stress_level", "stress_factors", "academic_overwhelm_frequency", "stress_relief_activity",
            "social_media_hours_daily", "social_media_academic_impact", "primary_social_platforms",
            "extracurricular_type", "extracurricular_hours_weekly", "extracurricular_wellbeing_impact",
            "career_preparedness", "career_experience", "job_confidence", "career_motivation_level"
        ]
    
    def setup_processors(self):
        """Initialize field processors for different data types."""
        self.processors = {}
        
        # Numeric processors with validation ranges
        scale_processor = NumericFieldProcessor(min_val=1, max_val=10)
        for field in ["focus_level", "sleep_productivity_rating", "stress_level", "job_confidence", "career_motivation_level"]:
            self.processors[field] = scale_processor
        
        # Special GPA processor
        self.processors["gpa"] = GPAFieldProcessor()
        
        # Categorical processors
        for field, mapping in self.categorical_mappings.items():
            is_multi = field in self.multi_select_fields
            self.processors[field] = CategoricalFieldProcessor(mapping, is_multi_select=is_multi)
        
        # Default text processor for unmapped fields
        self.default_processor = TextFieldProcessor()
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main transformation method.
        
        Args:
            df: Raw survey DataFrame
            
        Returns:
            Cleaned and standardized DataFrame
        """
        df = df.copy()
        
        # Step 1: Normalize column names
        df = self.normalize_column_names(df)
        
        # Step 2: Generate unique response IDs if missing
        if "response_id" not in df.columns:
            df = self.generate_response_ids(df)
        
        # Step 3: Rename columns to standardized names
        df = self.apply_column_mappings(df)
        
        # Step 4: Process each field according to its type
        df = self.process_fields(df)

        # Step 5: Remove duplicates and enforce schema
        df = self.finalize_data(df)

        return df
    
    def normalize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names by stripping whitespace and Unicode normalization."""
        df.columns = [unicodedata.normalize("NFKC", str(col).strip()) for col in df.columns]
        return df

    def generate_response_ids(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate unique response IDs based on row content hash."""
        def create_hash(row: pd.Series) -> str:
            content = "|".join([str(val) for val in row.values])
            return hashlib.sha256(content.encode('utf-8')).hexdigest()[:24]
        
        df["response_id"] = df.apply(create_hash, axis=1)
        return df
    
    def apply_column_mappings(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply column name mappings to standardize field names."""
        # Create mapping with normalized keys
        normalized_mappings = {
            unicodedata.normalize("NFKC", k.strip()): v 
            for k, v in self.column_mappings.items()
        }
        
        # Apply mappings for existing columns only
        rename_dict = {col: normalized_mappings[col] for col in df.columns if col in normalized_mappings}
        return df.rename(columns=rename_dict)
    
    def process_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process each field using appropriate processor."""
        for column in df.columns:
            if column in self.processors:
                processor = self.processors[column]
            else:
                processor = self.default_processor
            
            df[column] = df[column].apply(processor.process)
        
        return df
    
    def finalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicates, enforce schema, and add metadata."""
        
        # Remove duplicate responses
        if "response_id" in df.columns:
            df = df.drop_duplicates(subset="response_id", keep="last")
        
        # Ensure all required columns exist
        for col in self.required_columns:
            if col not in df.columns:
                df[col] = pd.NA
        
        # Add processing metadata
        df["ingested_at"] = pd.Timestamp.now(tz=pd.Timestamp.now().tz)
        
        # Return with required columns in specified order
        final_columns = self.required_columns + ["ingested_at"]
        return df[final_columns]
    
    def validate_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate input DataFrame schema against expected survey structure.
        
        Returns:
            Dictionary with validation results and statistics
        """
        expected_columns = set(self.column_mappings.keys())
        actual_columns = set(df.columns)
        
        missing_columns = expected_columns - actual_columns
        extra_columns = actual_columns - expected_columns
        matching_columns = expected_columns & actual_columns
        
        return {
            "is_valid": len(missing_columns) == 0,
            "total_responses": len(df),
            "expected_columns": len(expected_columns),
            "actual_columns": len(actual_columns),
            "matching_columns": len(matching_columns),
            "missing_columns": list(missing_columns),
            "extra_columns": list(extra_columns),
            "match_percentage": len(matching_columns) / len(expected_columns) * 100
        }
    
    def get_unmapped_values(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        Identify categorical values that don't have mappings.
        Useful for debugging and updating categorical mappings.
        """
        unmapped = {}
        
        # Apply column mappings first
        df_renamed = self.apply_column_mappings(self.normalize_column_names(df.copy()))
        
        for field, mapping in self.categorical_mappings.items():
            if field not in df_renamed.columns:
                continue
                
            # Get unique values excluding NaN
            unique_values = df_renamed[field].dropna().astype(str).unique()
            normalized_mapping_keys = set(k.lower().strip() for k in mapping.keys())
            
            # Find unmapped values
            unmapped_values = []
            for value in unique_values:
                normalized_value = value.lower().strip()
                if normalized_value not in normalized_mapping_keys and normalized_value != 'nan':
                    unmapped_values.append(value)
            
            if unmapped_values:
                unmapped[field] = unmapped_values
        
        return unmapped