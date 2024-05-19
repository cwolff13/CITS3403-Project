# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from flask import url_for
# from app import create_app, db
# from app.models import User
# from app.config import TestConfig
 
 
 
# def test_sign_up(driver, base_url, app):
#     with app.app_context():
#         signup_url = url_for('main.signup', _external=True)
#         print(f"Generated signup URL: {signup_url}")
#         driver.get(signup_url)
       
#         # Use explicit waits to locate elements
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.ID, "UWA"))
#         ).send_keys("selenium_user")
       
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.ID, "UWA1"))
#         ).send_keys("selenium_user@example.com")
       
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.ID, "UWA2"))
#         ).send_keys("selenium_password")
       
#         WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.ID, "UWA3"))
#         ).click()
 
 
   
# # def test_login(driver, base_url):
# #     driver.get(base_url + url_for('main.login'))
# #     driver.find_element(By.NAME, "username").send_keys("selenium_user")
# #     driver.find_element(By.NAME, "password").send_keys("selenium_password")
# #     driver.find_element(By.NAME, "submit").click()
 
# # def test_logout(driver, base_url):
# #     driver.get(base_url + url_for('main.logout'))
 
# # def test_update_password(driver, base_url):
# #     driver.get(base_url + url_for('main.profile'))
# #     driver.find_element(By.NAME, "password").send_keys("selenium_password")
# #     driver.find_element(By.NAME, "confirm_password").send_keys("new_selenium_password")
# #     driver.find_element(By.NAME, "submit").click()
 
# # def test_catch_pokemon(driver, base_url):
# #     driver.get(base_url + url_for('main.catching'))
# #     driver.find_element(By.ID, "pokeball").click()
 
# # def test_inventory(driver, base_url):
# #     driver.get(base_url + url_for('main.inventory'))
 
# # def test_trade_pokemon(driver, base_url):
# #     driver.get(base_url + url_for('main.trading'))
 
# class PokemonTradingAppSeleniumTest(unittest.TestCase):
 
#     @classmethod
#     def setUpClass(cls):
#         cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
#         cls.base_url = "http://localhost:5000"
 
#     def setUp(self):
#         self.app = create_app(TestConfig)
#         self.app.config['SERVER_NAME'] = 'localhost:5000'
#         self.app.config['APPLICATION_ROOT'] = '/'
#         self.app.config['PREFERRED_URL_SCHEME'] = 'http'
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()
 
#         user = User(username='selenium_user', email='selenium_user@example.com')
#         user.set_password('selenium_password')
#         db.session.add(user)
#         db.session.commit()
 
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()
 
#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()
 
#     def test_sign_up(self):
#         test_sign_up(self.driver, self.base_url ,self.app)
 
#     # def test_login(self):
#     #     test_login(self.driver, self.base_url)
 
#     # def test_logout(self):
#     #     test_logout(self.driver, self.base_url)
 
#     # def test_update_password(self):
#     #     test_update_password(self.driver, self.base_url)
 
#     # def test_catch_pokemon(self):
#     #     test_catch_pokemon(self.driver, self.base_url)
 
#     # def test_inventory(self):
#     #     test_inventory(self.driver, self.base_url)
 
#     # def test_trade_pokemon(self):
#     #     test_trade_pokemon(self.driver, self.base_url)
 
# if __name__ == "__main__":
#     unittest.main()