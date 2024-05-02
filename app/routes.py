from flask import render_template
from app import app

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/catching')
def catching():
    return render_template('catching.html')