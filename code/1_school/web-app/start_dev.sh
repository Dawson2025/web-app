#!/bin/bash
# Start development environment for the minimal web app

echo "🚀 Starting Minimal Web App Development Environment"
echo "=================================================="

# Activate virtual environment
source .venv/bin/activate

# Run app.py directly
echo "Starting Flask app..."
python app.py
