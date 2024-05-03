from flask import render_template
from app import app

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/catching')
def catching():
    return render_template('catching.html')

@app.route('/trading')
def trading():
    return render_template('trading.html')

@app.route('/profile')
def profile():
    return render_template('profile/profileManagement.html')

@app.route('/inventory')
def inventory():
    return render_template('profile/inventory.html')

@app.route('/project-trading')
def projectTrading():
    return render_template('profile/projectTrading.html')