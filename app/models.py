"""
Module containing model structure for all database tables. You can add your database code below.
"""

from typing import Optional
import os
import sqlalchemy as sa
import sqlalchemy.orm as so
from .db import db

class Pokemon(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), index=True, nullable=False)
    poke_url: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False)

    def __repr__(self):
        return f'<Pokemon {self.name}>'
    
    def initialise_database(): # Need to rewrite to instead check integrity of database rather than exsistence.
        if not os.path.exists('app.db'): #Checks to see if the database already exsists, Only runs if the database hasn't already been created. 
            db.create_all() #May need to adjust depending on format of other databases.
            Pokemon.populate_database()

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