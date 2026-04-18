# ml_training/generate_dataset.py

import random
import numpy as np
import pandas as pd
from features import ALL_FEATURES, TARGET_COLUMN

NUM_SAMPLES = 4000


def generate_student_features():
    return {
        "gpa": round(random.uniform(6.0, 9.8), 2),
        "college_tier": random.randint(1, 3),
        "study_time": round(random.uniform(0.5, 4.0), 2),  # hours per day
        "switch_months": random.randint(12, 36),

        "risk_score": random.randint(1, 10),
        "ambition_score": random.randint(1, 10),
        "stability_score": random.randint(1, 10),
        "learning_score": random.randint(1, 10),
        "salary_priority": random.randint(1, 10),
        "wlb_preference": random.randint(1, 10),
    }


def generate_offer_features(student):
    ctc = round(random.uniform(4, 25), 2)

    company_type = random.randint(1, 5)  # 1=mass, 5=startup
    location_tier = random.randint(1, 3)

    workload_score = round(random.uniform(4, 9), 2)
    skill_match = random.randint(40, 95)

    savings_rate = round(random.uniform(20, 70), 2)

    predicted_2yr_salary = round(ctc * random.uniform(1.2, 2.2), 2)

    switch_probability = min(
        100,
        (student["study_time"] * 10)
        + (student["ambition_score"] * 3)
        + random.randint(0, 20)
    )

    return {
        "ctc": ctc,
        "company_type": company_type,
        "location_tier": location_tier,
        "workload_score": workload_score,
        "skill_match": skill_match,
        "savings_rate": savings_rate,
        "switch_probability": switch_probability,
        "predicted_2yr_salary": predicted_2yr_salary,
    }


def compute_satisfaction(features):
    salary_growth_score = (
        (features["predicted_2yr_salary"] / features["ctc"]) * 50
    )

    wlb_score = 100 - (features["workload_score"] * 10)

    satisfaction = (
        0.25 * salary_growth_score +
        0.20 * features["skill_match"] +
        0.15 * features["savings_rate"] +
        0.15 * wlb_score +
        0.25 * features["switch_probability"]
    )

    # Add noise
    satisfaction += random.uniform(-5, 5)

    # Clamp between 0 and 100
    satisfaction = max(0, min(100, satisfaction))

    return round(satisfaction, 2)


def generate_dataset():
    data = []

    for _ in range(NUM_SAMPLES):
        student = generate_student_features()
        offer = generate_offer_features(student)

        combined = {**student, **offer}

        combined[TARGET_COLUMN] = compute_satisfaction(combined)

        data.append(combined)

    df = pd.DataFrame(data)

    df.to_csv("app/ml_training/dataset.csv", index=False)
    print("Dataset generated successfully with", len(df), "rows")


if __name__ == "__main__":
    generate_dataset()