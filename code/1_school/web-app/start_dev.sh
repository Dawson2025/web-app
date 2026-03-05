#!/bin/bash
# resource_id: 47b69b4c-eb9e-48da-831e-05e796576043
# Start development environment for the minimal web app

echo "🚀 Starting Minimal Web App Development Environment"
echo "=================================================="

# Activate virtual environment
source .venv/bin/activate

# Run app.py directly
echo "Starting Flask app..."
python app.py
