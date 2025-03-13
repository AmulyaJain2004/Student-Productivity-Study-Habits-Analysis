# Generated by Django 5.1.7 on 2025-03-13 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StudentSurveyModel",
            fields=[
                ("student_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "year_of_study",
                    models.IntegerField(
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
                    ),
                ),
                (
                    "major",
                    models.CharField(
                        choices=[
                            ("SOCS", "School of Computer Science"),
                            ("SOAE", "School of Advance Engineering"),
                            ("SOB", "School of Business"),
                            ("SOL", "School of Law"),
                            ("SOD", "School of Design"),
                            ("SOLS", "School of Liberal Studies"),
                            ("SOHST", "School of Health Sciences & Technology"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "study_hours_per_day",
                    models.CharField(
                        choices=[
                            ("1-2", "1-2 hours"),
                            ("3-4", "3-4 hours"),
                            ("5-6", "5-6 hours"),
                            ("More than 6 hours", "More than 6 hours"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "study_schedule",
                    models.CharField(
                        choices=[
                            ("Weekdays only", "Weekdays only"),
                            ("Weekends only", "Weekends only"),
                            ("Daily study routine", "Daily study routine"),
                            (
                                "Sporadic, depending on assignments/tests",
                                "Sporadic, depending on assignments/tests",
                            ),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "study_environment",
                    models.CharField(
                        choices=[
                            ("Noisy (Café, dorm, etc.)", "Noisy (Café, dorm, etc.)"),
                            (
                                "Quiet (Library, study room, etc.)",
                                "Quiet (Library, study room, etc.)",
                            ),
                            (
                                "I don’t have a dedicated study space",
                                "I don’t have a dedicated study space",
                            ),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "focus_level",
                    models.IntegerField(
                        choices=[
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                            (5, 5),
                            (6, 6),
                            (7, 7),
                            (8, 8),
                            (9, 9),
                            (10, 10),
                        ]
                    ),
                ),
                ("gpa", models.FloatField()),
                (
                    "avg_sleep_hours",
                    models.CharField(
                        choices=[
                            ("Less than 4 hours", "Less than 4 hours"),
                            ("4-5 hours", "4-5 hours"),
                            ("6-7 hours", "6-7 hours"),
                            ("8 or more hours", "8 or more hours"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "sleep_quality",
                    models.CharField(
                        choices=[
                            ("Poor", "Poor"),
                            ("Fair", "Fair"),
                            ("Good", "Good"),
                            ("Excellent", "Excellent"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "productivity_level",
                    models.IntegerField(
                        choices=[
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                            (5, 5),
                            (6, 6),
                            (7, 7),
                            (8, 8),
                            (9, 9),
                            (10, 10),
                        ]
                    ),
                ),
                (
                    "sleep_disruption",
                    models.CharField(
                        choices=[
                            ("Yes, always", "Yes, always"),
                            ("Sometimes", "Sometimes"),
                            ("No", "No"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "stress_level",
                    models.IntegerField(
                        choices=[
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                            (5, 5),
                            (6, 6),
                            (7, 7),
                            (8, 8),
                            (9, 9),
                            (10, 10),
                        ]
                    ),
                ),
                (
                    "stress_factors",
                    models.CharField(
                        choices=[
                            ("Academic pressure", "Academic pressure"),
                            ("Financial concerns", "Financial concerns"),
                            ("Personal/Family issues", "Personal/Family issues"),
                            ("Time Management", "Time Management"),
                            ("Other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "frequency_of_overwhelm",
                    models.CharField(
                        choices=[
                            ("Always", "Always"),
                            ("Often", "Often"),
                            ("Sometimes", "Sometimes"),
                            ("Rarely", "Rarely"),
                            ("Never", "Never"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "relaxation_techniques",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=5
                    ),
                ),
                (
                    "social_media_hours",
                    models.CharField(
                        choices=[
                            ("Less than 1 hour", "Less than 1 hour"),
                            ("1-2 hours", "1-2 hours"),
                            ("3-4 hours", "3-4 hours"),
                            ("More than 4 hours", "More than 4 hours"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "social_media_impact",
                    models.CharField(
                        choices=[
                            ("Positively", "Positively"),
                            ("Negatively", "Negatively"),
                            (
                                "No, it doesn’t affect my academic performance",
                                "No, it doesn’t affect my academic performance",
                            ),
                            ("Maybe", "Maybe"),
                        ],
                        max_length=50,
                    ),
                ),
                ("social_media_platforms", models.TextField()),
                (
                    "extracurricular_participation",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=5
                    ),
                ),
                (
                    "extracurricular_hours",
                    models.CharField(
                        choices=[
                            ("Less than 1 hour", "Less than 1 hour"),
                            ("1-3 hours", "1-3 hours"),
                            ("4-6 hours", "4-6 hours"),
                            ("More than 6 hours", "More than 6 hours"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "extracurricular_impact",
                    models.CharField(
                        choices=[
                            ("Positively", "Positively"),
                            ("Negatively", "Negatively"),
                            ("No Effect", "No Effect"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "extracurricular_impact_stress_levels",
                    models.CharField(
                        choices=[
                            ("Reduces stress", "Reduces stress"),
                            ("Increases stress", "Increases stress"),
                            ("No Effect", "No Effect"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "career_preparedness",
                    models.CharField(
                        choices=[
                            ("Yes, fully prepared", "Yes, fully prepared"),
                            ("Somewhat prepared", "Somewhat prepared"),
                            ("Not prepared at all", "Not prepared at all"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "internship_experience",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=5
                    ),
                ),
                (
                    "job_confidence",
                    models.IntegerField(
                        choices=[
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                            (5, 5),
                            (6, 6),
                            (7, 7),
                            (8, 8),
                            (9, 9),
                            (10, 10),
                        ]
                    ),
                ),
                (
                    "part_time_job",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=5
                    ),
                ),
                (
                    "work_hours_per_week",
                    models.CharField(
                        choices=[
                            ("Less than 5 hours", "Less than 5 hours"),
                            ("5-10 hours", "5-10 hours"),
                            ("10-15 hours", "10-15 hours"),
                            ("More than 15 hours", "More than 15 hours"),
                            ("Not Applicable", "Not Applicable"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "financial_stress",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=5
                    ),
                ),
                (
                    "financial_stress_impact",
                    models.CharField(
                        choices=[
                            ("Negatively", "Negatively"),
                            ("Positively", "Positively"),
                            ("No Impact", "No Impact"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
