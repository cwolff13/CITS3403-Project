
from typing import Optional, List
import os
import sqlalchemy as sa
import sqlalchemy.orm as so
from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class Pokemon(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), index=True, nullable=False)
    poke_url: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)

    def __repr__(self):
        return f'<Pokemon {self.name}>'
    
    def populate_database():
        dirname = os.path.dirname(__file__) #Gets current directory
        file_path = os.path.join(dirname, 'pokemonlist.txt')# Appends relative file to locate Pokemon list. 
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                # Assuming the file has no header and each line is id,name,image_url
                for line in file:
                    # Sort data from pokemon list file. 
                    id, name, poke_url = line.strip().split(',')
                    
                    # Convert id to interger
                    id = int(id)
                    
                    # Check if the Pokemon already exists to prevent duplicates
                    if not Pokemon.query.get(id):
                        new_pokemon = Pokemon(id=id, name=name, poke_url=poke_url)
                        db.session.add(new_pokemon)
                
                # Commit all new entries to the database
                db.session.commit()
        #Error handling, prints error message to terminal. DOES NOT TERMINATE CREATION OF DB. WILL STILL CREATE EMPTY TABLE!!!
        except FileNotFoundError:
            print("Error: The file was not found at" + " " + file_path) 
        except ValueError as e:
            print(f"Error parsing data: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")      

class Trading(db.Model): 
        id:int = db.Column(db.Integer, primary_key=True, autoincrement=True) 
        user_name:str = db.Column(db.String(100), unique=False)

        '''
        Takes a pokemon object represented as the pokemon's ID.
        Important to note! 
        - pokemon_trade_in_id is an integer that is referencing a Pokemon entry in the database.

        - pokemon_trade_in is a relational map to the Pokemon object.
        Therefore it can be used like trading_instance.pokemon_trade_in.name to get the pokemon's name without a separate query
        '''
        pokemon_trade_in_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False, unique=False) 
        pokemon_trade_out_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False, unique=False)
        
        #Defines the relationship to Pokemon table
        pokemon_trade_in = db.relationship('Pokemon', foreign_keys=[pokemon_trade_in_id])
        pokemon_trade_out = db.relationship('Pokemon', foreign_keys=[pokemon_trade_out_id])

        def __repr__(self):
                return f'<{self.user_name} {self.pokemon_trade_in.name} {self.pokemon_trade_out.name}>'
        
        # Adding new trade function 
        @classmethod
        def add_trade(cls, user_name, pokemon_trade_in_id, pokemon_trade_out_id):
            new_trade = cls(user_name=user_name, pokemon_trade_in_id=pokemon_trade_in_id, pokemon_trade_out_id=pokemon_trade_out_id)
            db.session.add(new_trade)   
            db.session.commit() 
        
        # Finding pokemon object via its ID    
        @classmethod
        def find_pokemon_id(cls, pokemon_name):
            pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
            if pokemon:
                return pokemon.id
            else:
                return None
        
        # Deleting existed trade function
        @classmethod
        def delete_trade(cls, trade_id):
            trade = cls.query.get(trade_id)
            if trade:
                db.session.delete(trade)
                db.session.commit()

inventory_pokemon_association = db.Table('inventory_pokemon',
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.inventory_id'), primary_key=True), 
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'), primary_key=True), 
    db.Column('quantity', db.Integer, default=1)  # quantinty of each pokemon, can have mutliple copies. 
)

