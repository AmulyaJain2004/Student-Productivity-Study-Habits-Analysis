from django.db import models

# Create your models here.
class StudentSurveyModel(models.Model):
    # Student Information
    student_id = models.AutoField(primary_key=True)
    year_of_study = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    major = models.CharField(max_length=10, choices=[
        ("SOCS", "School of Computer Science"),
        ("SOAE", "School of Advance Engineering"),
        ("SOB", "School of Business"),
        ("SOL", "School of Law"),
        ("SOD", "School of Design"),
        ("SOLS", "School of Liberal Studies"),
        ("SOHST", "School of Health Sciences & Technology"),
    ])
    
    # Study Habits & Academic Performance
    study_hours_per_day = models.CharField(max_length=20, choices=[
        ("1-2", "1-2 hours"),
        ("3-4", "3-4 hours"),
        ("5-6", "5-6 hours"),
        ("More than 6 hours", "More than 6 hours"),
    ])
    study_schedule = models.CharField(max_length=50, choices=[
        ("Weekdays only", "Weekdays only"),
        ("Weekends only", "Weekends only"),
        ("Daily study routine", "Daily study routine"),
        ("Sporadic, depending on assignments/tests", "Sporadic, depending on assignments/tests"),
    ])
    study_environment = models.CharField(max_length=50, choices=[
        ("Noisy (Café, dorm, etc.)", "Noisy (Café, dorm, etc.)"),
        ("Quiet (Library, study room, etc.)", "Quiet (Library, study room, etc.)"),
        ("I don’t have a dedicated study space", "I don’t have a dedicated study space"),
    ])
    focus_level = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # Scale: 1-10
    gpa = models.FloatField()  # Scale: 0.0 - 10.0
    
    # Sleep & Productivity
    avg_sleep_hours = models.CharField(max_length=20, choices=[
        ("Less than 4 hours", "Less than 4 hours"),
        ("4-5 hours", "4-5 hours"),
        ("6-7 hours", "6-7 hours"),
        ("8 or more hours", "8 or more hours"),
    ])
    sleep_quality = models.CharField(max_length=20, choices=[
        ("Poor", "Poor"),
        ("Fair", "Fair"),
        ("Good", "Good"),
        ("Excellent", "Excellent"),
    ])
    productivity_level = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # Scale: 1-10
    sleep_disruption = models.CharField(max_length=20, choices=[
        ("Yes, always", "Yes, always"),
        ("Sometimes", "Sometimes"),
        ("No", "No"),
    ])
    
    # Stress Levels
    stress_level = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # Scale: 1-10
    stress_factors = models.CharField(max_length=50, choices=[
        ("Academic pressure", "Academic pressure"),
        ("Financial concerns", "Financial concerns"),
        ("Personal/Family issues", "Personal/Family issues"),
        ("Time Management", "Time Management"),
        ("Other", "Other"),
    ])
    frequency_of_overwhelm = models.CharField(max_length=20, choices=[
        ("Always", "Always"),
        ("Often", "Often"),
        ("Sometimes", "Sometimes"),
        ("Rarely", "Rarely"),
        ("Never", "Never"),
    ])
    relaxation_techniques = models.CharField(max_length=5, choices=[
        ("Yes", "Yes"),
        ("No", "No"),
    ])  # Yes/No
    
    # Social Media Usage
    social_media_hours = models.CharField(max_length=20, choices=[
        ("Less than 1 hour", "Less than 1 hour"),
        ("1-2 hours", "1-2 hours"),
        ("3-4 hours", "3-4 hours"),
        ("More than 4 hours", "More than 4 hours"),
    ])
    social_media_impact = models.CharField(max_length=50, choices=[
        ("Positively", "Positively"),
        ("Negatively", "Negatively"),
        ("No, it doesn’t affect my academic performance", "No, it doesn’t affect my academic performance"),
        ("Maybe", "Maybe"),
    ])
    social_media_platforms = models.TextField()  # Store comma-separated values

    # Extracurricular Activities
    extracurricular_participation = models.CharField(max_length=5, choices=[
        ("Yes", "Yes"),
        ("No", "No"),
    ])
    extracurricular_hours = models.CharField(max_length=20, choices=[
        ("Less than 1 hour", "Less than 1 hour"),
        ("1-3 hours", "1-3 hours"),
        ("4-6 hours", "4-6 hours"),
        ("More than 6 hours", "More than 6 hours"),
    ])
    extracurricular_impact = models.CharField(max_length=20, choices=[
        ("Positively", "Positively"),
        ("Negatively", "Negatively"),
        ("No Effect", "No Effect"),
    ])
    extracurricular_impact_stress_levels = models.CharField(max_length=20, choices=[
        ("Reduces stress", "Reduces stress"),
        ("Increases stress", "Increases stress"),
        ("No Effect", "No Effect"),
    ])

    # Career Preparedness
    career_preparedness = models.CharField(max_length=30, choices=[
        ("Yes, fully prepared", "Yes, fully prepared"),
        ("Somewhat prepared", "Somewhat prepared"),
        ("Not prepared at all", "Not prepared at all"),
    ])
    internship_experience = models.CharField(max_length=5, choices=[
        ("Yes", "Yes"),
        ("No", "No"),
    ])
    job_confidence = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # Scale: 1-10

    # Financial Stress & Workload
    part_time_job = models.CharField(max_length=5, choices=[
        ("Yes", "Yes"),
        ("No", "No"),
    ])
    work_hours_per_week = models.CharField(max_length=30, choices=[
        ("Less than 5 hours", "Less than 5 hours"),
        ("5-10 hours", "5-10 hours"),
        ("10-15 hours", "10-15 hours"),
        ("More than 15 hours", "More than 15 hours"),
        ("Not Applicable", "Not Applicable"),
    ])
    financial_stress = models.CharField(max_length=5, choices=[
        ("Yes", "Yes"),
        ("No", "No"),
    ])
    financial_stress_impact = models.CharField(max_length=20, choices=[
        ("Negatively", "Negatively"),
        ("Positively", "Positively"),
        ("No Impact", "No Impact"),
    ])
    
    def __str__(self):
        return f"Student {self.student_id} - GPA: {self.gpa}"