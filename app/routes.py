from urllib import request
from app.forms import TradingForm
from flask import render_template, redirect
from app import app
from app.models import Inventory, Pokemon, Trading

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/catching')
def catching():
    return render_template('catching.html')

@app.route('/trading', methods=['GET', 'POST'])
def trading():
    if request.method == 'POST':
        # Retrieve the Pokémon names from the form data
        pokemon_to_receive_name = request.form['pokemon_to_receive']
        pokemon_to_trade_out_name = request.form['pokemon_to_trade_out']
        
        # Find the IDs of the Pokémon
        pokemon_to_receive_id = Trading.find_pokemon_id(pokemon_to_receive_name)
        pokemon_to_trade_out_id = Trading.find_pokemon_id(pokemon_to_trade_out_name)
        
        if pokemon_to_receive_id and pokemon_to_trade_out_id:
            # Add the trade using the IDs
            Trading.add_trade(user_name='example_user', 
                              pokemon_trade_in_id=pokemon_to_receive_id, 
                              pokemon_trade_out_id=pokemon_to_trade_out_id)
            # Optionally, you can redirect or render a new template after adding the trade
            return redirect('/trading')
    
    trading_data = Trading.query.all()
    #user_inventory = Inventory.query.filter_by(user_id=current_user.user_id).first()
    #user_pokemon = user_inventory.pokemon_items
    
    all_pokemon = Pokemon.query.all()
    # Pass the form object to the template along with other data
    #return render_template('trading.html', trading_data=trading_data, user_pokemon = user_pokemon, all_pokemon = all_pokemon)
    return render_template('trading.html', trading_data=trading_data, all_pokemon = all_pokemon)

@app.route('/profile')
def profile():
    return render_template('profile/profileManagement.html')

@app.route('/inventory')
def inventory():
    return render_template('profile/inventory.html')
