# 🚀 QUICK START GUIDE

## 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)

**Backend**:
```bash
pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib python-multipart PyPDF2 scikit-learn numpy pandas
```

**Frontend**:
```bash
cd frontend
npm install
```

### Step 2: Run Backend (1 minute)

```bash
# From project root
python -m uvicorn app.main:app --reload
```

✅ Backend running at: http://127.0.0.1:8000

📚 API Docs at: http://localhost:8000/docs

### Step 3: Run Frontend (1 minute)

```bash
# In a new terminal
cd frontend
npm start
```

✅ Frontend running at: http://localhost:3000

### Step 4: Use the App (1 minute)

1. Open http://localhost:3000
2. Click "Register" → Create account
3. Login with your credentials
4. Complete your profile
5. Upload resume (PDF)
6. Add job offers
7. Click "Get AI Recommendations" 🎯

---

## Demo Credentials

For quick testing:

**Email**: demo@student.com
**Password**: demo123

---

## Sample Data to Test

### Profile:
- College: IIT Delhi
- Branch: CSE
- GPA: 8.5
- Career Goal: "Want to switch to product company after 2 years"

### Offer 1:
- Company: Google
- Type: Product
- Role: Software Engineer
- CTC: 25 LPA
- Location: Bangalore

### Offer 2:
- Company: Infosys
- Type: Service
- Role: Systems Engineer
- CTC: 8 LPA
- Location: Pune

---

## Expected Result

System should recommend:
✅ **Offer 1 (Google)** with ~90/100 score
❌ **Offer 2 (Infosys)** with ~45/100 score

Reasons:
- Google: Higher growth, better skills, good for switching
- Infosys: Limited growth, mass recruiter patterns

---

## Troubleshooting

**Problem**: Can't install packages
**Solution**: Use `pip install --user <package>` or `sudo pip install`

**Problem**: Port 8000 already in use
**Solution**: Use `python -m uvicorn app.main:app --port 8001 --reload`

**Problem**: Frontend won't start
**Solution**: Delete `node_modules` and run `npm install` again

---

## Next Steps

1. ✅ Test all features
2. 📝 Customize for your college data
3. 🎨 Modify UI colors/branding
4. 📊 Add more ML models
5. 🚀 Deploy to cloud

---

**Need Help?** Check:
- README.md - Full documentation
- DOCUMENTATION.md - Technical deep dive
- /docs endpoint - API reference

**Happy Coding! 🎓**
