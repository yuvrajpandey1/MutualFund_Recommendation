# Mutual Funds Recommendation System

🚀 An AI-powered mutual funds recommendation system with FastAPI backend and Streamlit UI, powered by Groq LLM.

## Overview

This system combines:
- **Real mutual fund data** (multiple categories: Equity, Debt, Hybrid, Liquid, Gold, International)
- **Advanced AI** (Groq LLM integration for intelligent recommendations)
- **FastAPI backend** for robust API endpoints
- **Streamlit UI** for user-friendly interface

## Features

✨ **Key Features:**
- 📋 Get personalized fund recommendations based on investment profile
- 💬 Chat with an AI financial advisor
- 📊 Browse and compare mutual funds
- 📈 View performance metrics and ratings
- 🤖 AI-powered analysis and recommendations

## Project Structure

```
Recommendation_Systems/
├── data/
│   └── mutual_funds_data.py      # Mutual funds data provider
├── models/
│   └── llm_engine.py              # Groq LLM integration
├── api/
│   └── main.py                    # FastAPI backend
├── ui/
│   └── app.py                     # Streamlit frontend
├── utils/
│   └── __init__.py                # Utility functions
├── config.py                       # Configuration module
├── .env                            # Environment variables
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Installation

### 1. Prerequisites
- Python 3.8+
- pip or conda
- Groq API Key: Get from https://console.groq.com/keys

### 2. Create Virtual Environment

```bash
cd d:\Recommendation_Systems
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create or update `.env` file with your Groq API key:

```bash
GROQ_API_KEY=your-groq-api-key-here
```

## Running the Application

### Option 1: Run Streamlit UI Only

```bash
cd d:\Recommendation_Systems
venv\Scripts\activate
streamlit run ui/app.py
```

The application will open at `http://localhost:8501`

### Option 2: Run FastAPI Backend + Streamlit UI

**Terminal 1 - Start FastAPI Backend:**
```bash
cd d:\Recommendation_Systems
venv\Scripts\activate
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Streamlit UI:**
```bash
cd d:\Recommendation_Systems
venv\Scripts\activate
streamlit run ui/app.py
```

FastAPI will be available at `http://localhost:8000`
Streamlit will be available at `http://localhost:8501`

## Usage

### 1. Get Recommendations
- Navigate to "Get Recommendations" section
- Fill in your investment profile:
  - Investment amount
  - Risk tolerance (Low, Medium, High)
  - Time horizon
  - Investment goals
- Receive AI-powered personalized recommendations

### 2. Chat with Advisor
- Use the chat interface to ask questions
- Get real-time responses from the AI advisor
- Discuss investment strategies and fund details

### 3. Browse Funds
- View all available mutual funds
- Filter by category, risk level, or ratings
- Search for specific funds

### 4. Compare Funds
- Select multiple funds (up to 6)
- Compare performance metrics
- Visual representations of returns and ratings

## API Endpoints

### Core Endpoints

```
GET  /api/funds                    # Get all funds
GET  /api/funds/{fund_id}          # Get specific fund
GET  /api/categories               # Get all categories
GET  /api/categories/{category_id} # Get funds by category
GET  /api/top-rated               # Get top-rated funds
GET  /api/search?query=...         # Search funds
POST /api/recommendations          # Get recommendations
POST /api/chat                     # Chat with advisor
GET  /api/quick-recommendation     # Quick recommendation
GET  /api/compare                  # Compare funds
GET  /api/health                   # Health check
```

### Example Requests

**Get Recommendations:**
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

