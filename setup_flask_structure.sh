#!/bin/bash

echo "Setting up Flask project structure..."

# Create the main project directory
mkdir -p Budgeting_system
cd Budgeting_system

# Create templates directory
mkdir -p templates

# Create static directory for CSS/JS (optional)
mkdir -p static

echo "Flask project structure created:"
echo "Budgeting_system/"
echo "├── app.py"
echo "├── templates/"
echo "│   ├── base.html"
echo "│   ├── welcome.html"
echo "│   ├── income.html"
echo "│   ├── allocation.html"
echo "│   └── chart.html"
echo "└── static/ (optional)"

echo ""
echo "Next steps:"
echo "1. Copy app.py to Budgeting_system/"
echo "2. Copy all HTML templates to Budgeting_system/templates/"
echo "3. Run: cd Budgeting_system && python3 app.py"
