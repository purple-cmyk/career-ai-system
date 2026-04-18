# ml_training/features.py

"""
This file defines the full feature schema used for training
the Satisfaction Regression Model.
All features are numeric.
"""

# Student Features
STUDENT_FEATURES = [
    "gpa",
    "college_tier",
    "study_time",
    "switch_months",
    "risk_score",
    "ambition_score",
    "stability_score",
    "learning_score",
    "salary_priority",
    "wlb_preference"
]

# Offer Features
OFFER_FEATURES = [
    "ctc",
    "company_type",        # encoded as numeric
    "location_tier",
    "workload_score",
    "skill_match",
    "savings_rate",
    "switch_probability",
    "predicted_2yr_salary"
]

# Combined Feature List
ALL_FEATURES = STUDENT_FEATURES + OFFER_FEATURES

# Target Column
TARGET_COLUMN = "satisfaction_score"