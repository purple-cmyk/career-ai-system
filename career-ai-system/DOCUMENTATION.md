# Career AI - Complete Project Documentation

## 📚 Table of Contents
1. [Project Overview](#project-overview)
2. [Technical Architecture](#technical-architecture)
3. [ML Algorithms Explained](#ml-algorithms-explained)
4. [Installation Guide](#installation-guide)
5. [API Reference](#api-reference)
6. [Database Schema](#database-schema)
7. [Testing Guide](#testing-guide)
8. [Deployment Guide](#deployment-guide)
9. [Academic Project Guidelines](#academic-project-guidelines)

---

## Project Overview

### What Problem Does This Solve?

Engineering students face a critical challenge during campus placements:
- **Multiple job offers** with varying CTCs, roles, and companies
- **Limited time** to make decisions (typically 24-48 hours)
- **Conflicting factors**: High salary vs good work-life balance, brand name vs skill development
- **No systematic way** to evaluate long-term career impact

### Our Solution

An AI-powered system that:
1. Analyzes your profile, resume, and offers
2. Predicts future outcomes (salary growth, career trajectory)
3. Considers your personal goals and constraints
4. Provides data-driven, personalized recommendations

---

## Technical Architecture

### System Components

```
┌─────────────────┐
│   React Frontend│
│   (Port 3000)   │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│  FastAPI Backend│
│   (Port 8000)   │
└────────┬────────┘
         │
    ┌────▼────┬────────┬────────┐
    │         │        │        │
┌───▼───┐ ┌──▼──┐ ┌──▼──┐ ┌───▼────┐
│Auth   │ │Resume│ │ML   │ │Decision│
│Service│ │Service│ │Models│ │Engine  │
└───────┘ └──────┘ └─────┘ └────────┘
         │
    ┌────▼────┐
    │ SQLite  │
    │Database │
    └─────────┘
```

### Data Flow

1. **User Registration** → JWT Token → Authenticated Access
2. **Profile Creation** → Stored in Database
3. **Resume Upload** → PDF Parsing → Skill Extraction → Embeddings
4. **Add Offers** → Stored with metadata
5. **Get Recommendations** → ML Predictions → Decision Engine → Scored Results

---

## ML Algorithms Explained

### 1. Salary Growth Predictor

**Type**: Multi-variable regression with weighted factors

**Mathematical Formula**:
```
predicted_2yr_ctc = current_ctc × growth_rate

where:
growth_rate = company_mult × location_mult × role_mult × college_mult × gpa_mult
```

**Factor Weights**:
- Company Type:
  - Startup: 1.45× (high growth but risky)
  - Product: 1.35× (good growth)
  - MNC: 1.30× (stable growth)
  - Service: 1.20× (moderate growth)
  - Mass Recruiter: 1.15× (limited growth)

- Location:
  - Tier 1 cities (Bangalore, Mumbai, etc.): 1.2×
  - Tier 2/3 cities: 1.1×

- College Tier:
  - Tier 1: 1.3×
  - Tier 2: 1.2×
  - Tier 3: 1.1×

- GPA Impact: `1.0 + (GPA - 6.5) × 0.05`

**Example**:
```
Input:
- Current CTC: ₹10 LPA
- Company: Product
- Location: Bangalore
- College: Tier 1
- GPA: 8.0

Calculation:
growth_rate = 1.35 × 1.2 × 1.0 × 1.3 × 1.075 = 2.26
predicted_2yr = 10 × 2.26 = ₹22.6 LPA
```

---

### 2. Skill Matching Engine

**Algorithm**: TF-IDF + Cosine Similarity

**Steps**:

1. **Skill Extraction from Resume**:
   ```python
   - Parse PDF → Extract text
   - Match against skill dictionary
   - Return: ['python', 'react', 'sql', ...]
   ```

2. **Skill Extraction from Job Description**:
   ```python
   - Parse JD text
   - Extract required skills
   - Return: ['python', 'django', 'postgres', ...]
   ```

3. **Calculate Match**:
   ```python
   # Method 1: Direct overlap
   overlap_score = (matching_skills / required_skills) × 100
   
   # Method 2: TF-IDF similarity
   vectorizer = TfidfVectorizer()
   vectors = vectorizer.fit_transform([resume_text, jd_text])
   similarity = cosine_similarity(vectors[0], vectors[1])
   
   # Final score
   final_score = 0.6 × overlap_score + 0.4 × similarity_score
   ```

**Example**:
```
User Skills: [python, react, sql, docker]
Required Skills: [python, django, postgres, docker]

Matching: [python, docker] = 2/4 = 50%
TF-IDF Similarity: 65%
Final Score: 0.6×50 + 0.4×65 = 56%
```

---

### 3. Workload Predictor

**Algorithm**: Rule-based classification with company profiling

**Workload Scoring** (1-10 scale):

```python
base_workload = {
    'Startup': 8.5,    # High pressure, long hours
    'Product': 6.5,    # Moderate, balanced
    'Service': 7.0,    # Project deadlines
    'MNC': 6.0,        # More structured
    'Mass Recruiter': 7.5  # Variable
}

# Adjustments
if work_mode == 'WFH': workload -= 0.5
if work_mode == 'Office': workload += 0.5
if role in high_pressure_roles: workload += 1.0

# WLB Score (inverse)
wlb_score = 11 - workload_score

# Study Time Available
study_hours_per_day = (10 - workload_score) × 0.5
```

**Example**:
```
Company: Product
Work Mode: Hybrid
Role: Software Engineer

Workload = 6.5 (base) - 0 (hybrid) + 0 (regular role) = 6.5
WLB = 11 - 6.5 = 4.5/10
Study Time = (10 - 6.5) × 0.5 = 1.75 hours/day
```

---

### 4. Switch Probability Model

**Formula**:
```
switch_prob = base_prob + skill_impact + study_impact + 
              timeline_impact + role_demand

where:
- base_prob = 50%
- skill_impact = (100 - skill_gap) × 0.3
- study_impact = min(study_hours × 5, 25)
- timeline_impact = min(months × 1.5, 20)
- role_demand = 15 (if high demand role) else 5
```

**Example**:
```
Skill Gap: 30%
Study Time: 2 hours/day
Timeline: 24 months
Role: Data Scientist (high demand)

switch_prob = 50 + (70×0.3) + (2×5) + (24×1.5) + 15
            = 50 + 21 + 10 + 20 + 15 = 116
            = min(116, 95) = 95%
```

---

### 5. Core Decision Engine

**The Heart of the System**

**Algorithm**: Weighted Multi-Criteria Decision Analysis (MCDA)

**Formula**:
```
final_score = Σ(weight_i × normalized_score_i) + penalties

Components:
1. Salary Score (0-100)
2. Skill Alignment Score (0-100)
3. Work-Life Balance Score (0-100)
4. Savings Score (0-100)
5. Switch Probability Score (0-100)
```

**Dynamic Weight Adjustment**:

```python
# Default weights
weights = {
    'salary': 0.25,
    'skill': 0.25,
    'wlb': 0.20,
    'savings': 0.15,
    'switch': 0.15
}

# Adjust based on user's career goal
if 'switch' in career_goal:
    weights['wlb'] = 0.30      # Need time to study
    weights['switch'] = 0.25    # High priority
    weights['salary'] = 0.20    # Less important now

elif 'save' in career_goal:
    weights['salary'] = 0.35
    weights['savings'] = 0.25

elif 'learn' in career_goal:
    weights['skill'] = 0.35
```

**Penalties**:
```python
penalties = 0
if is_mass_recruiter: penalties -= 15
if bond_period > 0: penalties -= min(20, bond_period/12 × 5)
```

**Score Normalization**:
```python
# Salary score: normalize to 0-100
salary_score = min(100, (predicted/current - 1) × 50 + 50)

# Skill score: already 0-100
skill_score = skill_match_percentage

# WLB score: convert 1-10 to 0-100
wlb_score = wlb_rating × 10

# Savings score: normalize percentage
savings_score = min(100, savings_rate)

# Switch score: already 0-100
switch_score = switch_probability
```

**Complete Example**:

```
User Profile:
- Career Goal: "Want to switch to FAANG after 2 years"
- Wants to switch after: 24 months
- Study time available: 2 hours/day

Offer Analysis:
Company: Tech Startup
CTC: ₹12 LPA
Predicted 2yr: ₹18 LPA
Skill Match: 85%
Workload: 7.5/10 → WLB: 2.5/10
Savings Rate: 45%
Switch Probability: 75%

Adjusted Weights (for switch goal):
salary: 0.20, skill: 0.25, wlb: 0.30, savings: 0.10, switch: 0.25

Score Calculation:
salary_score = ((18/12 - 1) × 50 + 50) = 75
skill_score = 85
wlb_score = 25
savings_score = 45
switch_score = 75

final_score = 0.20×75 + 0.25×85 + 0.30×25 + 0.10×45 + 0.25×75
            = 15 + 21.25 + 7.5 + 4.5 + 18.75
            = 67/100

Recommendation: "👍 RECOMMEND - Good choice"
```

---

## Installation Guide

### System Requirements

- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **Node.js**: 14.0 or higher
- **RAM**: 4GB minimum
- **Storage**: 500MB free space

### Step-by-Step Installation

#### 1. Clone/Extract Project
```bash
cd career_ai_system
```

#### 2. Backend Setup

**Install Python dependencies**:
```bash
pip install -r requirements.txt
```

**Verify installation**:
```bash
python -c "import fastapi; print('FastAPI installed')"
```

**Run backend**:
```bash
python -m uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

#### 3. Frontend Setup

**Install Node packages**:
```bash
cd frontend
npm install
```

**Run frontend**:
```bash
npm start
```

Expected output:
```
Compiled successfully!
Local:            http://localhost:3000
```

### Troubleshooting

**Issue**: ModuleNotFoundError
**Solution**: 
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Issue**: Port already in use
**Solution**:
```bash
# Change port in backend
uvicorn app.main:app --port 8001

# Change port in frontend (package.json)
"start": "PORT=3001 react-scripts start"
```

---

## API Reference

### Authentication APIs

#### Register User
```http
POST /api/register
Content-Type: application/json

{
  "email": "student@example.com",
  "password": "securepass123",
  "full_name": "John Doe"
}

Response: 200 OK
{
  "id": 1,
  "email": "student@example.com",
  "full_name": "John Doe",
  "created_at": "2026-02-04T10:00:00"
}
```

#### Login
```http
POST /api/login

{
  "email": "student@example.com",
  "password": "securepass123"
}

Response: 200 OK
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Profile APIs

#### Create Profile
```http
POST /api/profile
Authorization: Bearer <token>

{
  "college": "IIT Delhi",
  "branch": "CSE",
  "gpa": 8.5,
  "college_tier": 1,
  "career_goal": "Want to switch to product company after 2 years",
  "wants_to_switch_after": 24,
  "study_time_available": 2.0
}
```

### Recommendation API (Most Important)

```http
POST /api/recommend
Authorization: Bearer <token>

Response: 200 OK
{
  "total_offers": 3,
  "recommendations": [
    {
      "offer_id": 1,
      "company_name": "Google",
      "recommendation_score": 92.5,
      "recommendation": {
        "action": "✅ STRONGLY RECOMMEND",
        "reason": "Excellent fit based on your profile and goals",
        "key_insights": [...]
      },
      "predictions": {
        "salary": {...},
        "skill_match": 85,
        "workload": {...},
        "savings": {...}
      }
    }
  ]
}
```

---

## Database Schema

### Complete ER Diagram

```
Users (1) ──── (1) Profile
  │
  ├──── (*) Resumes
  ├──── (*) Offers
  └──── (*) Feedbacks
```

### Table Structures

**users**:
```sql
id: INTEGER PRIMARY KEY
email: VARCHAR UNIQUE
hashed_password: VARCHAR
full_name: VARCHAR
created_at: DATETIME
is_active: BOOLEAN
```

**profiles**:
```sql
id: INTEGER PRIMARY KEY
user_id: INTEGER FOREIGN KEY
college: VARCHAR
branch: VARCHAR
gpa: FLOAT
college_tier: INTEGER
current_location: VARCHAR
home_location: VARCHAR
career_goal: TEXT
wants_to_switch_after: INTEGER
study_time_available: FLOAT
```

**offers**:
```sql
id: INTEGER PRIMARY KEY
user_id: INTEGER FOREIGN KEY
company_name: VARCHAR
role: VARCHAR
ctc: FLOAT
location: VARCHAR
predicted_2yr_salary: FLOAT
skill_match_score: FLOAT
recommendation_score: FLOAT
```

---

## Academic Project Guidelines

### For Minor Project (4-6 weeks)

**Scope**:
1. Basic authentication
2. Profile management
3. Resume upload & skill extraction
4. Add offers
5. Simple recommendations (rule-based)
6. Basic UI

**Deliverables**:
- Working prototype
- Report (20-30 pages)
- Presentation (10-15 slides)

### For Major Project (3-4 months)

**Additional Features**:
1. Advanced ML models
2. Explainable AI
3. Career path projection
4. Skill gap analysis
5. Feedback loop
6. Analytics dashboard

**Deliverables**:
- Production-ready system
- Comprehensive report (50-80 pages)
- Research paper format
- Detailed presentation

### Report Structure

```
1. Title Page
2. Certificate
3. Abstract
4. Acknowledgments
5. Table of Contents
6. List of Figures/Tables

7. Introduction (5 pages)
   - Problem Statement
   - Motivation
   - Objectives
   - Scope

8. Literature Survey (10 pages)
   - Existing Systems
   - Technologies
   - Gap Analysis

9. System Analysis (8 pages)
   - Feasibility Study
   - Requirements
   - Use Cases

10. System Design (12 pages)
    - Architecture
    - ER Diagram
    - DFD
    - UML Diagrams

11. Implementation (15 pages)
    - Tech Stack
    - Code Snippets
    - ML Algorithms
    - Screenshots

12. Testing (5 pages)
    - Test Cases
    - Results
    - Bug Fixes

13. Results & Discussion (5 pages)
    - Performance Metrics
    - User Feedback
    - Analysis

14. Conclusion & Future Work (3 pages)

15. References
16. Appendix (Code listings)
```

---

## Testing Guide

### Manual Testing Checklist

**Authentication**:
- [ ] User can register
- [ ] User can login
- [ ] Invalid credentials rejected
- [ ] JWT token works

**Profile**:
- [ ] Profile creation works
- [ ] Profile update works
- [ ] Data validation works

**Resume**:
- [ ] PDF upload works
- [ ] Skills extracted correctly
- [ ] Resume stored in DB

**Offers**:
- [ ] Can add offers
- [ ] Can view offers
- [ ] Offer validation works

**Recommendations**:
- [ ] Recommendations generated
- [ ] Scores calculated
- [ ] Explanations provided

### API Testing with cURL

```bash
# Test registration
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User"
  }'

# Test login
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

---

## Deployment Guide

### Local Deployment

Already covered in Installation Guide.

### Cloud Deployment (Heroku)

**Backend**:
```bash
# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy
heroku create career-ai-backend
git push heroku main
```

**Frontend**:
```bash
# Build
npm run build

# Deploy to Netlify/Vercel
# Upload build folder
```

---

**End of Documentation**
