import random
from flask import render_template, request, redirect, url_for, flash, Flask, request, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from app import app, db
from app.models import User, Pokemon, Inventory, Trading
# imports for the updating users password:
from app.form import UpdateAccountForm
from werkzeug.security import generate_password_hash, check_password_hash  


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
            new_user = User(username=username, email=email, pokeballs=5) # more advanced logic can be added time permitting.
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
    pokeball_count = current_user.pokeballs
    return render_template('catching.html', pokeball_count=pokeball_count )

@app.route('/catching-pokemon', methods=['POST'])
@login_required
def catching_pokemon():
    if current_user.pokeballs < 1:
        return jsonify({'success': False, 'message': 'Not enough Pokeballs'})

    current_user.deduct_pokeball()
    pokemon_id = random.randint(1, 151)
    pokemon = Pokemon.query.filter_by(id=pokemon_id).first()

    if not pokemon:
        return jsonify({'success': False, 'message': 'Pokemon not found'})

    # Ensure user has an inventory to add Pokémon to
    user_inventory = Inventory.query.filter_by(user_id=current_user.user_id).first()
    if not user_inventory:
        user_inventory = Inventory(user_id=current_user.user_id)
        db.session.add(user_inventory)
        db.session.commit()  # Make sure to commit so the ID is generated

    # Now add the Pokémon to the inventory
    user_inventory.add_pokemon(pokemon_id)

    db.session.commit()

    return jsonify({
        'success': True,
        'pokemon': {'name': pokemon.name, 'image': pokemon.poke_url},
        'newPokeballCount': current_user.pokeballs
    })

@app.route('/trading', methods=['GET', 'POST', 'DELETE'])
@login_required
def trading():
    #current_user = User.query.filter_by(username="long").first()
    trading_data = Trading.query.all()
    current_user_inventory = Inventory.query.filter_by(user_id=current_user.user_id).first()
    if not current_user_inventory:
        # Handle case where user does not have an inventory
        flash('Inventory not found for the current user.')
        return redirect(url_for('inventory'))
    
    current_user_pokemon = current_user_inventory.pokemon_items
    all_pokemon = Pokemon.query.all()

    if request.method == 'POST':
        # Retrieve the Pokémon names from the form data
        pokemon_to_receive_name = request.form['pokemon_to_receive']
        pokemon_to_trade_out_name = request.form['pokemon_to_trade_out']
        
        # Find the IDs of the Pokémon
        pokemon_to_receive_id = Trading.find_pokemon_id(pokemon_to_receive_name)
        pokemon_to_trade_out_id = Trading.find_pokemon_id(pokemon_to_trade_out_name)
        
        if pokemon_to_receive_id and pokemon_to_trade_out_id:
            # Add the trade using the IDs
            Trading.add_trade(user_name=current_user.username, 
                              pokemon_trade_in_id=pokemon_to_receive_id, 
                              pokemon_trade_out_id=pokemon_to_trade_out_id)
            # Optionally, you can redirect or render a new template after adding the trade
            return jsonify({'success': True, 'message': 'Posting trade success'})
        return redirect(url_for('trading'))
    elif request.method == 'DELETE':
        trade_available = False
        
        trade_id = request.args.get('trade_id')
        
        trade = Trading.query.get(trade_id)
        
        user = User.query.filter_by(username=trade.user_name).first()
        
        user_inventory = Inventory.query.filter_by(user_id=user.user_id).first()
        
        pokemon_trade_in = trade.pokemon_trade_in_id
        
        pokemon_trade_out = trade.pokemon_trade_out_id
        
        for pokemon in current_user_pokemon:
            if pokemon.id == pokemon_trade_in: 
                trade_available = True
                break
            
        if (trade_available) and (current_user.user_id != user.user_id):
            for trades in trading_data:
                if trades.user_name == user.username and trades.pokemon_trade_out_id == pokemon_trade_out:
                    if user_inventory.get_pokemon_quantity(trades.pokemon_trade_out_id) == 1:
                        Trading.delete_trade(trades.id)
                        
            user_inventory.add_pokemon(pokemon_trade_in)
            
            current_user_inventory.remove_pokemon(pokemon_trade_in)   
            
            current_user_inventory.add_pokemon(pokemon_trade_out)
            
            user_inventory.remove_pokemon(pokemon_trade_out)
            
            Trading.delete_trade(trade_id)
            
        # else:  
        #     if (current_user.user_id == user.user_id):
        #         flash('You cannot trade against yourself', 'warning')
        #     else:
        #         flash('The Pokémon you are trying to trade out is not in your inventory.', 'warning')
        # return redirect(url_for('trading'))
        else:  
            response_data = {'success': False}
            if (current_user.user_id == user.user_id):
                response_data['message'] = 'You cannot trade against yourself'
            else:
                response_data['message'] = 'The Pokémon you are trying to trade out is not in your inventory'
            return jsonify(response_data)
        
        response_data = {'success': True, 'message': 'Trade successful'}
        return jsonify(response_data)
    else:
        for trade in trading_data:
            print(f"Trade ID: {trade.id}, User Name: {trade.user_name}, Trade In ID: {trade.pokemon_trade_in_id}, Trade Out ID: {trade.pokemon_trade_out_id}")
        
        for pokemon in current_user_pokemon:
            print(f"pokemon ID: {pokemon.id}")
        # Pass the form object to the template along with other data
        return render_template('trading.html', trading_data=trading_data, current_user_pokemon=current_user_pokemon, all_pokemon=all_pokemon, Pokemon=Pokemon)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # Handle form submission logic here if needed
        pass
    return render_template('profile/profileManagement.html', username=current_user.username, form=form)


# @app.route('/inventory')
# @login_required
# def inventory():
#     return render_template('profile/inventory.html')

# newly added:

@app.route('/inventory')
@login_required
def inventory():
    # Fetch the current user's inventory
    inventory = Inventory.query.filter_by(user_id=current_user.user_id).first()
    inventory_pokemon = inventory.pokemon_items if inventory else []

    return render_template('/profile/inventory.html', inventory_pokemon=inventory_pokemon, username=current_user.username)

# this is the route that will update you password for a given user:
@app.route('/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # Update username if it's different
        if current_user.username != form.username.data:
            current_user.username = form.username.data
        
        # Update password
        current_user.password_hash = generate_password_hash(form.password.data)
        
        db.session.commit()
        
        flash('Your account has been updated! For security reasons, you have been logged out. Please log in with your new credentials.', 'success')
        logout_user()
        return redirect(url_for('login'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('update_account.html', form=form)