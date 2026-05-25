#!/bin/bash
# Start Streamlit Application
# This script activates the virtual environment and runs the Streamlit app

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting Mutual Funds Recommendation System..."
streamlit run ui/app.py
