#!/bin/bash
# Start FastAPI Backend
# This script activates the virtual environment and runs the FastAPI server

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting FastAPI Backend..."
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
