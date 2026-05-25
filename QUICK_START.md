# Quick Start Guide

## 🚀 Running Locally

### 1. Activate Virtual Environment

**Windows:**
```bash
d:\Recommendation_Systems\venv\Scripts\activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 2. Run Streamlit Application

```bash
streamlit run ui/app.py
```

The app will open at: `http://localhost:8501`

---

## 🌐 Run Both Frontend and Backend

### Terminal 1 - Start FastAPI Backend

```bash
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

API available at: `http://localhost:8000`  
API Docs: `http://localhost:8000/docs`

### Terminal 2 - Start Streamlit UI

```bash
streamlit run ui/app.py
```

Streamlit available at: `http://localhost:8501`

---

## 📋 Using Scripts

### Windows

**Run Streamlit:**
```bash
run_streamlit.bat
```

**Run API:**
```bash
run_api.bat
```

### Linux/Mac

**Run Streamlit:**
```bash
bash run_streamlit.sh
```

**Run API:**
```bash
bash run_api.sh
```

---

## 🎯 Features to Try

### 1. Get Recommendations
- Click "Get Recommendations"
- Fill in your investment profile
- Get AI-powered recommendations

### 2. Chat with Advisor
- Click "Chat with Advisor"
- Ask questions about mutual funds
- Get expert financial guidance

### 3. Browse Funds
- Click "Browse Funds"
- Filter by category, risk level, or search
- View detailed fund information

### 4. Compare Funds
- Click "Compare Funds"
- Select 2-6 funds
- See performance comparison

---

## 📊 API Usage

### Get All Funds
```bash
curl http://localhost:8000/api/funds
```

### Search Funds
```bash
curl "http://localhost:8000/api/search?query=equity"
```

### Get Recommendations
```bash
curl -X POST http://localhost:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "investor_profile": {
      "investment_amount": 100000,
      "risk_tolerance": "medium",
      "time_horizon": "5+ years",
      "goals": "Wealth Accumulation"
    }
  }'
```

### Chat with Advisor
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What funds would you recommend?"}'
```

### View API Documentation
Open: `http://localhost:8000/docs`

---

## 🔑 Important Configuration

### Groq API Key

The API key is stored in `.env` file:
```bash
GROQ_API_KEY=your-groq-api-key-here
```

For deployment, use Streamlit Cloud Secrets instead.

---

## 📱 Deploying to Streamlit Cloud

See **DEPLOYMENT_GUIDE.md** for detailed instructions.

Quick steps:
1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Connect your repository
4. Select `ui/app.py` as main file
5. Add GROQ_API_KEY in Secrets
6. Deploy!

Your URL will be: `https://share.streamlit.io/yourusername/repository/main/ui/app.py`

---

## 🆘 Troubleshooting

### Virtual Environment Won't Activate

**Recreate it:**
```bash
python -m venv venv --clear
venv\Scripts\activate.ps1
pip install -r requirements.txt
```

### Port Already in Use

**Streamlit (8501):**
```bash
streamlit run ui/app.py --server.port 8502
```

**FastAPI (8000):**
```bash
python -m uvicorn api.main:app --port 8001
```

### ModuleNotFoundError

**Install missing packages:**
```bash
pip install -r requirements.txt
```

### Clear Streamlit Cache

```bash
streamlit cache clear
```

---

## 📚 Project Structure

```
Recommendation_Systems/
├── ui/app.py              → Main Streamlit application
├── api/main.py            → FastAPI backend
├── models/llm_engine.py   → Groq LLM integration
├── data/mutual_funds_data.py → Fund data provider
├── requirements.txt       → Python dependencies
├── .env                   → Environment variables
└── README.md              → Full documentation
```

---

## 📞 Support Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Groq API Docs**: https://console.groq.com/docs
- **GitHub Repository**: [Your repo link]

---

## ✅ Next Steps

1. ✓ Run the application locally
2. ✓ Test all features
3. ✓ Deploy to Streamlit Cloud (see DEPLOYMENT_GUIDE.md)
4. ✓ Share URL with manager
5. ✓ Gather feedback
6. ✓ Iterate and improve

---

**Version**: 1.0.0  
**Last Updated**: May 2024
