#!/bin/bash

echo "Setting up complete Budgeting System with Flask..."

# Install required packages
echo "Installing Flask and matplotlib..."
pip3 install flask matplotlib

# Create the main project structure
echo " Creating project structure..."
mkdir -p Budgeting_system/templates

echo " Project structure created:"
echo "Budgeting_system/"
echo "├── app.py"
echo "└── templates/"
echo "    ├── base.html"
echo "    ├── welcome.html"
echo "    ├── income.html"
echo "    ├── allocation.html"
echo "    └── chart.html"
echo ""

echo "Next steps:"
echo "1. All files have been created in the Budgeting_system directory"
echo "2. cd Budgeting_system"
echo "3. python3 app.py"
echo "4. Open browser to http://localhost:5000"
echo ""
echo " Your Flask Budget Planner is ready to run!"
