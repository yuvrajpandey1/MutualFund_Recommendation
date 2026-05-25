"""
Streamlit UI for Mutual Funds Recommendation System
"""
import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.mutual_funds_data import data_provider
from models.llm_engine import RecommendationService

# Configuration
# Get your Groq API key from: https://console.groq.com/keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")

# Initialize session state
if 'recommendation_service' not in st.session_state:
    st.session_state.recommendation_service = RecommendationService(GROQ_API_KEY, data_provider)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Page configuration
st.set_page_config(
    page_title="Mutual Funds Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .recommendation-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .fund-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🏦 Mutual Funds Advisor")
page = st.sidebar.radio(
    "Select Option",
    ["🏠 Home", "💡 Get Recommendations", "💬 Chat with Advisor", 
     "📊 Browse Funds", "📈 Compare Funds", "ℹ️ About"]
)

# Home Page
if page == "🏠 Home":
    st.markdown("<h1 class='main-header'>Mutual Funds Recommendation System</h1>", 
                unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Funds", len(data_provider.get_all_funds()))
    
    with col2:
        st.metric("Categories", len(data_provider.get_all_categories()))
    
    with col3:
        top_funds = data_provider.get_top_rated_funds(1)
        if top_funds:
            st.metric("Top Rated Fund", top_funds[0]["name"][:20])
    
    st.markdown("---")
    
    st.subheader("Welcome to Your AI-Powered Financial Advisor")
    st.write("""
    This platform combines real mutual fund data with advanced AI (powered by Groq) 
    to provide personalized investment recommendations tailored to your financial goals.
    
    **Features:**
    - 📋 **Get Recommendations**: Answer a few questions to get personalized fund recommendations
    - 💬 **Chat with Advisor**: Have a natural conversation with our AI advisor
    - 📊 **Browse Funds**: Explore our comprehensive database of mutual funds
    - 📈 **Compare Funds**: Compare performance metrics of different funds
    
    **Why Choose Us?**
    - AI-powered personalized recommendations
    - Real market data on mutual funds
    - Expert financial guidance
    - Easy-to-understand comparisons
    """)
    
    st.markdown("---")
    st.subheader("Quick Stats")
    
    risk_groups = {
        "Low Risk": ["liquid", "debt"],
        "Medium Risk": ["hybrid", "gold"],
        "High Risk": ["equity", "international"]
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        low_risk_funds = sum(len(data_provider.get_funds_by_category(cat)) 
                             for cat in risk_groups["Low Risk"])
        st.info(f"**Low Risk Funds**: {low_risk_funds}")
    
    with col2:
        medium_risk_funds = sum(len(data_provider.get_funds_by_category(cat)) 
                                for cat in risk_groups["Medium Risk"])
        st.warning(f"**Medium Risk Funds**: {medium_risk_funds}")
    
    with col3:
        high_risk_funds = sum(len(data_provider.get_funds_by_category(cat)) 
                              for cat in risk_groups["High Risk"])
        st.error(f"**High Risk Funds**: {high_risk_funds}")

# Get Recommendations Page
elif page == "💡 Get Recommendations":
    st.title("💡 Get Personalized Recommendations")
    
    st.markdown("---")
    st.subheader("Tell us about your investment profile")
    
    with st.form("recommendation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            investment_amount = st.number_input(
                "Investment Amount (₹)",
                min_value=1000,
                max_value=10000000,
                value=100000,
                step=10000
            )
            
            risk_tolerance = st.selectbox(
                "Risk Tolerance",
                ["Low", "Medium", "High"],
                help="Low: Conservative investments, Medium: Balanced, High: Growth-oriented"
            )
        
        with col2:
            time_horizon = st.selectbox(
                "Investment Time Horizon",
                ["1-3 years", "3-5 years", "5+ years"],
                help="How long do you plan to stay invested?"
            )
            
            investment_goal = st.selectbox(
                "Primary Investment Goal",
                ["Wealth Accumulation", "Retirement Planning", "Child Education", 
                 "Home Purchase", "Emergency Fund", "Other"]
            )
        
        current_investments = st.text_area(
            "Current Investments (Optional)",
            placeholder="Describe your current investment portfolio if any...",
            height=80
        )
        
        submit_button = st.form_submit_button("Get Recommendations", use_container_width=True)
    
    if submit_button:
        with st.spinner("Generating personalized recommendations..."):
            try:
                profile = {
                    "investment_amount": investment_amount,
                    "risk_tolerance": risk_tolerance.lower(),
                    "time_horizon": time_horizon,
                    "goals": investment_goal,
                    "current_investments": current_investments
                }
                
                result = st.session_state.recommendation_service.get_personalized_recommendation(profile)
                
                # Store result in session
                st.session_state.last_recommendation = result
                
                st.success("✅ Recommendations Generated!")
                
                st.markdown("---")
                st.subheader("📋 Recommended Funds for You")
                
                # Display recommended funds
                if result["funds"]:
                    for idx, fund in enumerate(result["funds"], 1):
                        with st.container():
                            col1, col2, col3 = st.columns([2, 1, 1])
                            
                            with col1:
                                st.markdown(f"**{idx}. {fund['name']}**")
                                st.caption(f"Fund ID: {fund['fund_id']} | Category: {fund['category'].upper()}")
                            
                            with col2:
                                st.metric("Rating", f"{'⭐' * fund['rating']}")
                            
                            with col3:
                                st.metric("1Y Return", f"{fund['returns_1y']:.1f}%")
                            
                            col_a, col_b, col_c, col_d = st.columns(4)
                            with col_a:
                                st.metric("Min. Investment", f"₹{fund['min_investment']:.0f}")
                            with col_b:
                                st.metric("AUM", f"₹{fund['aum']}Cr")
                            with col_c:
                                st.metric("NAV", f"₹{fund['nav']:.2f}")
                            with col_d:
                                st.metric("Expense Ratio", f"{fund['expense_ratio']:.2f}%")
                            
                            st.write(fund['description'])
                            st.divider()
                
                st.markdown("---")
                st.subheader("🤖 AI Advisor's Analysis")
                st.info(result["llm_recommendation"])
                
            except Exception as e:
                st.error(f"Error generating recommendations: {str(e)}")

# Chat with Advisor Page
elif page == "💬 Chat with Advisor":
    st.title("💬 Chat with AI Advisor")
    
    st.markdown("---")
    st.write("Ask questions about mutual funds, investment strategies, or get personalized advice!")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask me anything about mutual funds...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message
        st.chat_message("user").write(user_input)
        
        # Get AI response
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.recommendation_service.chat_with_advisor(user_input)
                
                # Add assistant message to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Display assistant message
                st.chat_message("assistant").write(response)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Browse Funds Page
elif page == "📊 Browse Funds":
    st.title("📊 Browse Mutual Funds")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        view_type = st.radio(
            "How would you like to browse?",
            ["All Funds", "By Category", "By Risk Level", "Top Rated", "Search"]
        )
    
    with col2:
        st.write("")
    
    st.markdown("---")
    
    if view_type == "All Funds":
        funds = data_provider.get_all_funds()
        df = pd.DataFrame(funds)
        
        st.subheader(f"All Available Funds ({len(funds)})")
        st.dataframe(
            df[['fund_id', 'name', 'category', 'nav', 'returns_1y', 'rating', 'min_investment']],
            use_container_width=True,
            hide_index=True
        )
    
    elif view_type == "By Category":
        category = st.selectbox(
            "Select Category",
            [cat["name"] for cat in data_provider.get_all_categories()]
        )
        
        category_id = next(cat["id"] for cat in data_provider.get_all_categories() 
                          if cat["name"] == category)
        
        funds = data_provider.get_funds_by_category(category_id)
        
        if funds:
            df = pd.DataFrame(funds)
            st.subheader(f"{category} ({len(funds)} funds)")
            st.dataframe(
                df[['fund_id', 'name', 'nav', 'returns_1y', 'rating', 'aum']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No funds found in this category")
    
    elif view_type == "By Risk Level":
        risk_level = st.selectbox(
            "Select Risk Level",
            ["Very Low", "Low", "Medium", "High"]
        )
        
        funds = data_provider.get_funds_by_risk_level(risk_level)
        
        if funds:
            df = pd.DataFrame(funds)
            st.subheader(f"{risk_level} Risk Funds ({len(funds)} funds)")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No funds found with this risk level")
    
    elif view_type == "Top Rated":
        limit = st.slider("Number of funds to show", 1, 10, 5)
        funds = data_provider.get_top_rated_funds(limit)
        
        df = pd.DataFrame(funds)
        st.subheader(f"Top {limit} Rated Funds")
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    elif view_type == "Search":
        search_query = st.text_input("Search for a fund...")
        
        if search_query:
            results = data_provider.search_funds(search_query)
            
            if results:
                df = pd.DataFrame(results)
                st.subheader(f"Search Results ({len(results)} found)")
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No funds found matching your search query")

# Compare Funds Page
elif page == "📈 Compare Funds":
    st.title("📈 Compare Mutual Funds")
    
    st.markdown("---")
    st.write("Select multiple funds to compare their performance")
    
    all_funds = data_provider.get_all_funds()
    fund_options = {f["name"]: f["fund_id"] for f in all_funds}
    
    selected_funds = st.multiselect(
        "Select funds to compare",
        list(fund_options.keys()),
        max_selections=6,
        help="You can select up to 6 funds"
    )
    
    if len(selected_funds) > 1:
        fund_ids = [fund_options[name] for name in selected_funds]
        
        comparison_data = []
        for fund_id in fund_ids:
            fund = data_provider.get_fund_by_id(fund_id)
            if fund:
                comparison_data.append({
                    "Fund Name": fund["name"],
                    "1Y Return": f"{fund['returns_1y']}%",
                    "3Y Return": f"{fund['returns_3y']}%",
                    "5Y Return": f"{fund['returns_5y']}%",
                    "Rating": "⭐" * fund["rating"],
                    "Expense Ratio": f"{fund['expense_ratio']}%",
                    "Min Investment": f"₹{fund['min_investment']}"
                })
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Visualization
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 1Y Returns comparison
            returns_data = []
            for name in selected_funds:
                fund = data_provider.get_fund_by_id(fund_options[name])
                returns_data.append({"Fund": name[:15], "Return": fund['returns_1y']})
            
            df_returns = pd.DataFrame(returns_data)
            st.bar_chart(df_returns.set_index("Fund"))
        
        with col2:
            # Ratings comparison
            rating_data = []
            for name in selected_funds:
                fund = data_provider.get_fund_by_id(fund_options[name])
                rating_data.append({"Fund": name[:15], "Rating": fund['rating']})
            
            df_ratings = pd.DataFrame(rating_data)
            st.bar_chart(df_ratings.set_index("Fund"))
    
    elif len(selected_funds) == 1:
        st.info("Please select at least 2 funds to compare")

# About Page
elif page == "ℹ️ About":
    st.title("ℹ️ About This Platform")
    
    st.markdown("""
    ## 🤖 Mutual Funds Recommendation System
    
    ### Overview
    This platform combines AI technology with mutual fund data to provide personalized investment recommendations.
    It uses advanced language models (powered by Groq) to understand your financial goals and recommend 
    the most suitable mutual funds for your portfolio.
    
    ### Key Features
    
    #### 1. **AI-Powered Recommendations**
    - Powered by Groq's advanced LLM technology
    - Understands your investment profile and goals
    - Provides personalized recommendations backed by financial analysis
    
    #### 2. **Comprehensive Fund Database**
    - Multiple fund categories (Equity, Debt, Hybrid, Liquid, Gold, International)
    - Real-time performance metrics
    - Detailed fund information including NAV, AUM, expense ratios, and ratings
    
    #### 3. **Interactive Chat**
    - Ask questions about mutual funds and investment strategies
    - Get expert financial advice from our AI advisor
    - Natural conversation interface
    
    #### 4. **Fund Comparison**
    - Compare performance metrics of multiple funds
    - Visual representations of returns and ratings
    - Make informed investment decisions
    
    ### Fund Categories
    
    - **Equity Funds**: High growth potential, higher risk
    - **Debt Funds**: Lower risk, stable returns
    - **Hybrid Funds**: Balanced mix of equity and debt
    - **Liquid Funds**: Short-term, highly liquid
    - **Gold Funds**: Precious metals investment
    - **International Funds**: Global market exposure
    
    ### How It Works
    
    1. **Profile Assessment**: Answer questions about your investment goals, risk tolerance, and time horizon
    2. **AI Analysis**: Our LLM analyzes your profile and market conditions
    3. **Recommendations**: Get personalized fund recommendations with explanations
    4. **Monitoring**: Track your recommended funds and adjust as needed
    
    ### Risk Disclaimer
    
    This platform provides information and recommendations for educational purposes. 
    Mutual funds are subject to market risks. Past performance is not indicative of future results.
    Please consult with a financial advisor before making investment decisions.
    
    ### Technologies Used
    
    - **Frontend**: Streamlit
    - **Backend**: FastAPI
    - **AI/LLM**: Groq
    - **Data Processing**: Pandas, NumPy
    - **ML**: Scikit-learn
    
    ### Contact & Support
    
    For questions or support, please reach out to our team.
    
    ---
    
    **Version**: 1.0.0  
    **Last Updated**: 2024
    """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("✅ Fully Functional Platform")
    
    with col2:
        st.warning("⚠️ For Educational Use")
    
    with col3:
        st.success("🚀 Powered by Groq AI")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9rem;'>
    <p>Mutual Funds Recommendation System | Powered by Groq AI | 2024</p>
    <p>Disclaimer: This is for educational purposes. Consult a financial advisor before investing.</p>
</div>
""", unsafe_allow_html=True)