**Chat with Advisor:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What funds would you recommend for retirement planning?"}'
```

## Deployment on Streamlit Cloud

### Step 1: Prepare Your Repository

1. Create a GitHub repository:
```bash
cd d:\Recommendation_Systems
git init
git add .
git commit -m "Initial commit: Mutual Funds Recommendation System"
git branch -M main
git remote add origin https://github.com/yourusername/recommendation-system.git
git push -u origin main
```

2. Create `.streamlit/secrets.toml` for sensitive data:
```toml
GROQ_API_KEY = "your-groq-api-key-here"
```

3. Update `ui/app.py` to use secrets:
```python
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [Streamlit Cloud Dashboard](https://share.streamlit.io/)
2. Click "New app"
3. Connect your GitHub repository
4. Select the repository and specify the main file: `ui/app.py`
5. Click "Deploy"

### Step 3: Add Secrets to Streamlit Cloud

1. In your app settings on Streamlit Cloud
2. Go to Secrets management
3. Add your Groq API key and other configuration

### Step 4: Get Your Public URL

Once deployed, Streamlit Cloud will provide a public URL:
```
https://share.streamlit.io/yourusername/recommendation-system/main/ui/app.py
```

## Deployment on Heroku (Optional)

### 1. Create Procfile:
```
web: streamlit run ui/app.py --logger.level=error
```

### 2. Create Runtime.txt:
```
python-3.9.18
```

### 3. Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

## Configuration

### Environment Variables

Create/update `.env` file:

```bash
# API Configuration
GROQ_API_KEY=your_groq_api_key
API_HOST=0.0.0.0
API_PORT=8000

# LLM Configuration
LLM_MODEL=mixtral-8x7b-32768
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1024

# Application Configuration
DEBUG_MODE=False
LOG_LEVEL=INFO
```

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **AI/LLM**: Groq (Mixtral 8x7B)
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **HTTP Client**: Requests
- **Environment Management**: Python-dotenv

## API Documentation

Once FastAPI is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Troubleshooting

### Issue: Virtual environment activation fails
```bash
# Recreate virtual environment
python -m venv venv --clear
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Streamlit app won't load
```bash
# Clear cache and restart
streamlit cache clear
streamlit run ui/app.py
```

### Issue: Groq API key error
- Verify the API key is correct
- Check `.env` file has proper formatting
- Ensure `python-dotenv` is installed

### Issue: Port already in use
```bash
# For Streamlit (default 8501)
streamlit run ui/app.py --server.port 8502

# For FastAPI (default 8000)
python -m uvicorn api.main:app --port 8001
```

## Development

### Adding New Funds

Edit `data/mutual_funds_data.py` and add to `SAMPLE_MUTUAL_FUNDS`:

```python
{
    "fund_id": "MF009",
    "name": "New Fund",
    "category": "equity",
    "aum": 1000,
    "nav": 100.00,
    ...
}
```

### Modifying LLM Behavior

Edit `models/llm_engine.py` and update `_create_system_prompt()`:

```python
def _create_system_prompt(self) -> str:
    return """Your custom system prompt here..."""
```

## Security Considerations

⚠️ **Important:**
- Never commit your API keys to version control
- Use environment variables for sensitive data
- In production, use proper secrets management (AWS Secrets Manager, Azure Key Vault, etc.)
- Implement rate limiting on API endpoints
- Use HTTPS in production

## Performance Optimization

1. **Caching**: Streamlit automatically caches function results
2. **Database**: Consider adding a database layer for larger datasets
3. **API Rate Limiting**: Implement rate limiting on FastAPI endpoints
4. **LLM Response Caching**: Cache common questions and responses

## Future Enhancements

- 🔄 Real-time mutual fund data integration
- 📱 Mobile application
- 📊 Advanced portfolio analytics
- 🎯 Risk assessment questionnaire
- 💾 User profiles and saved recommendations
- 📧 Email notifications
- 🔐 User authentication and authorization

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Contact the development team
- Check the FAQ section

## Disclaimer

⚠️ **Important Disclaimer:**

This system is for **educational and informational purposes only**. It does not constitute financial advice. 

- Mutual funds are subject to market risks
- Past performance is not indicative of future results
- Always consult with a qualified financial advisor before making investment decisions
- The recommendations provided are based on algorithms and should not be the sole basis for investment decisions

The developers and maintainers of this system are not responsible for any financial losses or decisions made based on the recommendations provided.

---

**Version**: 1.0.0  
**Last Updated**: May 2024  
**Developed with ❤️ using Groq AI**
