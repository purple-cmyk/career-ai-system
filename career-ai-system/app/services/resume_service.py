from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
import PyPDF2
import io
import re
from typing import List
from app.db import models
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Common technical skills
TECH_SKILLS = [
    'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 'php', 'swift',
    'kotlin', 'typescript', 'r', 'matlab', 'scala', 'perl', 'dart', 'sql', 'html', 'css',
    'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring', 'fastapi',
    'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'opencv', 'keras',
    'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'jenkins', 'terraform',
    'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch', 'cassandra',
    'machine learning', 'deep learning', 'nlp', 'computer vision', 'data science',
    'api', 'rest', 'graphql', 'microservices', 'agile', 'scrum', 'ci/cd',
    'linux', 'unix', 'bash', 'powershell', 'networking', 'security', 'blockchain'
]

async def process_resume(db: Session, user_id: int, file: UploadFile):
    """Process uploaded resume PDF"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Read PDF
    content = await file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    
    # Extract text
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # Extract skills
    extracted_skills = extract_skills(text)
    
    # Parse structured data
    parsed_data = {
        "education": extract_education(text),
        "experience": extract_experience(text),
        "projects": extract_projects(text),
        "certifications": extract_certifications(text)
    }
    
    # Create resume record
    db_resume = models.Resume(
        user_id=user_id,
        filename=file.filename,
        raw_text=text,
        parsed_data=parsed_data,
        extracted_skills=extracted_skills,
        skill_embeddings=[]  # Will be computed later if needed
    )
    
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    return {
        "message": "Resume processed successfully",
        "resume_id": db_resume.id,
        "extracted_skills": extracted_skills,
        "parsed_data": parsed_data
    }

def extract_skills(text: str) -> List[str]:
    """Extract skills from resume text"""
    text_lower = text.lower()
    found_skills = []
    
    for skill in TECH_SKILLS:
        if skill in text_lower:
            found_skills.append(skill)
    
    return list(set(found_skills))

def extract_education(text: str) -> dict:
    """Extract education information"""
    education = {
        "degrees": [],
        "institutions": []
    }
    
    # Simple regex patterns
    degree_patterns = [
        r'b\.?tech',
        r'bachelor',
        r'm\.?tech',
        r'master',
        r'phd',
        r'diploma'
    ]
    
    for pattern in degree_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            match = re.search(f'{pattern}.*?(?=\\n|$)', text, re.IGNORECASE)
            if match:
                education["degrees"].append(match.group(0).strip())
    
    return education

def extract_experience(text: str) -> List[str]:
    """Extract work experience"""
    experience = []
    
    # Look for common experience keywords
    exp_keywords = ['intern', 'developer', 'engineer', 'analyst', 'consultant']
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for keyword in exp_keywords:
            if keyword in line_lower and len(line) > 10:
                experience.append(line.strip())
                break
    
    return experience[:5]  # Limit to 5 experiences

def extract_projects(text: str) -> List[str]:
    """Extract projects"""
    projects = []
    
    # Look for project section
    if 'project' in text.lower():
        lines = text.split('\n')
        in_project_section = False
        
        for line in lines:
            if 'project' in line.lower():
                in_project_section = True
                continue
            
            if in_project_section and len(line.strip()) > 20:
                projects.append(line.strip())
                if len(projects) >= 5:
                    break
    
    return projects

def extract_certifications(text: str) -> List[str]:
    """Extract certifications"""
    certifications = []
    
    cert_keywords = ['certified', 'certification', 'certificate', 'course']
    lines = text.split('\n')
    
    for line in lines:
        line_lower = line.lower()
        for keyword in cert_keywords:
            if keyword in line_lower and len(line) > 10:
                certifications.append(line.strip())
                break
    
    return certifications[:5]

def get_user_skills(db: Session, user_id: int):
    """Get skills from user's latest resume"""
    resume = db.query(models.Resume).filter(
        models.Resume.user_id == user_id
    ).order_by(models.Resume.uploaded_at.desc()).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found")
    
    return {
        "skills": resume.extracted_skills,
        "resume_id": resume.id
    }

def match_skills_with_job(db: Session, user_id: int, job_description: str):
    """Match user skills with job description using TF-IDF"""
    resume = db.query(models.Resume).filter(
        models.Resume.user_id == user_id
    ).order_by(models.Resume.uploaded_at.desc()).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found")
    
    # Extract skills from job description
    job_skills = extract_skills(job_description)
    user_skills = resume.extracted_skills
    
    # Calculate match score
    if not user_skills or not job_skills:
        match_score = 0.0
    else:
        matching_skills = set(user_skills).intersection(set(job_skills))
        match_score = (len(matching_skills) / len(job_skills)) * 100 if job_skills else 0
    
    # TF-IDF similarity
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([resume.raw_text, job_description])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        text_similarity = similarity * 100
    except:
        text_similarity = match_score
    
    # Combined score
    final_score = (match_score * 0.6 + text_similarity * 0.4)
    
    return {
        "skill_match_score": round(final_score, 2),
        "user_skills": user_skills,
        "job_required_skills": job_skills,
        "matching_skills": list(set(user_skills).intersection(set(job_skills))),
        "missing_skills": list(set(job_skills) - set(user_skills)),
        "text_similarity": round(text_similarity, 2)
    }
