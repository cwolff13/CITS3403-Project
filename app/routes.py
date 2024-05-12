import random
from flask import render_template, request, redirect, url_for, flash, Flask, request, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from app import app, db
from app.models import User, Pokemon, Inventory

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
def catching():
    current_user = User.query.filter_by(user_id = 1).first() # Hardcoded user for testing.
    pokeball_count = current_user.pokeballs
    return render_template('catching.html', pokeball_count=pokeball_count)

@app.route('/catching-pokemon', methods=['POST'])
def catching_pokemon():
    current_user_ID = request.json.get('user_id')
    current_user = User.query.filter_by(user_id = current_user_ID).first()

    if not current_user: 
        return jsonify({'success': False, 'message': 'User not found'})

    if current_user.pokeballs < 1:
        return jsonify({'success': False, 'message': 'Not enough Pokeballs'})
    
    current_user.deduct_pokeball()
    pokemon_id = random.randint(1,151)
    pokemon = Pokemon.query.filter_by(id = pokemon_id).first()
    pokeballcount = current_user.pokeballs

    user_inventory = Inventory.query.filter_by(user_id = current_user_ID).first()
    user_inventory.add_pokemon(pokemon_id)

    db.session.commit()

    return jsonify({
        'success': True,
        'pokemon': {'name': pokemon.name, 'image': pokemon.poke_url},
        'newPokeballCount': pokeballcount
    })

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
