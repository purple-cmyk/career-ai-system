from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import numpy as np

from app.db.database import engine, get_db, Base
from app.schemas import schemas
from app.services import auth_service, resume_service, prediction_service, decision_service
from app.db import models

# Create tables
print("MAIN APP STARTED")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Career AI - Placement Decision Support System",
    description="AI-powered career guidance for engineering students",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,   # ← IMPORTANT
    allow_methods=["*"],
    allow_headers=["*"],
)



# ==================== AUTHENTICATION ====================

@app.post("/api/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new student user"""
    return auth_service.create_user(db, user)

@app.post("/api/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login and get JWT token"""
    return auth_service.authenticate_user(db, credentials)

# ==================== PROFILE MANAGEMENT ====================

@app.post("/api/profile", response_model=schemas.ProfileResponse)
def create_profile(
    profile: schemas.ProfileCreate,
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update student profile"""
    return auth_service.create_or_update_profile(db, current_user.id, profile)

@app.get("/api/profile", response_model=schemas.ProfileResponse)
def get_profile(
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile"""
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

# ==================== RESUME PROCESSING ====================

@app.post("/api/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and parse resume"""
    return await resume_service.process_resume(db, current_user.id, file)

@app.get("/api/resume/skills")
def get_extracted_skills(
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Get skills extracted from resume"""
    return resume_service.get_user_skills(db, current_user.id)

# ==================== JOB OFFERS ====================

@app.post("/api/offers", response_model=schemas.OfferResponse)
def add_offer(
    offer: schemas.OfferCreate,
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Add a job offer received"""
    db_offer = models.Offer(
        user_id=current_user.id,
        **offer.dict()
    )
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer

@app.get("/api/offers", response_model=List[schemas.OfferResponse])
def get_offers(
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Get all job offers for current user"""
    return db.query(models.Offer).filter(models.Offer.user_id == current_user.id).all()

# ==================== SKILL MATCHING ====================

@app.post("/api/match/skills")
def match_skills(
    job_description: schemas.JobDescription,
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Match user skills with job description"""
    return resume_service.match_skills_with_job(db, current_user.id, job_description.description)

# ==================== PREDICTIONS ====================

@app.post("/api/predict/salary")
def predict_salary(
    offer: schemas.SalaryPredictionInput,
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Predict future salary growth"""
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    return prediction_service.predict_salary_growth(offer, profile)

@app.post("/api/predict/switch")
def predict_switch_probability(
    data: schemas.SwitchPredictionInput,
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Predict probability of switching to better role"""
    return prediction_service.predict_switch_probability(data)

@app.post("/api/predict/workload")
def predict_workload(
    data: schemas.WorkloadPredictionInput,
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Predict workload and work-life balance"""
    return prediction_service.predict_workload(data)

# ==================== DECISION ENGINE (CORE) ====================

@app.post("/api/recommend")
def get_recommendation(
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized recommendation for all offers"""
    return decision_service.generate_recommendations(db, current_user.id)

@app.post("/api/recommend/compare")
def compare_offers(
    offer_ids: schemas.CompareOffersInput,
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Compare specific offers side-by-side"""
    return decision_service.compare_specific_offers(db, current_user.id, offer_ids.offer_ids)

@app.get("/api/explain/{offer_id}")
def explain_recommendation(
    offer_id: int,
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed explanation for a recommendation"""
    return decision_service.explain_decision(db, current_user.id, offer_id)

# ==================== FEEDBACK LOOP ====================

@app.post("/api/feedback")
def submit_feedback(
    feedback: schemas.FeedbackCreate,
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Submit feedback on accepted offer outcome"""
    db_feedback = models.Feedback(
        user_id=current_user.id,
        **feedback.dict()
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return {"message": "Feedback recorded successfully", "id": db_feedback.id}

# ==================== ANALYTICS ====================

@app.get("/api/analytics/career-path")
def get_career_path_projection(
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Get 5-year career path projection"""
    return decision_service.project_career_path(db, current_user.id)

@app.get("/api/analytics/skill-gap")
def analyze_skill_gap(
    current_user: models.User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze skill gaps and suggest improvements"""
    return decision_service.analyze_skill_gaps(db, current_user.id)

# ==================== HEALTH CHECK ====================

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Career AI - Placement Decision Support",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
