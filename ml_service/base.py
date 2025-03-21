import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define number of samples
num_samples = 500

# Generate synthetic data
data = {
    "student_id": np.arange(1, num_samples + 1),
    "year_of_study": np.random.randint(1, 6, num_samples),
    "major": np.random.choice(["SOCS", "SOAE", "SOB", "SOL", "SOD", "SOLS", "SOHST"], num_samples),
    
    "study_hours_per_day": np.random.choice(["1-2", "3-4", "5-6", "More than 6 hours"], num_samples),
    "study_schedule": np.random.choice([
        "Weekdays only", "Weekends only", "Daily study routine", "Sporadic, depending on assignments/tests"], num_samples),
    "study_environment": np.random.choice([
        "Noisy (Café, dorm, etc.)", "Quiet (Library, study room, etc.)", "I don’t have a dedicated study space"], num_samples),
    "focus_level": np.random.randint(1, 11, num_samples),
    "gpa": np.round(np.random.uniform(0.0, 10.0, num_samples), 2),
    
    "avg_sleep_hours": np.random.choice([
        "Less than 4 hours", "4-5 hours", "6-7 hours", "8 or more hours"], num_samples),
    "sleep_quality": np.random.choice(["Poor", "Fair", "Good", "Excellent"], num_samples),
    "productivity_level": np.random.randint(1, 11, num_samples),
    "sleep_disruption": np.random.choice(["Yes, always", "Sometimes", "No"], num_samples),
    
    "stress_level": np.random.randint(1, 11, num_samples),
    "stress_factors": np.random.choice([
        "Academic pressure", "Financial concerns", "Personal/Family issues", "Time Management", "Other"], num_samples),
    "frequency_of_overwhelm": np.random.choice(["Always", "Often", "Sometimes", "Rarely", "Never"], num_samples),
    "relaxation_techniques": np.random.choice(["Yes", "No"], num_samples),
    
    "social_media_hours": np.random.choice(["Less than 1 hour", "1-2 hours", "3-4 hours", "More than 4 hours"], num_samples),
    "social_media_impact": np.random.choice([
        "Positively", "Negatively", "No, it doesn’t affect my academic performance", "Maybe"], num_samples),
    "social_media_platforms": [", ".join(np.random.choice([
        "Instagram", "Facebook", "X (Twitter)", "Snapchat", "Reddit", "Whatsapp", "Telegram", "YouTube", "Discord", "LinkedIn", "Quora", "Others"], size=np.random.randint(1, 5), replace=False)) for _ in range(num_samples)],
    
    "extracurricular_participation": np.random.choice(["Yes", "No"], num_samples),
    "extracurricular_hours": np.random.choice([
        "Less than 1 hour", "1-3 hours", "4-6 hours", "More than 6 hours"], num_samples),
    "extracurricular_impact": np.random.choice(["Positively", "Negatively", "No Effect"], num_samples),
    "extracurricular_impact_stress_levels": np.random.choice([
        "Reduces stress", "Increases stress", "No Effect"], num_samples),
    
    "career_preparedness": np.random.choice([
        "Yes, fully prepared", "Somewhat prepared", "Not prepared at all"], num_samples),
    "internship_experience": np.random.choice(["Yes", "No"], num_samples),
    "job_confidence": np.random.randint(1, 11, num_samples),
    
    "part_time_job": np.random.choice(["Yes", "No"], num_samples),
    "work_hours_per_week": np.random.choice([
        "Less than 5 hours", "5-10 hours", "10-15 hours", "More than 15 hours", "Not Applicable"], num_samples),
    "financial_stress": np.random.choice(["Yes", "No"], num_samples),
    "financial_stress_impact": np.random.choice(["Negatively", "Positively", "No Impact"], num_samples),
}

# Create DataFrame
df = pd.DataFrame(data)

# Save as CSV
file_path = "synthetic_student_data.csv"
df.to_csv(file_path, index=False)

# Display the first few rows
df.head()
