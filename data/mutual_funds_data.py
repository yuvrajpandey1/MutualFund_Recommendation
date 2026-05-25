"""
Mutual Funds Data Module
Provides data for mutual fund recommendations
"""
import pandas as pd
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta
import random

# Sample mutual fund categories
MUTUAL_FUND_CATEGORIES = [
    {
        "id": "equity",
        "name": "Equity Funds",
        "description": "Invest in stocks for growth",
        "risk_level": "High",
        "expected_return": "12-15%"
    },
    {
        "id": "debt",
        "name": "Debt Funds",
        "description": "Invest in bonds and fixed income securities",
        "risk_level": "Low",
        "expected_return": "5-8%"
    },
    {
        "id": "hybrid",
        "name": "Hybrid Funds",
        "description": "Mix of equity and debt investments",
        "risk_level": "Medium",
        "expected_return": "8-12%"
    },
    {
        "id": "liquid",
        "name": "Liquid Funds",
        "description": "Short-term, highly liquid investments",
        "risk_level": "Very Low",
        "expected_return": "3-5%"
    },
    {
        "id": "gold",
        "name": "Gold Funds",
        "description": "Invest in gold and precious metals",
        "risk_level": "Medium",
        "expected_return": "6-10%"
    },
    {
        "id": "international",
        "name": "International Funds",
        "description": "Invest in global markets",
        "risk_level": "High",
        "expected_return": "10-15%"
    }
]

# Sample mutual funds data
SAMPLE_MUTUAL_FUNDS = [
    {
        "fund_id": "MF001",
        "name": "Growth Equity Fund",
        "category": "equity",
        "aum": 5000,  # Assets Under Management in Crores
        "nav": 250.50,  # Net Asset Value
        "expense_ratio": 1.2,
        "returns_1y": 15.5,
        "returns_3y": 18.2,
        "returns_5y": 16.8,
        "min_investment": 500,
        "rating": 5,
        "description": "Large-cap equity fund focused on growth"
    },
    {
        "fund_id": "MF002",
        "name": "Premium Debt Fund",
        "category": "debt",
        "aum": 8000,
        "nav": 150.25,
        "expense_ratio": 0.75,
        "returns_1y": 6.5,
        "returns_3y": 6.8,
        "returns_5y": 7.2,
        "min_investment": 1000,
        "rating": 4,
        "description": "Fixed income fund with focus on quality bonds"
    },
    {
        "fund_id": "MF003",
        "name": "Balanced Growth Fund",
        "category": "hybrid",
        "aum": 3500,
        "nav": 180.75,
        "expense_ratio": 1.0,
        "returns_1y": 10.5,
        "returns_3y": 11.2,
        "returns_5y": 10.8,
        "min_investment": 500,
        "rating": 5,
        "description": "60% equity, 40% debt balanced portfolio"
    },
    {
        "fund_id": "MF004",
        "name": "Money Market Fund",
        "category": "liquid",
        "aum": 2000,
        "nav": 100.10,
        "expense_ratio": 0.5,
        "returns_1y": 4.5,
        "returns_3y": 4.8,
        "returns_5y": 5.0,
        "min_investment": 100,
        "rating": 4,
        "description": "Ultra-short-term investment vehicle"
    },
    {
        "fund_id": "MF005",
        "name": "Gold ETF Fund",
        "category": "gold",
        "aum": 1200,
        "nav": 5250.00,
        "expense_ratio": 0.6,
        "returns_1y": 8.5,
        "returns_3y": 7.2,
        "returns_5y": 8.8,
        "min_investment": 500,
        "rating": 4,
        "description": "Fund tracking gold prices"
    },
    {
        "fund_id": "MF006",
        "name": "Global Opportunity Fund",
        "category": "international",
        "aum": 4500,
        "nav": 320.50,
        "expense_ratio": 1.5,
        "returns_1y": 12.5,
        "returns_3y": 14.2,
        "returns_5y": 13.8,
        "min_investment": 1000,
        "rating": 5,
        "description": "Diversified international equity exposure"
    },
    {
        "fund_id": "MF007",
        "name": "Aggressive Growth Fund",
        "category": "equity",
        "aum": 2800,
        "nav": 275.30,
        "expense_ratio": 1.4,
        "returns_1y": 18.5,
        "returns_3y": 20.5,
        "returns_5y": 18.2,
        "min_investment": 500,
        "rating": 4,
        "description": "Mid-cap and small-cap growth focus"
    },
    {
        "fund_id": "MF008",
        "name": "Conservative Hybrid Fund",
        "category": "hybrid",
        "aum": 5500,
        "nav": 165.40,
        "expense_ratio": 0.85,
        "returns_1y": 7.5,
        "returns_3y": 8.2,
        "returns_5y": 8.5,
        "min_investment": 500,
        "rating": 5,
        "description": "30% equity, 70% debt conservative approach"
    },
]

