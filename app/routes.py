from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from app import app, db
from app.models import User

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('inventory'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Username or email already taken')
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('User Created Successfully.')
            return redirect(url_for('catching'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')


@app.route('/catching')
@login_required
def catching():
    return render_template('catching.html')

@app.route('/trading')
@login_required
def trading():
    return render_template('trading.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile/profileManagement.html')

@app.route('/inventory')
@login_required
def inventory():
    return render_template('profile/inventory.html')
