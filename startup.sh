#!/bin/bash
# NMM Kitchen Startup Script
echo "Installing kitchen toolbelt..."
pip install --no-cache-dir -r requirements.txt
echo "Starting the FastAPI Orchestrator..."
uvicorn app.main:app --host 0.0.0.0 --port 8080