class MutualFundDataProvider:
    """Provides mutual fund data and related operations"""
    
    def __init__(self):
        self.categories = MUTUAL_FUND_CATEGORIES
        self.funds = SAMPLE_MUTUAL_FUNDS
        self.df_funds = pd.DataFrame(self.funds)
    
    def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all mutual fund categories"""
        return self.categories
    
    def get_category_by_id(self, category_id: str) -> Dict[str, Any]:
        """Get a specific category by ID"""
        for cat in self.categories:
            if cat["id"] == category_id:
                return cat
        return None
    
    def get_all_funds(self) -> List[Dict[str, Any]]:
        """Get all mutual funds"""
        return self.funds
    
    def get_funds_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get funds from a specific category"""
        return [f for f in self.funds if f["category"] == category]
    
    def get_top_rated_funds(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top-rated funds"""
        return sorted(self.funds, key=lambda x: x["rating"], reverse=True)[:limit]
    
    def get_funds_by_risk_level(self, risk_level: str) -> List[Dict[str, Any]]:
        """Get funds by risk level"""
        matching_funds = []
        for fund in self.funds:
            category = self.get_category_by_id(fund["category"])
            if category and category["risk_level"] == risk_level:
                matching_funds.append(fund)
        return matching_funds
    
    def get_funds_by_min_investment(self, min_amount: float) -> List[Dict[str, Any]]:
        """Get funds with minimum investment <= specified amount"""
        return [f for f in self.funds if f["min_investment"] <= min_amount]
    
    def search_funds(self, query: str) -> List[Dict[str, Any]]:
        """Search funds by name or description"""
        query_lower = query.lower()
        results = []
        for fund in self.funds:
            if (query_lower in fund["name"].lower() or 
                query_lower in fund["description"].lower()):
                results.append(fund)
        return results
    
    def get_fund_by_id(self, fund_id: str) -> Dict[str, Any]:
        """Get a specific fund by ID"""
        for fund in self.funds:
            if fund["fund_id"] == fund_id:
                return fund
        return None
    
    def get_performance_comparison(self, fund_ids: List[str], 
                                   period: str = "1y") -> pd.DataFrame:
        """Compare performance of multiple funds"""
        period_map = {
            "1y": "returns_1y",
            "3y": "returns_3y",
            "5y": "returns_5y"
        }
        
        performance_data = []
        for fund_id in fund_ids:
            fund = self.get_fund_by_id(fund_id)
            if fund:
                performance_data.append({
                    "fund_id": fund["fund_id"],
                    "name": fund["name"],
                    "returns": fund.get(period_map[period], 0),
                    "rating": fund["rating"]
                })
        
        return pd.DataFrame(performance_data)
    
    def recommend_funds(self, investment_amount: float, 
                       risk_profile: str, time_horizon: str) -> List[Dict[str, Any]]:
        """Get fund recommendations based on investor profile"""
        # Filter by investment amount
        eligible_funds = self.get_funds_by_min_investment(investment_amount)
        
        # Filter by risk profile
        risk_to_category = {
            "low": ["liquid", "debt"],
            "medium": ["hybrid", "gold"],
            "high": ["equity", "international"]
        }
        
        risk_categories = risk_to_category.get(risk_profile.lower(), ["hybrid"])
        filtered_funds = [f for f in eligible_funds 
                         if f["category"] in risk_categories]
        
        # Sort by rating and returns
        sorted_funds = sorted(
            filtered_funds,
            key=lambda x: (x["rating"], x["returns_1y"]),
            reverse=True
        )
        
        return sorted_funds[:5]

# Initialize global data provider
data_provider = MutualFundDataProvider()
