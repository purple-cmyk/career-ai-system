# 🎓 Career AI - AI-Assisted Placement Decision Support System

**An intelligent system that helps engineering students make informed placement decisions using Machine Learning and Predictive Analytics**

---

## 🌟 Features

### Core Capabilities
✅ **Intelligent Resume Analysis** - Automatically extract skills from PDF resumes
✅ **ML-Powered Predictions** - Predict salary growth, workload, and career trajectory
✅ **Smart Decision Engine** - Personalized recommendations based on your goals
✅ **Skill Matching** - Compare your skills with job requirements
✅ **Career Path Projection** - Visualize your 5-year career trajectory
✅ **Work-Life Balance Analysis** - Predict workload and burnout risk
✅ **Savings Calculator** - Estimate actual savings based on location and expenses

### Advanced Features
🧠 **Explainable AI** - Understand why the system recommends specific offers
🔄 **Learning Loop** - System learns from user feedback
📊 **Multi-Factor Analysis** - Considers salary, skills, WLB, savings, and switching probability
🎯 **Personalized Weighting** - Recommendations adapt to your career goals
⚖️ **Trade-off Analysis** - Compare lower salary with better skills vs higher salary with poor fit

---

## 🏗️ System Architecture

### Backend (FastAPI + Python)
```
app/
├── main.py                 # Main FastAPI application
├── db/
│   ├── database.py        # Database connection
│   └── models.py          # SQLAlchemy models
├── schemas/
│   └── schemas.py         # Pydantic schemas
└── services/
    ├── auth_service.py    # Authentication & Authorization
    ├── resume_service.py  # Resume parsing & skill extraction
    ├── prediction_service.py  # ML prediction models
    └── decision_service.py    # Core AI decision engine
```

### Frontend (React)
```
frontend/
├── public/
│   └── index.html
└── src/
    ├── App.js            # Main React application
    ├── App.css           # Styling
    └── index.js          # Entry point
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Install Python dependencies**
```bash
cd career_ai_system
pip install -r requirements.txt
```

2. **Run the backend server**
```bash
python -m uvicorn app.main:app --reload
```

Backend will be available at: `http://localhost:8000`

API Documentation (Swagger): `http://localhost:8000/docs`

### Frontend Setup

1. **Install Node dependencies**
```bash
cd frontend
npm install
```

2. **Start the React development server**
```bash
npm start
```

Frontend will be available at: `http://localhost:3000`

---

## 📖 How to Use

### Step 1: Create Account
1. Register with your email and password
2. Login to access the dashboard

### Step 2: Complete Profile
1. Fill in your academic details (College, GPA, Branch)
2. Add location information
3. Specify career goals and preferences
4. Indicate if/when you plan to switch jobs

### Step 3: Upload Resume
1. Go to "Resume" section
2. Upload your PDF resume
3. System automatically extracts skills

### Step 4: Add Job Offers
1. Click "Add Offer"
2. Enter company details, role, CTC, location
3. Optionally add job description
4. Mark if mass recruiter or has bond period

### Step 5: Get Recommendations
1. Click "Get AI Recommendations"
2. Review detailed analysis for each offer
3. See predictions for:
   - 2-year salary growth
   - Skill match percentage
   - Work-life balance score
   - Savings potential
   - Switch probability

### Step 6: Make Informed Decision
- Compare offers side-by-side
- Understand trade-offs
- Accept the best fit for your goals!

---

## 🧠 ML Models & Algorithms

### 1. Salary Growth Predictor
**Algorithm**: Multi-factor regression with weighted scoring

**Inputs**:
- Company type (Product/Service/Startup/MNC)
- Role seniority
- Location (Tier 1/2/3 city)
- College tier
- GPA

**Output**: Predicted CTC after 2 years + growth rate

### 2. Skill Matching Engine
**Algorithm**: TF-IDF vectorization + Cosine similarity

**Process**:
1. Extract skills from resume using NLP
2. Extract required skills from job description
3. Calculate overlap percentage
4. Compute text similarity using TF-IDF

**Output**: Skill match score (0-100%)

### 3. Workload Predictor
**Algorithm**: Rule-based + company type classification

**Factors**:
- Company type (Startups = High, MNC = Medium)
- Work mode (WFH = Lower, Office = Higher)
- Role pressure level

**Output**: Workload score, WLB score, Burnout risk

### 4. Switch Probability Model
**Algorithm**: Multi-factor probability estimation

**Inputs**:
- Skill gap (inverse of skill match)
- Study time available
- Timeline for switch
- Role demand in market

**Output**: Probability of successful switch (0-100%)

### 5. Decision Engine (Core Algorithm)
**Algorithm**: Weighted scoring with dynamic weight adjustment

```python
score = w1 * salary_score + 
        w2 * skill_score + 
        w3 * wlb_score + 
        w4 * savings_score + 
        w5 * switch_score +
        penalties
```

**Dynamic Weighting**:
- Weights adjust based on user's career goal
- If goal = "switch soon" → Higher WLB weight
- If goal = "save money" → Higher salary weight
- If goal = "learn" → Higher skill alignment weight

---

## 📊 Database Schema

### Users Table
- id, email, hashed_password, full_name, created_at

### Profiles Table
- user_id, college, branch, gpa, college_tier
- locations, career_goal, preferences
- wants_to_switch_after, study_time_available

### Resumes Table
- user_id, filename, raw_text, parsed_data
- extracted_skills, skill_embeddings

### Offers Table
- user_id, company_name, role, ctc, location
- predicted_2yr_salary, skill_match_score
- switch_probability, workload_score
- recommendation_score

### Feedbacks Table
- user_id, offer_id, actual_outcomes
- ratings (workload, growth, satisfaction)

---

## 🎯 API Endpoints

