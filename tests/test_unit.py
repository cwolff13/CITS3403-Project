from unittest import TestCase

from flask import Flask
from app import create_app, db
from app.config import TestConfig
from app.models import User, Pokemon, Inventory
from app.routes import *

class BasicUnitTests(TestCase):

    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        self.client = testApp.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup(self):
        response = self.client.post('/signup', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }, follow_redirects=False)

        new_user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(new_user)
        self.assertTrue(new_user.check_password('newpassword'))
        
    def test_login(self):
        user = User(user_id = 1,username='testuser', email='test@example.com', pokeballs=5)
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            }, follow_redirects=True)

        self.assertIn('Inventory', response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        

    def test_catching_pokemon(self):

        user = User(user_id = 2,username='pokehunter', email='hunter@example.com', pokeballs=1)
        user.set_password('secure')
        db.session.add(user)
        db.session.add(Inventory(owner=user))
        db.session.commit()

        self.client.post('/login', data={
            'username': 'pokehunter',
            'password': 'secure'
        }, follow_redirects=True)

        response = self.client.post('/catching-pokemon', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        inventory = Inventory.query.filter_by(owner=user).first()
        self.assertIsNotNone(inventory)
        i = 0 
        for pokemon in inventory.pokemon_items:
            i = i + 1
        self.assertEqual(i,1)
      
    def test_pokemon_search_function(self):
        user = User(user_id = 3, username="Gymleader",password_hash="ben10",email = "pokefan@gym.com",pokeballs = 10)
        db.session.add(user)
        db.session.add(Inventory(owner=user))
        inventory = Inventory.query.filter_by(owner=user).first()
        inventory.add_pokemon(1)
        db.session.commit() 

        for pokemon in inventory.pokemon_items:
            self.assertEqual(pokemon.id,1)
            self.assertEqual(pokemon.name, "Bulbasaur")
            self.assertEqual(pokemon.poke_url,"images/pokemonImages/Bulbasaur.jpg")
