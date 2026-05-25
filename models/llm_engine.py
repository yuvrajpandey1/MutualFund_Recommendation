"""
Groq LLM Integration Module
Integrates Groq API for AI-powered recommendations
"""
from groq import Groq
from typing import List, Dict, Any, Optional
import json

class GroqRecommendationEngine:
    """Uses Groq LLM to generate personalized recommendations"""
    
    def __init__(self, api_key: str):
        """Initialize Groq client"""
        self.client = Groq(api_key=api_key)
        self.model = "mixtral-8x7b-32768"
        self.conversation_history = []
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for the recommendation engine"""
        return """You are an expert financial advisor specializing in mutual fund recommendations. 
Your role is to:
1. Understand customer investment goals, risk tolerance, and time horizon
2. Provide personalized mutual fund recommendations
3. Explain the benefits and risks of recommended funds
4. Answer questions about mutual funds in a clear, professional manner

Always consider:
- Customer's investment capacity
- Risk appetite and financial goals
- Time horizon for investment
- Current market conditions
- Diversification needs

Provide recommendations in a structured format with fund names, reasons for recommendation, and risk-return profiles."""
    
    def chat(self, user_message: str, funds_context: str = "") -> str:
        """Send a message and get a response from Groq"""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare context with available funds
        system_prompt = self._create_system_prompt()
        if funds_context:
            system_prompt += f"\n\nAvailable Mutual Funds Database:\n{funds_context}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    }
                ] + self.conversation_history,
                temperature=0.7,
                max_tokens=1024,
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        
        except Exception as e:
            error_msg = f"Error communicating with Groq API: {str(e)}"
            print(error_msg)
            return error_msg
    
    def get_recommendation(self, investment_profile: Dict[str, Any], 
                          available_funds: List[Dict[str, Any]]) -> str:
        """Get a recommendation based on investment profile and available funds"""
        
        # Format funds for context
        funds_str = json.dumps(available_funds, indent=2)
        
        # Create prompt for recommendation
        prompt = f"""Based on the following investor profile and available mutual funds, 
provide personalized recommendations:

Investor Profile:
- Investment Amount: ₹{investment_profile.get('investment_amount', 0):,.0f}
- Risk Tolerance: {investment_profile.get('risk_tolerance', 'Medium')}
- Time Horizon: {investment_profile.get('time_horizon', '5+ years')}
- Investment Goals: {investment_profile.get('goals', 'Wealth accumulation')}
- Current Investments: {investment_profile.get('current_investments', 'None mentioned')}

Available Mutual Funds:
{funds_str}

Please recommend the best mutual funds from the available options and explain why they are suitable 
for this investor profile."""
        
        return self.chat(prompt, funds_str)
    
    def answer_question(self, question: str, funds_context: str = "") -> str:
        """Answer a question about mutual funds"""
        return self.chat(question, funds_context)
    
    def analyze_funds(self, selected_funds: List[Dict[str, Any]]) -> str:
        """Analyze and compare selected funds"""
        
        funds_str = json.dumps(selected_funds, indent=2)
        prompt = f"""Please analyze and compare the following mutual funds:

{funds_str}

Provide:
1. Comparative analysis of returns and performance
2. Risk assessment for each fund
3. Which combinations work well together
4. Recommendation for different investor types"""
        
        return self.chat(prompt, funds_str)
    
    def create_portfolio(self, total_amount: float, 
                        risk_profile: str, funds: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a recommended portfolio allocation"""
        
        funds_str = json.dumps(funds, indent=2)
        prompt = f"""Create an optimal portfolio allocation for an investor with:
- Total Investment Amount: ₹{total_amount:,.0f}
- Risk Profile: {risk_profile}
- Available Funds: {funds_str}

Provide the allocation in the following JSON format:
{{
  "portfolio": [
    {{"fund_id": "MF001", "fund_name": "Fund Name", "allocation_percentage": 30, "amount": 30000}},
    ...
  ],
  "total_allocation": 100,
  "reasoning": "Explanation of why this allocation is recommended",
  "expected_return": "Expected return percentage",
  "risk_level": "Risk level of the portfolio"
}}"""
        
        response = self.chat(prompt, funds_str)
        
        # Try to parse JSON response
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                portfolio = json.loads(json_match.group())
                return portfolio
        except:
            pass
        
        return {"raw_response": response}
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history


class RecommendationService:
    """Service layer that combines LLM with mutual fund data"""
    
    def __init__(self, api_key: str, data_provider):
        self.llm_engine = GroqRecommendationEngine(api_key)
        self.data_provider = data_provider
    
    def get_personalized_recommendation(self, investor_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get personalized recommendations combining LLM and data"""
        
        # Get relevant funds
        recommended_funds = self.data_provider.recommend_funds(
            investment_amount=investor_profile.get('investment_amount', 100000),
            risk_profile=investor_profile.get('risk_tolerance', 'medium'),
            time_horizon=investor_profile.get('time_horizon', '5+ years')
        )
        
        # Get LLM recommendation
        llm_recommendation = self.llm_engine.get_recommendation(
            investor_profile,
            recommended_funds
        )
        
        return {
            "funds": recommended_funds,
            "llm_recommendation": llm_recommendation,
            "investor_profile": investor_profile
        }
    
    def chat_with_advisor(self, user_message: str) -> str:
        """Chat with the AI advisor"""
        # Get fund context
        all_funds = self.data_provider.get_all_funds()
        funds_summary = json.dumps(all_funds[:3], indent=2)  # Summary of top funds
        
        return self.llm_engine.answer_question(user_message, funds_summary)
    
    def get_recommendation_with_chat(self, investor_profile: Dict[str, Any], 
                                     user_follow_ups: List[str] = None) -> Dict[str, Any]:
        """Get recommendations with follow-up conversation"""
        
        # Initial recommendation
        initial_recommendation = self.get_personalized_recommendation(investor_profile)
        
        # Process follow-ups if any
        follow_up_responses = []
        if user_follow_ups:
            for question in user_follow_ups:
                response = self.chat_with_advisor(question)
                follow_up_responses.append({
                    "question": question,
                    "answer": response
                })
        
        return {
            "initial_recommendation": initial_recommendation,
            "follow_ups": follow_up_responses,
            "conversation_history": self.llm_engine.get_history()
        }
