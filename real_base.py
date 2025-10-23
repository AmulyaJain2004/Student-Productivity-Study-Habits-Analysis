import numpy as np
import pandas as pd

# Set seed for reproducibility
np.random.seed(42)

# Number of samples
num_samples = 500

# Define realistic distributions and correlations
data = {
    "student_id": np.arange(1, num_samples + 1),
    "year_of_study": np.random.choice([1, 2, 3, 4, 5], num_samples, p=[0.25, 0.25, 0.2, 0.2, 0.1]),
    "major": np.random.choice(["SOCS", "SOAE", "SOB", "SOL", "SOD", "SOLS", "SOHST"], num_samples),
    
    # Study habits
    "study_hours_per_day": np.random.choice(["1-2", "3-4", "5-6", "More than 6 hours"], num_samples, p=[0.4, 0.35, 0.2, 0.05]),
    "study_schedule": np.random.choice(["Weekdays only", "Weekends only", "Daily study routine", "Sporadic"], num_samples, p=[0.35, 0.1, 0.4, 0.15]),
    "study_environment": np.random.choice(["Noisy", "Quiet", "No dedicated space"], num_samples, p=[0.3, 0.5, 0.2]),
    
    # GPA follows a more natural distribution (higher study hours → higher GPA)
    "gpa": np.round(np.clip(np.random.normal(7.5, 1.5, num_samples), 5, 10), 2),
    
    # Sleep habits
    "avg_sleep_hours": np.random.choice(["<4", "4-5", "6-7", "8+"], num_samples, p=[0.1, 0.3, 0.45, 0.15]),
    "sleep_quality": np.random.choice(["Poor", "Fair", "Good", "Excellent"], num_samples, p=[0.2, 0.4, 0.3, 0.1]),
    
    # Productivity and focus
    "focus_level": np.random.randint(4, 10, num_samples),
    "productivity_level": np.random.randint(3, 10, num_samples),
    
    # Stress and mental health
    "stress_level": np.random.randint(3, 10, num_samples),
    "stress_factors": np.random.choice(["Academics", "Finance", "Personal", "Time Management"], num_samples, p=[0.5, 0.2, 0.15, 0.15]),
    "frequency_of_overwhelm": np.random.choice(["Always", "Often", "Sometimes", "Rarely"], num_samples, p=[0.2, 0.3, 0.4, 0.1]),
    
    # Social media usage
    "social_media_hours": np.random.choice(["<1", "1-2", "3-4", "4+"], num_samples, p=[0.2, 0.4, 0.3, 0.1]),
    "social_media_impact": np.random.choice(["Positive", "Negative", "No effect", "Maybe"], num_samples, p=[0.3, 0.4, 0.2, 0.1]),

    # Extracurriculars
    "extracurricular_participation": np.random.choice(["Yes", "No"], num_samples, p=[0.6, 0.4]),
    "extracurricular_hours": np.random.choice(["<1", "1-3", "4-6", "6+"], num_samples, p=[0.4, 0.4, 0.15, 0.05]),

    # Career & financial aspects
    "career_preparedness": np.random.choice(["Fully", "Somewhat", "Not at all"], num_samples, p=[0.3, 0.5, 0.2]),
    "internship_experience": np.random.choice(["Yes", "No"], num_samples, p=[0.3, 0.7]),
    "job_confidence": np.random.randint(4, 10, num_samples),

    # Part-time job & financial stress
    "part_time_job": np.random.choice(["Yes", "No"], num_samples, p=[0.2, 0.8]),
    "work_hours_per_week": np.random.choice(["<5", "5-10", "10-15", "15+", "NA"], num_samples, p=[0.05, 0.1, 0.05, 0.05, 0.75]),
    "financial_stress": np.random.choice(["Yes", "No"], num_samples, p=[0.3, 0.7]),
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Adjust GPA based on study hours (realism)
study_hours_map = {"1-2": -1.0, "3-4": 0.0, "5-6": 1.0, "More than 6 hours": 1.5}
df["gpa"] += df["study_hours_per_day"].map(study_hours_map)
df["gpa"] = np.clip(df["gpa"], 0, 10)  # Ensure GPA remains in range

# Adjust sleep quality based on stress level
df["sleep_quality"] = df.apply(lambda row: "Poor" if row["stress_level"] > 8 else row["sleep_quality"], axis=1)

# Adjust work hours for part-time job students
df.loc[df["part_time_job"] == "No", "work_hours_per_week"] = "NA"

# Display sample data
df.head()

file_path = "real_synthetic_student_data.csv"
df.to_csv(file_path, index=False)