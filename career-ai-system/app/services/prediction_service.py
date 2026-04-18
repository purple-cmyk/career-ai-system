import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from app.schemas import schemas
from app.db import models
import pickle
import os

# Pre-trained model placeholders (in production, load actual trained models)
# For demo, using rule-based logic with ML-like structure

def predict_salary_growth(offer: schemas.SalaryPredictionInput, profile: models.Profile = None):
    """
    Predict 2-year salary growth based on multiple factors
    
    Factors considered:
    - Company type (Product > Service > Startup)
    - Role seniority
    - Location (Tier 1 cities have higher growth)
    - College tier
    - GPA
    """
    
    base_ctc = offer.current_ctc
    
    # Company type multiplier
    company_multipliers = {
        "Product": 1.35,
        "MNC": 1.30,
        "Startup": 1.45,
        "Service": 1.20,
        "Mass Recruiter": 1.15
    }
    company_mult = company_multipliers.get(offer.company_type, 1.25)
    
    # Location multiplier
    tier1_cities = ['bangalore', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai']
    location_mult = 1.2 if any(city in offer.location.lower() for city in tier1_cities) else 1.1
    
    # Role multiplier
    senior_roles = ['senior', 'lead', 'architect', 'manager', 'principal']
    role_mult = 1.3 if any(term in offer.role.lower() for term in senior_roles) else 1.0
    
    # College tier multiplier
    college_mult = 1.0 + (0.1 * (4 - offer.college_tier))  # Tier 1 = 1.3, Tier 2 = 1.2, Tier 3 = 1.1
    
    # GPA multiplier
    gpa_mult = 1.0 + (offer.gpa - 6.5) * 0.05  # Bonus for GPA > 6.5
    
    # Calculate predicted salary
    growth_rate = company_mult * location_mult * role_mult * college_mult * gpa_mult
    predicted_2yr = base_ctc * growth_rate
    
    # Confidence score
    confidence = min(95, 70 + (offer.gpa - 6.0) * 5 + (4 - offer.college_tier) * 5)
    
    return {
        "current_ctc": base_ctc,
        "predicted_2yr_ctc": round(predicted_2yr, 2),
        "growth_rate": round((predicted_2yr - base_ctc) / base_ctc * 100, 2),
        "absolute_growth": round(predicted_2yr - base_ctc, 2),
        "confidence_score": round(confidence, 2),
        "factors": {
            "company_impact": round(company_mult, 2),
            "location_impact": round(location_mult, 2),
            "role_impact": round(role_mult, 2),
            "college_impact": round(college_mult, 2),
            "gpa_impact": round(gpa_mult, 2)
        }
    }

def predict_switch_probability(data: schemas.SwitchPredictionInput):
    """
    Predict probability of successfully switching to better role
    
    Factors:
    - Current role type
    - Skill gap (0-100)
    - Study time available
    - Timeline for switch
    """
    
    # Base probability
    base_prob = 50.0
    
    # Skill gap impact (lower gap = higher probability)
    skill_impact = (100 - data.skill_gap) * 0.3
    
    # Study time impact
    study_impact = min(data.study_time_available * 5, 25)  # Max 25% boost
    
    # Timeline impact
    timeline_impact = min(data.wants_to_switch_after * 1.5, 20)  # More time = better prep
    
    # Role demand (simplified)
    high_demand_roles = ['software engineer', 'data scientist', 'ml engineer', 'devops', 'sre']
    role_impact = 15 if any(role in data.current_role.lower() for role in high_demand_roles) else 5
    
    switch_probability = base_prob + skill_impact + study_impact + timeline_impact + role_impact
    switch_probability = min(95, max(10, switch_probability))
    
    # Recommended preparation time
    recommended_prep_months = max(6, int(data.skill_gap / 10))
    
    return {
        "switch_probability": round(switch_probability, 2),
        "recommended_preparation_months": recommended_prep_months,
        "skill_gap_impact": round(skill_impact, 2),
        "study_time_impact": round(study_impact, 2),
        "timeline_impact": round(timeline_impact, 2),
        "role_demand_impact": round(role_impact, 2),
        "confidence": "High" if switch_probability > 70 else "Medium" if switch_probability > 50 else "Low"
    }

def predict_workload(data: schemas.WorkloadPredictionInput):
    """
    Predict workload and work-life balance
    
    Returns:
    - Workload score (1-10, higher = more demanding)
    - WLB score
    - Burnout risk
    - Study time availability
    """
    
    # Base workload
    workload = 5.0
    
    # Company type impact
    company_workload = {
        "Startup": 8.5,
        "Product": 6.5,
        "Service": 7.0,
        "MNC": 6.0,
        "Mass Recruiter": 7.5
    }
    workload = company_workload.get(data.company_type, 6.5)
    
    # Work mode impact
    if data.work_mode == "WFH":
        workload -= 0.5
    elif data.work_mode == "Office":
        workload += 0.5
    
    # Role impact
    high_pressure_roles = ['manager', 'lead', 'architect', 'consultant']
    if any(role in data.role.lower() for role in high_pressure_roles):
        workload += 1.0
    
    workload = min(10, max(1, workload))
    
    # WLB score (inverse of workload)
    wlb_score = 11 - workload
    
    # Burnout risk
    burnout_risk = "High" if workload > 7.5 else "Medium" if workload > 5.5 else "Low"
    
    # Available study time (hours per day)
    study_hours = max(0, (10 - workload) * 0.5)
    
    return {
        "workload_score": round(workload, 1),
        "wlb_score": round(wlb_score, 1),
        "burnout_risk": burnout_risk,
        "available_study_hours": round(study_hours, 1),
        "factors": {
            "company_type_impact": data.company_type,
            "work_mode_impact": data.work_mode,
            "role_pressure": "High" if workload > 7 else "Moderate"
        }
    }

def calculate_savings_potential(ctc: float, location: str, distance_from_home: float):
    """Calculate potential savings based on location and distance"""
    
    # Location cost of living
    high_cost_cities = ['mumbai', 'bangalore', 'delhi', 'gurgaon', 'pune']
    medium_cost_cities = ['hyderabad', 'chennai', 'kolkata', 'ahmedabad']
    
    if any(city in location.lower() for city in high_cost_cities):
        expense_rate = 0.50  # 50% of salary
    elif any(city in location.lower() for city in medium_cost_cities):
        expense_rate = 0.40  # 40% of salary
    else:
        expense_rate = 0.35  # 35% of salary
    
    # Distance from home impact (accommodation costs)
    if distance_from_home > 500:  # Far from home
        expense_rate += 0.05
    elif distance_from_home < 50:  # Near home
        expense_rate -= 0.10
    
    monthly_ctc = (ctc * 100000) / 12  # Convert lakhs to rupees
    monthly_expenses = monthly_ctc * expense_rate
    monthly_savings = monthly_ctc - monthly_expenses
    yearly_savings = monthly_savings * 12
    
    return {
        "monthly_take_home": round(monthly_ctc, 2),
        "monthly_expenses": round(monthly_expenses, 2),
        "monthly_savings": round(monthly_savings, 2),
        "yearly_savings": round(yearly_savings, 2),
        "savings_rate": round((1 - expense_rate) * 100, 2),
        "location_expense_level": "High" if expense_rate > 0.45 else "Medium" if expense_rate > 0.35 else "Low"
    }
