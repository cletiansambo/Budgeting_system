from flask import Flask, render_template, request, redirect, url_for, session
import os
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

def create_pie_chart(budget_data):
    """Create a pie chart and return it as base64 encoded string"""
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('white')
    
    # Data for pie chart
    labels = ['Needs', 'Wants', 'Savings']
    sizes = [
        budget_data['needs']['amount'],
        budget_data['wants']['amount'],
        budget_data['savings']['amount']
    ]
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    
    # Enhance the chart
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(14)
    
    for text in texts:
        text.set_fontsize(14)
        text.set_fontweight('bold')
    
    ax.set_title('Budget Allocation', fontsize=18, fontweight='bold', pad=20)
    
    # Save to base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150, facecolor='white')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)  # Important: close the figure to free memory
    
    return image_base64

@app.route('/')
def welcome():
    """Welcome page"""
    return render_template('welcome.html')

@app.route('/income', methods=['GET', 'POST'])
def income():
    """Income input page"""
    if request.method == 'POST':
        try:
            income = float(request.form['income'])
            if income <= 0:
                return render_template('income.html', error="Please enter a positive amount")
            
            session['income'] = income
            return redirect(url_for('allocation'))
        except ValueError:
            return render_template('income.html', error="Please enter a valid number")
    
    return render_template('income.html')

@app.route('/allocation', methods=['GET', 'POST'])
def allocation():
    """Budget allocation page"""
    if 'income' not in session:
        return redirect(url_for('income'))
    
    income = session['income']
    
    # Get current values from session or defaults
    needs_percent = session.get('needs_percent', 50)
    wants_percent = session.get('wants_percent', 30)
    savings_percent = session.get('savings_percent', 20)
    
    if request.method == 'POST':
        # Check if it's a preset button
        if 'preset' in request.form:
            preset = request.form['preset']
            if preset == '50-30-20':
                needs_percent, wants_percent, savings_percent = 50, 30, 20
            elif preset == '60-20-20':
                needs_percent, wants_percent, savings_percent = 60, 20, 20
            elif preset == '70-20-10':
                needs_percent, wants_percent, savings_percent = 70, 20, 10
            
            # Store in session and redirect to show updated values
            session['needs_percent'] = needs_percent
            session['wants_percent'] = wants_percent
            session['savings_percent'] = savings_percent
            return redirect(url_for('allocation'))
        
        # Regular form submission
        try:
            needs_percent = float(request.form['needs'])
            wants_percent = float(request.form['wants'])
            savings_percent = float(request.form['savings'])
            
            total_percent = needs_percent + wants_percent + savings_percent
            
            if total_percent != 100:
                # Calculate amounts for display even with error
                needs_amount = income * needs_percent / 100
                wants_amount = income * wants_percent / 100
                savings_amount = income * savings_percent / 100
                
                return render_template('allocation.html', 
                                     income=income,
                                     error=f"Percentages must add up to 100%. Current total: {total_percent}%",
                                     needs=needs_percent,
                                     wants=wants_percent,
                                     savings=savings_percent,
                                     needs_amount=needs_amount,
                                     wants_amount=wants_amount,
                                     savings_amount=savings_amount,
                                     total_percent=total_percent)
            
            # Store allocation in session
            session['needs_percent'] = needs_percent
            session['wants_percent'] = wants_percent
            session['savings_percent'] = savings_percent
            
            return redirect(url_for('chart'))
            
        except ValueError:
            return render_template('allocation.html', 
                                 income=income,
                                 error="Please enter valid percentages",
                                 needs=needs_percent,
                                 wants=wants_percent,
                                 savings=savings_percent)
    
    # Calculate amounts for display
    needs_amount = income * needs_percent / 100
    wants_amount = income * wants_percent / 100
    savings_amount = income * savings_percent / 100
    total_percent = needs_percent + wants_percent + savings_percent
    
    return render_template('allocation.html', 
                         income=income,
                         needs=needs_percent,
                         wants=wants_percent,
                         savings=savings_percent,
                         needs_amount=needs_amount,
                         wants_amount=wants_amount,
                         savings_amount=savings_amount,
                         total_percent=total_percent)

@app.route('/chart')
def chart():
    """Budget chart visualization page"""
    if 'income' not in session:
        return redirect(url_for('income'))
    
    income = session['income']
    needs_percent = session.get('needs_percent', 50)
    wants_percent = session.get('wants_percent', 30)
    savings_percent = session.get('savings_percent', 20)
    
    # Calculate amounts
    needs_amount = income * needs_percent / 100
    wants_amount = income * wants_percent / 100
    savings_amount = income * savings_percent / 100
    
    budget_data = {
        'income': income,
        'needs': {'percent': needs_percent, 'amount': needs_amount},
        'wants': {'percent': wants_percent, 'amount': wants_amount},
        'savings': {'percent': savings_percent, 'amount': savings_amount}
    }
    
    # Create pie chart
    chart_image = create_pie_chart(budget_data)
    
    return render_template('chart.html', budget=budget_data, chart_image=chart_image)

@app.route('/reset')
def reset():
    """Clear session and start over"""
    session.clear()
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    print("Starting Flask Budget Planner...")
    print("Make sure you have the following structure:")
    print("Budgeting_system/")
    print("├── app.py")
    print("└── templates/")
    print("    ├── base.html")
    print("    ├── welcome.html")
    print("    ├── income.html")
    print("    ├── allocation.html")
    print("    └── chart.html")
    print("")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
