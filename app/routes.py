from flask import request, url_for, jsonify
from app.forms import TradingForm
from flask import render_template, redirect
from app import app
from app.models import Inventory, Pokemon, Trading, User

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/catching')
def catching():
    return render_template('catching.html')

@app.route('/trading', methods=['GET', 'POST', 'DELETE'])
def trading():
    current_user = User.query.filter_by(username="dvLong").first()
    trading_data = Trading.query.all()
    current_user_inventory = Inventory.query.filter_by(user_id=current_user.user_id).first()
    current_user_pokemon = current_user_inventory.pokemon_items
    
    all_pokemon = Pokemon.query.all()
    if not current_user:
        return "User not found", 404
    
    if request.method == 'POST':
        # Retrieve the Pokémon names from the form data
        pokemon_to_receive_name = request.form['pokemon_to_receive']
        pokemon_to_trade_out_name = request.form['pokemon_to_trade_out']
        
        # Find the IDs of the Pokémon
        pokemon_to_receive_id = Trading.find_pokemon_id(pokemon_to_receive_name)
        pokemon_to_trade_out_id = Trading.find_pokemon_id(pokemon_to_trade_out_name)
        
        if pokemon_to_receive_id and pokemon_to_trade_out_id:
            # Add the trade using the IDs
            Trading.add_trade(user_name= current_user.username, 
                              pokemon_trade_in_id=pokemon_to_receive_id, 
                              pokemon_trade_out_id=pokemon_to_trade_out_id)
            # Optionally, you can redirect or render a new template after adding the trade
            return redirect(location=url_for("trading"))
    elif request.method == 'DELETE':
        trade_id = request.args.get('trade_id')
        
        trade = Trading.query.get(trade_id)
        
        user = User.query.filter_by(username = trade.user_name).first()
        
        user_inventory = Inventory.query.filter_by(user_id=user.user_id).first()
        
        pokemon_trade_in = trade.pokemon_trade_in_id
        
        pokemon_trade_out = trade.pokemon_trade_out_id
        
        user_inventory.add_pokemon(pokemon_trade_in)
        
        current_user_inventory.remove_pokemon(pokemon_trade_in)   
        
        current_user_inventory.add_pokemon(pokemon_trade_out)
        
        user_inventory.remove_pokemon(pokemon_trade_out)
        
        Trading.delete_trade(trade_id)
        
        return redirect(location=url_for("trading"))
    else:
        
        
        for trade in trading_data:
            print(f"Trade ID: {trade.id}, User Name: {trade.user_name}, Trade In ID: {trade.pokemon_trade_in_id}, Trade Out ID: {trade.pokemon_trade_out_id}")
        
        for pokemon in current_user_pokemon:
            print(f"pokemon ID: {pokemon.id}")
        # Pass the form object to the template along with other data
        return render_template('trading.html', trading_data=trading_data, current_user_pokemon = current_user_pokemon, all_pokemon = all_pokemon, Pokemon = Pokemon)
    
@app.route('/profile')
def profile():
    return render_template('profile/profileManagement.html')

@app.route('/inventory')
def inventory():
    return render_template('profile/inventory.html')
