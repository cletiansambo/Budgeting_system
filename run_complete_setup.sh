#!/bin/bash

echo "Setting up complete Flask Budget Planner..."

# Install required packages
pip3 install flask matplotlib

# Create project structure
mkdir -p Budgeting_system/templates

echo "Project structure created successfully!"
echo ""
echo "To run the application:"
echo "1. cd Budgeting_system"
echo "2. python3 app.py"
echo "3. Open browser to http://localhost:5000"
echo ""
echo "Make sure all template files are in the templates/ directory!"