### Authentication
- `POST /api/register` - Create new account
- `POST /api/login` - Login and get JWT token

### Profile Management
- `POST /api/profile` - Create/update profile
- `GET /api/profile` - Get current profile

### Resume Processing
- `POST /api/resume/upload` - Upload and parse resume
- `GET /api/resume/skills` - Get extracted skills

### Job Offers
- `POST /api/offers` - Add new offer
- `GET /api/offers` - Get all offers

### Predictions
- `POST /api/predict/salary` - Predict salary growth
- `POST /api/predict/switch` - Predict switch probability
- `POST /api/predict/workload` - Predict workload

### Recommendations (Core)
- `POST /api/recommend` - Get personalized recommendations
- `POST /api/recommend/compare` - Compare specific offers
- `GET /api/explain/{offer_id}` - Get detailed explanation

### Analytics
- `GET /api/analytics/career-path` - 5-year projection
- `GET /api/analytics/skill-gap` - Skill gap analysis

---

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Secure API endpoints
- User data isolation

---

## 🎨 UI/UX Features

- Clean, modern interface
- Responsive design (mobile + desktop)
- Color-coded recommendations
- Interactive dashboards
- Real-time validation

---

## 📈 Future Enhancements

### Planned Features
1. **Advanced ML Models**
   - Neural networks for better predictions
   - Reinforcement learning for career path optimization

2. **Integration with LinkedIn/GitHub**
   - Auto-import skills
   - Track actual career progression

3. **Company Database**
   - Historical placement data
   - Alumni feedback integration

4. **Skill Recommendation Engine**
   - Suggest courses to bridge skill gaps
   - Learning roadmap generation

5. **Mobile App**
   - Native iOS/Android apps

6. **Collaborative Features**
   - Compare with peers anonymously
   - College-wise analytics

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLite (upgradeable to PostgreSQL)
- **ML Libraries**: scikit-learn, NumPy, Pandas
- **NLP**: Basic skill extraction (expandable to spaCy/Transformers)
- **Authentication**: JWT (python-jose)
- **PDF Processing**: PyPDF2

### Frontend
- **Framework**: React
- **HTTP Client**: Axios
- **Styling**: Custom CSS with gradients
- **State Management**: React Hooks

---

## 📝 Project Structure

```
career_ai_system/
│
├── app/                          # Backend
│   ├── main.py                  # FastAPI app
│   ├── db/                      # Database
│   ├── schemas/                 # Pydantic models
│   └── services/                # Business logic
│       ├── auth_service.py
│       ├── resume_service.py
│       ├── prediction_service.py
│       └── decision_service.py  # Core AI engine
│
├── frontend/                     # React frontend
│   ├── public/
│   └── src/
│       ├── App.js
│       ├── App.css
│       └── index.js
│
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── career_ai.db                 # SQLite database (auto-created)
```

---

## 👨‍💻 For Developers

### Adding New ML Models

1. Create model in `app/services/prediction_service.py`
2. Add API endpoint in `app/main.py`
3. Update schema in `app/schemas/schemas.py`
4. Test using `/docs` interface

### Adding New Features

1. Update database models in `app/db/models.py`
2. Create/update service in `app/services/`
3. Add API routes in `app/main.py`
4. Update frontend in `frontend/src/App.js`

---

## 🎓 For Academic Projects

### Report Structure Suggestions

1. **Introduction**
   - Problem statement
   - Motivation
   - Objectives

2. **Literature Review**
   - Existing placement systems
   - ML in career guidance
   - Gap analysis

3. **System Design**
   - Architecture diagram
   - ER diagram
   - Data flow diagram

4. **Implementation**
   - Technology stack
   - ML algorithms
   - Code snippets

5. **Results & Analysis**
   - Accuracy metrics
   - User feedback
   - Case studies

6. **Conclusion & Future Work**

---

## 📊 Sample Use Cases

### Case 1: High Salary vs Better Skills
**Student Profile**: Wants to switch after 2 years
**Offer A**: ₹12 LPA, 90% skill match, good WLB
**Offer B**: ₹15 LPA, 60% skill match, poor WLB

**System Recommendation**: Offer A
**Reason**: Better skill alignment + WLB = easier to upskill and switch to ₹20+ LPA role in 2 years

### Case 2: Mass Recruiter Warning
**Offer**: ₹10 LPA, mass recruiter, 2-year bond
**System**: ⚠️ NOT RECOMMENDED
**Reason**: Limited growth, bond restricts options

### Case 3: Location-Based Savings
**Student**: Lives in Tier 3 city
**Offer A**: ₹15 LPA in Bangalore
**Offer B**: ₹12 LPA in hometown

**System Analysis**:
- Offer A: Monthly savings = ₹50k
- Offer B: Monthly savings = ₹70k
**Better choice**: Offer B for savings-focused goal

---

## 🤝 Contributing

This is an academic project template. Feel free to:
- Fork and customize
- Add new ML models
- Improve UI/UX
- Add more features
- Create pull requests

---

## 📄 License

This project is created for educational purposes. Free to use for academic projects.

---

## 🙏 Acknowledgments

Built for B.Tech CSE students to make better placement decisions using AI and ML.

---

## 📞 Support

For issues or questions:
1. Check the `/docs` API documentation
2. Review this README
3. Test APIs using Postman or Swagger UI

---

## 🎉 Success Metrics

A successful implementation should achieve:
- ✅ User can register, login, and create profile
- ✅ Resume upload and skill extraction works
- ✅ Multiple offers can be added
- ✅ Recommendations are generated with scores
- ✅ Explanations are provided for each recommendation
- ✅ UI is responsive and user-friendly

---

**Built with ❤️ for Engineering Students**

**Version**: 1.0.0
**Last Updated**: February 2026
