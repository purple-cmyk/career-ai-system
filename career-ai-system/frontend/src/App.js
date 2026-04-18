import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

function App() {
  const [currentView, setCurrentView] = useState('login');
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [offers, setOffers] = useState([]);
  const [recommendations, setRecommendations] = useState(null);

  // Auth states
  const [authForm, setAuthForm] = useState({ email: '', password: '', full_name: '' });
  
  // Profile form
  const [profileForm, setProfileForm] = useState({
    college: '', branch: '', gpa: 7.0, college_tier: 2,
    current_location: '', home_location: '', distance_from_home: 0,
    career_goal: '', internships_count: 0, projects_count: 0,
    wants_to_switch_after: 24, study_time_available: 2.0
  });

  // Offer form
  const [offerForm, setOfferForm] = useState({
    company_name: '', company_type: 'Product', role: '',
    job_description: '', ctc: 0, location: '',
    is_mass_recruiter: false, bond_period: 0, work_mode: 'Office'
  });

  const [resumeFile, setResumeFile] = useState(null);

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchProfile();
      fetchOffers();
    }
  }, [token]);

  const handleRegister = async () => {
    try {
      await axios.post(`${API_URL}/register`, authForm);
      alert('Registration successful! Please login.');
      setCurrentView('login');
    } catch (error) {
      alert(error.response?.data?.detail || 'Registration failed');
    }
  };

  const handleLogin = async () => {
    try {
      const response = await axios.post(`${API_URL}/login`, {
        email: authForm.email,
        password: authForm.password
      });
      setToken(response.data.access_token);
      localStorage.setItem('token', response.data.access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
      setCurrentView('dashboard');
    } catch (error) {
      alert(error.response?.data?.detail || 'Login failed');
    }
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('token');
    setCurrentView('login');
    setUser(null);
    setProfile(null);
  };

  const fetchProfile = async () => {
    try {
      const response = await axios.get(`${API_URL}/profile`);
      setProfile(response.data);
    } catch (error) {
      console.log('No profile found');
    }
  };

  const handleCreateProfile = async () => {
    try {
      await axios.post(`${API_URL}/profile`, profileForm);
      alert('Profile created successfully!');
      fetchProfile();
      setCurrentView('dashboard');
    } catch (error) {
      alert(error.response?.data?.detail || 'Profile creation failed');
    }
  };

  const handleResumeUpload = async () => {
    if (!resumeFile) {
      alert('Please select a resume file');
      return;
    }

    const formData = new FormData();
    formData.append('file', resumeFile);

    try {
      const response = await axios.post(`${API_URL}/resume/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      alert(`Resume uploaded! Skills extracted: ${response.data.extracted_skills.join(', ')}`);
    } catch (error) {
      alert(error.response?.data?.detail || 'Resume upload failed');
    }
  };

  const fetchOffers = async () => {
    try {
      const response = await axios.get(`${API_URL}/offers`);
      setOffers(response.data);
    } catch (error) {
      console.log('No offers found');
    }
  };

  const handleAddOffer = async () => {
    try {
      await axios.post(`${API_URL}/offers`, offerForm);
      alert('Offer added successfully!');
      fetchOffers();
      setOfferForm({
        company_name: '', company_type: 'Product', role: '',
        job_description: '', ctc: 0, location: '',
        is_mass_recruiter: false, bond_period: 0, work_mode: 'Office'
      });
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to add offer');
    }
  };

  const handleGetRecommendations = async () => {
    try {
      const response = await axios.post(`${API_URL}/recommend`);
      setRecommendations(response.data);
      setCurrentView('recommendations');
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to get recommendations');
    }
  };

  // ==================== RENDER VIEWS ====================

  if (!token) {
    return (
      <div className="App">
        <div className="auth-container">
          <h1>🎓 Career AI - Placement Decision Support</h1>
          <div className="auth-tabs">
            <button 
              className={currentView === 'login' ? 'active' : ''}
              onClick={() => setCurrentView('login')}
            >
              Login
            </button>
            <button 
              className={currentView === 'register' ? 'active' : ''}
              onClick={() => setCurrentView('register')}
            >
              Register
            </button>
          </div>

          {currentView === 'login' ? (
            <div className="auth-form">
              <input
                type="email"
                placeholder="Email"
                value={authForm.email}
                onChange={(e) => setAuthForm({...authForm, email: e.target.value})}
              />
              <input
                type="password"
                placeholder="Password"
                value={authForm.password}
                onChange={(e) => setAuthForm({...authForm, password: e.target.value})}
              />
              <button onClick={handleLogin}>Login</button>
            </div>
          ) : (
            <div className="auth-form">
              <input
                type="text"
                placeholder="Full Name"
                value={authForm.full_name}
                onChange={(e) => setAuthForm({...authForm, full_name: e.target.value})}
              />
              <input
                type="email"
                placeholder="Email"
                value={authForm.email}
                onChange={(e) => setAuthForm({...authForm, email: e.target.value})}
              />
              <input
                type="password"
                placeholder="Password"
                value={authForm.password}
                onChange={(e) => setAuthForm({...authForm, password: e.target.value})}
              />
              <button onClick={handleRegister}>Register</button>
            </div>
          )}
        </div>
      </div>
    );
  }

  if (currentView === 'profile' || (!profile && currentView === 'dashboard')) {
    return (
      <div className="App">
        <nav className="navbar">
          <h2>Career AI</h2>
          <button onClick={handleLogout}>Logout</button>
        </nav>
        
        <div className="container">
          <h2>📝 Complete Your Profile</h2>
          <div className="profile-form">
            <div className="form-row">
              <input
                type="text"
                placeholder="College Name"
                value={profileForm.college}
                onChange={(e) => setProfileForm({...profileForm, college: e.target.value})}
              />
              <input
                type="text"
                placeholder="Branch (e.g., CSE)"
                value={profileForm.branch}
                onChange={(e) => setProfileForm({...profileForm, branch: e.target.value})}
              />
            </div>

            <div className="form-row">
              <input
                type="number"
                step="0.01"
                placeholder="GPA"
                value={profileForm.gpa}
                onChange={(e) => setProfileForm({...profileForm, gpa: parseFloat(e.target.value)})}
              />
              <select
                value={profileForm.college_tier}
                onChange={(e) => setProfileForm({...profileForm, college_tier: parseInt(e.target.value)})}
              >
                <option value="1">Tier 1 College</option>
                <option value="2">Tier 2 College</option>
                <option value="3">Tier 3 College</option>
              </select>
            </div>

            <div className="form-row">
              <input
                type="text"
                placeholder="Current Location"
                value={profileForm.current_location}
                onChange={(e) => setProfileForm({...profileForm, current_location: e.target.value})}
              />
              <input
                type="text"
                placeholder="Home Location"
                value={profileForm.home_location}
                onChange={(e) => setProfileForm({...profileForm, home_location: e.target.value})}
              />
            </div>

            <textarea
              placeholder="Career Goal (e.g., Want to switch to product company after 2 years)"
              value={profileForm.career_goal}
              onChange={(e) => setProfileForm({...profileForm, career_goal: e.target.value})}
              rows="3"
            />

            <div className="form-row">
              <input
                type="number"
                placeholder="Internships Count"
                value={profileForm.internships_count}
                onChange={(e) => setProfileForm({...profileForm, internships_count: parseInt(e.target.value)})}
              />
              <input
                type="number"
                placeholder="Projects Count"
                value={profileForm.projects_count}
                onChange={(e) => setProfileForm({...profileForm, projects_count: parseInt(e.target.value)})}
              />
            </div>

            <div className="form-row">
              <input
                type="number"
                placeholder="Plan to switch after (months)"
                value={profileForm.wants_to_switch_after}
                onChange={(e) => setProfileForm({...profileForm, wants_to_switch_after: parseInt(e.target.value)})}
              />
              <input
                type="number"
                step="0.5"
                placeholder="Study time available (hours/day)"
                value={profileForm.study_time_available}
                onChange={(e) => setProfileForm({...profileForm, study_time_available: parseFloat(e.target.value)})}
              />
            </div>

            <button onClick={handleCreateProfile} className="btn-primary">
              Create Profile
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <nav className="navbar">
        <h2>🎓 Career AI</h2>
        <div className="nav-links">
          <button onClick={() => setCurrentView('dashboard')}>Dashboard</button>
          <button onClick={() => setCurrentView('offers')}>Add Offer</button>
          <button onClick={() => setCurrentView('resume')}>Resume</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </nav>

      <div className="container">
        {currentView === 'dashboard' && (
          <>
            <h1>Welcome to Career AI! 🚀</h1>
            <div className="dashboard-stats">
              <div className="stat-card">
                <h3>{offers.length}</h3>
                <p>Job Offers</p>
              </div>
              <div className="stat-card">
                <h3>{profile?.college}</h3>
                <p>College</p>
              </div>
              <div className="stat-card">
                <h3>{profile?.gpa}</h3>
                <p>GPA</p>
              </div>
            </div>

            <h2>Your Job Offers</h2>
            {offers.length === 0 ? (
              <p>No offers yet. Add your first offer!</p>
            ) : (
              <div className="offers-grid">
                {offers.map(offer => (
                  <div key={offer.id} className="offer-card">
                    <h3>{offer.company_name}</h3>
                    <p><strong>Role:</strong> {offer.role}</p>
                    <p><strong>CTC:</strong> ₹{offer.ctc} LPA</p>
                    <p><strong>Location:</strong> {offer.location}</p>
                    {offer.is_mass_recruiter && <span className="badge">Mass Recruiter</span>}
                    {offer.bond_period > 0 && <span className="badge warning">Bond: {offer.bond_period} months</span>}
                  </div>
                ))}
              </div>
            )}

            {offers.length > 0 && (
              <button 
                onClick={handleGetRecommendations} 
                className="btn-primary btn-large"
                style={{marginTop: '20px'}}
              >
                🎯 Get AI Recommendations
              </button>
            )}
          </>
        )}

        {currentView === 'offers' && (
          <>
            <h2>➕ Add New Job Offer</h2>
            <div className="offer-form">
              <input
                type="text"
                placeholder="Company Name"
                value={offerForm.company_name}
                onChange={(e) => setOfferForm({...offerForm, company_name: e.target.value})}
              />

              <select
                value={offerForm.company_type}
                onChange={(e) => setOfferForm({...offerForm, company_type: e.target.value})}
              >
                <option value="Product">Product Company</option>
                <option value="Service">Service Company</option>
                <option value="Startup">Startup</option>
                <option value="MNC">MNC</option>
                <option value="Mass Recruiter">Mass Recruiter</option>
              </select>

              <input
                type="text"
                placeholder="Role"
                value={offerForm.role}
                onChange={(e) => setOfferForm({...offerForm, role: e.target.value})}
              />

              <textarea
                placeholder="Job Description (optional)"
                value={offerForm.job_description}
                onChange={(e) => setOfferForm({...offerForm, job_description: e.target.value})}
                rows="4"
              />

              <div className="form-row">
                <input
                  type="number"
                  step="0.1"
                  placeholder="CTC (in Lakhs)"
                  value={offerForm.ctc}
                  onChange={(e) => setOfferForm({...offerForm, ctc: parseFloat(e.target.value)})}
                />
                <input
                  type="text"
                  placeholder="Location"
                  value={offerForm.location}
                  onChange={(e) => setOfferForm({...offerForm, location: e.target.value})}
                />
              </div>

              <select
                value={offerForm.work_mode}
                onChange={(e) => setOfferForm({...offerForm, work_mode: e.target.value})}
              >
                <option value="Office">Office</option>
                <option value="WFH">Work From Home</option>
                <option value="Hybrid">Hybrid</option>
              </select>

              <div className="form-row">
                <label>
                  <input
                    type="checkbox"
                    checked={offerForm.is_mass_recruiter}
                    onChange={(e) => setOfferForm({...offerForm, is_mass_recruiter: e.target.checked})}
                  />
                  Mass Recruiter
                </label>

                <input
                  type="number"
                  placeholder="Bond Period (months)"
                  value={offerForm.bond_period}
                  onChange={(e) => setOfferForm({...offerForm, bond_period: parseInt(e.target.value)})}
                />
              </div>

              <button onClick={handleAddOffer} className="btn-primary">
                Add Offer
              </button>
            </div>
          </>
        )}

        {currentView === 'resume' && (
          <>
            <h2>📄 Upload Resume</h2>
            <div className="resume-upload">
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setResumeFile(e.target.files[0])}
              />
              <button onClick={handleResumeUpload} className="btn-primary">
                Upload Resume
              </button>
              <p style={{marginTop: '10px', color: '#666'}}>
                Upload your resume in PDF format. We'll extract your skills automatically.
              </p>
            </div>
          </>
        )}

        {currentView === 'recommendations' && recommendations && (
          <>
            <h2>🎯 AI-Powered Recommendations</h2>
            
            <div className="summary-card">
              <h3>Analysis Summary</h3>
              <p><strong>Total Offers Analyzed:</strong> {recommendations.total_offers}</p>
              <p><strong>Average Score:</strong> {recommendations.analysis_summary.average_recommendation_score}/100</p>
              <div style={{marginTop: '10px'}}>
                {recommendations.analysis_summary.insights.map((insight, idx) => (
                  <p key={idx}>{insight}</p>
                ))}
              </div>
            </div>

            <h3>Detailed Recommendations</h3>
            {recommendations.recommendations.map((rec, idx) => (
              <div key={rec.offer_id} className="recommendation-card">
                <div className="rec-header">
                  <h3>#{idx + 1} {rec.company_name}</h3>
                  <div className="score-badge" style={{
                    backgroundColor: rec.recommendation_score >= 80 ? '#10b981' : 
                                   rec.recommendation_score >= 65 ? '#3b82f6' : 
                                   rec.recommendation_score >= 50 ? '#f59e0b' : '#ef4444'
                  }}>
                    {rec.recommendation_score.toFixed(1)}/100
                  </div>
                </div>

                <p><strong>Role:</strong> {rec.role}</p>
                <p><strong>CTC:</strong> ₹{rec.ctc} LPA</p>

                <div className="recommendation-action">
                  <h4>{rec.recommendation.action}</h4>
                  <p>{rec.recommendation.reason}</p>
                </div>

                <div className="key-insights">
                  <h4>Key Insights:</h4>
                  <ul>
                    {rec.recommendation.key_insights.map((insight, i) => (
                      <li key={i}>{insight}</li>
                    ))}
                  </ul>
                </div>

                <div className="predictions-grid">
                  <div className="prediction-item">
                    <strong>💰 2-Year Salary:</strong>
                    <p>₹{rec.predictions.salary.predicted_2yr_ctc} L ({rec.predictions.salary.growth_percentage}% growth)</p>
                  </div>
                  <div className="prediction-item">
                    <strong>🎯 Skill Match:</strong>
                    <p>{rec.predictions.skill_match.toFixed(1)}%</p>
                  </div>
                  <div className="prediction-item">
                    <strong>⚖️ Work-Life Balance:</strong>
                    <p>{rec.predictions.workload.wlb_score.toFixed(1)}/10</p>
                  </div>
                  <div className="prediction-item">
                    <strong>💵 Yearly Savings:</strong>
                    <p>₹{rec.predictions.savings.yearly.toLocaleString()}</p>
                  </div>
                </div>
              </div>
            ))}

            <button onClick={() => setCurrentView('dashboard')} className="btn-secondary">
              Back to Dashboard
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