class Inventory(db.Model):
    __tablename__ = 'inventory'

    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # ForeignKey to User table

    # Relationship back to the User table (many-to-one)
    owner = db.relationship('User', back_populates='inventory_items')

    # Relationship to manage inventory items through association table
    pokemon_items = db.relationship('Pokemon', secondary=inventory_pokemon_association, backref='inventories', lazy='dynamic')

    def __repr__(self):
        return f"<Inventory(inventory_id={self.inventory_id}, user_id={self.user_id})"   

    def add_pokemon(self, pokemon_id: int):
        # Direct SQL statement to increment quantity or insert a new row if not exists
        existing_association = db.session.execute(
            sa.select(inventory_pokemon_association).where(
                inventory_pokemon_association.c.inventory_id == self.inventory_id,
                inventory_pokemon_association.c.pokemon_id == pokemon_id
            )
        ).fetchone()
        if existing_association:
            # If the Pokémon is already in the inventory, increment the quantity
            db.session.execute(
                inventory_pokemon_association.update().where(
                    inventory_pokemon_association.c.inventory_id == self.inventory_id,
                    inventory_pokemon_association.c.pokemon_id == pokemon_id
                ).values(quantity=inventory_pokemon_association.c.quantity + 1)
            )
        else:
            # If not present, add a new entry to the association table
            db.session.execute(
                inventory_pokemon_association.insert().values(
                    inventory_id=self.inventory_id,
                    pokemon_id=pokemon_id,
                    quantity=1
                )
            )
        db.session.commit()

    def remove_pokemon(self, pokemon_id: int):
        try:
            existing_association = db.session.execute(
            sa.select(inventory_pokemon_association).where(
                inventory_pokemon_association.c.inventory_id == self.inventory_id,
                inventory_pokemon_association.c.pokemon_id == pokemon_id
            )
            ).fetchone()
            if existing_association:
                current_quantity = existing_association[2]
                print(f"Successfully fetched. Current quantity: {current_quantity}")
                if current_quantity > 1:
                    db.session.execute(
                        inventory_pokemon_association.update().where(
                            sa.and_(
                                inventory_pokemon_association.c.inventory_id == self.inventory_id,
                                inventory_pokemon_association.c.pokemon_id == pokemon_id
                            )
                        ).values(quantity=current_quantity - 1)
                    )
                elif current_quantity == 1:
                    db.session.execute(
                        sa.delete(inventory_pokemon_association).where(
                            sa.and_(
                                inventory_pokemon_association.c.inventory_id == self.inventory_id,
                                inventory_pokemon_association.c.pokemon_id == pokemon_id
                            )
                        )
                    )
                db.session.commit()
        except Exception as e:
            print(f"Error during fetch: {e}")
    
    def get_pokemon_quantity(self, pokemon_id: int) -> int:
        association = db.session.query(inventory_pokemon_association).filter_by(inventory_id=self.inventory_id, pokemon_id=pokemon_id).first()
        if association:
            return association.quantity
        return 0
    
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    pokeballs = db.Column(db.Integer)

    inventory_items = db.relationship('Inventory', back_populates='owner', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username={self.username}, email={self.email}, pokeballs = {self.pokeballs})>"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # helper function to allow flask login to get the user ID
    def get_id(self):
        return str(self.user_id)

    def deduct_pokeball(self):
        if self.pokeballs > 0:
            self.pokeballs -= 1
            db.session.commit()
            return True
        return False   
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


def initialise_database(): 
    if not os.path.exists('app.db'): #Checks to see if the database already exsists, Only runs if the database hasn't already been created. 
        db.create_all() 
        Pokemon.populate_database()
    
    # Create user inventories to test possible trading functionality scenarios.
    # Create 2 user with the same name below and uncomment these lines to add pokemon to user's inventory
    
    # user1 = User.query.filter_by(username="long").first()

    # inventory1 = Inventory(owner=user1)
    # db.session.add(inventory1)
    # db.session.commit()
    
    # inventory1 = Inventory.query.filter_by(user_id=1).first()
    # inventory1.add_pokemon(1)
    # inventory1.add_pokemon(1)
    # inventory1.add_pokemon(2)
    # inventory1.add_pokemon(3)
    # inventory1.add_pokemon(4)
    # inventory1.add_pokemon(5)

    # db.session.commit() 

    # user2 = User.query.filter_by(username="kaoma").first()
    # db.session.add(user2)    
    # db.session.commit()

    # inventory2 = Inventory(owner=user2)
    # db.session.add(inventory2)
    # db.session.commit()
    
    # inventory2 = Inventory.query.filter_by(user_id=2).first()
    # inventory2.add_pokemon(5)
    # inventory2.add_pokemon(6)
    # inventory2.add_pokemon(7)
    # inventory2.add_pokemon(8)

    # db.session.commit()