"""
FAST API Backend for Mutual Funds Recommendation System
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.mutual_funds_data import data_provider, MutualFundDataProvider
from models.llm_engine import GroqRecommendationEngine, RecommendationService

# Initialize FastAPI app
app = FastAPI(
    title="Mutual Funds Recommendation System",
    description="AI-powered mutual fund recommendations using Groq LLM",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
# Get your Groq API key from: https://console.groq.com/keys
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "your-groq-api-key-here")
recommendation_service = RecommendationService(GROQ_API_KEY, data_provider)

# Pydantic models
class InvestorProfile(BaseModel):
    investment_amount: float
    risk_tolerance: str  # low, medium, high
    time_horizon: str  # 1-3 years, 3-5 years, 5+ years
    goals: str
    current_investments: Optional[str] = None

class ChatMessage(BaseModel):
    message: str

class FundQuery(BaseModel):
    query: str

class PortfolioRequest(BaseModel):
    total_amount: float
    risk_profile: str
    fund_ids: List[str]

class RecommendationRequest(BaseModel):
    investor_profile: InvestorProfile
    follow_up_questions: Optional[List[str]] = None

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Mutual Funds Recommendation System",
        "version": "1.0.0",
        "endpoints": {
            "funds": "/api/funds",
            "categories": "/api/categories",
            "recommendations": "/api/recommendations",
            "chat": "/api/chat"
        }
    }

@app.get("/api/funds")
async def get_all_funds():
    """Get all available mutual funds"""
    try:
        funds = data_provider.get_all_funds()
        return {
            "status": "success",
            "count": len(funds),
            "funds": funds
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/funds/{fund_id}")
async def get_fund(fund_id: str):
    """Get details of a specific fund"""
    try:
        fund = data_provider.get_fund_by_id(fund_id)
        if not fund:
            raise HTTPException(status_code=404, detail="Fund not found")
        return {"status": "success", "fund": fund}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/categories")
async def get_categories():
    """Get all mutual fund categories"""
    try:
        categories = data_provider.get_all_categories()
        return {
            "status": "success",
            "count": len(categories),
            "categories": categories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/categories/{category_id}")
async def get_category(category_id: str):
    """Get funds from a specific category"""
    try:
        funds = data_provider.get_funds_by_category(category_id)
        if not funds:
            raise HTTPException(status_code=404, detail="Category not found or no funds in category")
        return {
            "status": "success",
            "category": category_id,
            "count": len(funds),
            "funds": funds
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/top-rated")
async def get_top_rated(limit: int = 5):
    """Get top-rated mutual funds"""
    try:
        funds = data_provider.get_top_rated_funds(limit)
        return {
            "status": "success",
            "count": len(funds),
            "funds": funds
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
async def search_funds(query: str):
    """Search mutual funds by name or description"""
    try:
        if not query or len(query) < 2:
            raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
        
        results = data_provider.search_funds(query)
        return {
            "status": "success",
            "query": query,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommendations")
async def get_recommendations(request: RecommendationRequest):
    """Get personalized recommendations based on investor profile"""
    try:
        profile_dict = {
            "investment_amount": request.investor_profile.investment_amount,
            "risk_tolerance": request.investor_profile.risk_tolerance,
            "time_horizon": request.investor_profile.time_horizon,
            "goals": request.investor_profile.goals,
            "current_investments": request.investor_profile.current_investments or ""
        }
        
        result = recommendation_service.get_personalized_recommendation(profile_dict)
        
        return {
            "status": "success",
            "recommendations": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_with_advisor(message: ChatMessage):
    """Chat with the AI advisor"""
    try:
        if not message.message or len(message.message.strip()) == 0:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        response = recommendation_service.chat_with_advisor(message.message)
        return {
            "status": "success",
            "message": message.message,
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/quick-recommendation")
async def quick_recommendation(
    amount: float,
    risk: str = "medium",
    horizon: str = "5+ years"
):
    """Get quick recommendation with minimal parameters"""
    try:
        funds = data_provider.recommend_funds(amount, risk, horizon)
        return {
            "status": "success",
            "parameters": {
                "amount": amount,
                "risk": risk,
                "horizon": horizon
            },
            "count": len(funds),
            "funds": funds
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/compare")
async def compare_funds(fund_ids: str, period: str = "1y"):
    """Compare performance of multiple funds"""
    try:
        ids = [f.strip() for f in fund_ids.split(",")]
        comparison = data_provider.get_performance_comparison(ids, period)
        
        return {
            "status": "success",
            "period": period,
            "comparison": comparison.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Mutual Funds Recommendation System",
        "version": "1.0.0"
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"status": "error", "detail": "Resource not found"}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"status": "error", "detail": "Internal server error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
