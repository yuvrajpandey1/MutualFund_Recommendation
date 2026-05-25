@echo off
REM Start Streamlit Application
REM This script activates the virtual environment and runs the Streamlit app

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting Mutual Funds Recommendation System...
streamlit run ui/app.py

pause
