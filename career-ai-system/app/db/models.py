from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    profile = relationship("Profile", back_populates="user", uselist=False)
    resumes = relationship("Resume", back_populates="user")
    offers = relationship("Offer", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    college = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    gpa = Column(Float, nullable=False)
    college_tier = Column(Integer, default=2)  # 1=Tier 1, 2=Tier 2, 3=Tier 3
    
    current_location = Column(String)
    home_location = Column(String)
    distance_from_home = Column(Float, default=0.0)  # in km
    
    career_goal = Column(Text)  # Long-term career aspirations
    preferred_domains = Column(JSON)  # List of preferred domains
    preferred_roles = Column(JSON)  # List of preferred roles
    
    internships_count = Column(Integer, default=0)
    projects_count = Column(Integer, default=0)
    
    current_skills = Column(JSON)  # List of skills
    linkedin_url = Column(String)
    github_url = Column(String)
    portfolio_url = Column(String)
    
    wants_to_switch_after = Column(Integer)  # Months after which user plans to switch
    study_time_available = Column(Float)  # Hours per day available for upskilling
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="profile")

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    raw_text = Column(Text)
    parsed_data = Column(JSON)  # Structured parsed data
    extracted_skills = Column(JSON)  # List of skills
    skill_embeddings = Column(JSON)  # Vector embeddings
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="resumes")

class Offer(Base):
    __tablename__ = "offers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    company_name = Column(String, nullable=False)
    company_type = Column(String)  # Product/Service/Startup/MNC
    role = Column(String, nullable=False)
    job_description = Column(Text)
    
    ctc = Column(Float, nullable=False)  # In lakhs
    base_salary = Column(Float)
    location = Column(String, nullable=False)
    
    is_mass_recruiter = Column(Boolean, default=False)
    bond_period = Column(Integer, default=0)  # In months
    
    skill_requirements = Column(JSON)  # Required skills
    work_mode = Column(String)  # WFH/Hybrid/Office
    
    received_date = Column(DateTime, default=datetime.utcnow)
    deadline = Column(DateTime)
    is_accepted = Column(Boolean, default=False)
    
    # ML predictions (filled after analysis)
    predicted_2yr_salary = Column(Float)
    skill_match_score = Column(Float)
    switch_probability = Column(Float)
    workload_score = Column(Float)
    recommendation_score = Column(Float)
    
    user = relationship("User", back_populates="offers")

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    offer_id = Column(Integer, ForeignKey("offers.id"))
    
    actual_experience = Column(Text)
    actual_salary_after_1yr = Column(Float)
    actual_salary_after_2yr = Column(Float)
    did_switch = Column(Boolean)
    switched_after_months = Column(Integer)
    
    workload_rating = Column(Integer)  # 1-10
    growth_rating = Column(Integer)  # 1-10
    satisfaction_rating = Column(Integer)  # 1-10
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="feedbacks")
