import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define number of samples
num_samples = 500

# Generate synthetic data
data = {
    "Student_ID": np.arange(1, num_samples + 1),
    "Year_of_Study": np.random.randint(1, 5, num_samples),
    "Major": np.random.choice(["SOCS", "SOAE", "SOB", "SOL", "SOD", "SOLS", "SOHST"], num_samples),
    
    "Study_Hours_Per_Day": np.random.choice(["1-2 hours", "3-4 hours", "5-6 hours", "More than 6 hours"], num_samples),
    "Study_Schedule": np.random.choice(["Weekdays only", "Weekends only", "Daily study routine", "Sporadic, depending on assignments/tests"], num_samples),
    "Study_Environment": np.random.choice(["Quiet", "Noisy", "I don't have any"], num_samples),
    "Focus_Level": np.random.randint(1, 11, num_samples),  # Scale of 1-10
    "GPA": np.round(np.random.uniform(0.0, 10.0, num_samples), 2),  # GPA between 0.0 and 10.0
    
    "Sleep_Hours": np.random.choice(["Less than 4 hours", "4-5 hours", "6-7 hours", "8 or more hours"], num_samples),
    "Sleep_Quality": np.random.choice(["Poor", "Fair", "Good", "Excellent"], num_samples),
    "Productivity_Level": np.random.randint(1, 11, num_samples),
    "Sleep_Disruption": np.random.choice(["Yes", "Sometimes", "No"], num_samples),
    
    "Stress_Level": np.random.randint(1, 11, num_samples),  # Scale of 1-10
    "Stress_Factors": np.random.choice(["Academic", "Financial", "Personal", "Time Management", "Other"], num_samples),
    "Social_Media_Hours": np.random.randint(0, 6, num_samples),
    "Social_Media_Impact": np.random.choice(["Positive", "Negative", "No Effect"], num_samples),
    "Extracurricular_Participation": np.random.choice(["Yes", "No"], num_samples),
    "Extracurricular_Hours": np.random.randint(0, 8, num_samples),
    "Extracurricular_Impact": np.random.choice(["Positive", "Negative", "No Effect"], num_samples),
    "Career_Preparedness": np.random.choice(["Yes", "Somewhat", "No"], num_samples),
    "Internship_Experience": np.random.choice(["Yes", "No"], num_samples),
    "Job_Confidence": np.random.randint(1, 11, num_samples),  # Scale of 1-10
    "Financial_Stress": np.random.choice(["Yes", "No"], num_samples),
    "Part_Time_Job": np.random.choice(["Yes", "No"], num_samples),
    "Work_Hours_Per_Week": np.random.randint(0, 20, num_samples),
}

# Create DataFrame
df = pd.DataFrame(data)

# Save as CSV
file_path = "synthetic_student_data.csv"
df.to_csv(file_path, index=False)

# Display the first few rows
df.head()
