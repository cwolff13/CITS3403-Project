# CITS3403-Project - PokeTrade

## Team Members
| UWA ID    | Name           | GitHub Username   |
|-----------|----------------|-------------------|
| 23186998 | Carson Wolff | @cwolff13 |
| 23757264 | Duc Long Tran| @longtrann |
| 23169267  | Kaoma Kabange | @kaomakabange |
| 22716417 | Ryan Lam | @RyanZhiLam |

## Project Description
**PokeTrade** is a marketplace platform that allows users to catch and trade the first generation of Pokemon Characters.
After logging in and catching their first Pokemon, users can navigate to place trade requests.

**How Trading Works:**
Trades are made by placing a request for a specific Pokemon the user does not have, while offering one of their own Pokemon from their personal inventory.  A pokemon in a user's inventory can be posted on multiple trade posts. Trade occurs when a user has a pokemon that the post owner wants and trades on the trade post. Then the corresponding pokemon in the trade post will go to the corresponding inventory user. If a pokemon is not available for trading in the user's inventory, previous trade posts containing that pokemon will be deleted. 
Users cannot trade with themselves. User cannot trade if they don't have the pokemon post owner want to have.

## Architecture
PokeTrade is a Flask web application structured to promote modularity and maintainability. The main components of the application include:

1. **Flask Application**:
   - The core of PokeTrade, responsible for handling web requests, managing sessions, and rendering templates. `/app` contains the essential components of the PokeTrade product. 

2. **Database**:
   - A SQLite database (`app.db`) that stores User information, Pokemon inventory, and Trade requests. SQLAlchemy is used as the ORM for database interactions.

3. **User Authentication**:
   - Managed using Flask-Login, allowing users to register, log in, and manage their sessions securely.

4. **HTML Templates**:
   - HTML web page templates stored in `app/templates`, which provide interfaces for users to interact with PokeTrade.

5. **Static Files**:
   - CSS, JavaScript and Image files stored in the `app/static/` directory. These pages add styling and functionality to the aforementioned HTML templates. 

6. **Routes**:
   - Defined in `app/routes.py`, handling different URL endpoints and associating them with specific functions to process requests and return responses. Renders the HTML Pages. 

7. **Forms**:
   - Defined in `app/form.py`, managing user input and validation for various forms in the application.

8. **Models**:
   - Defined in `app/models.py`, representing the data structures of the application and the database schema.

9. **Configuration**:
   - Application configuration settings are managed in `app/config.py` and environment-specific settings in `env.py`.

10. **Database Migrations**:
    - Managed using Alembic, with migration scripts and configuration files located in the `migrations/` directory.

## Launch
To launch this Flask application, follow these steps:

1. **Set up your environment**:
   - Ensure Python is installed on your system.
   - Optionally, activate a virtual environment to best manage dependencies:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```

2. **Install dependencies**:
   - Install all required packages from the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

3. **Set environment variables**:
   - Specify the environment and debug mode:
     ```bash
     export FLASK_APP=app.py      # On Windows use `set FLASK_APP=app.py`
     export FLASK_ENV=development # On Windows use `set FLASK_ENV=development`
     export FLASK_DEBUG=1         # On Windows use `set FLASK_DEBUG=1`
     ```

4. **Change Directory into the main App**
      ```bash
      cd app
      ```

5. **Run the application**:
   - Start the Flask server:
     ```bash
     flask run
     ```
   - Access the application via `http://127.0.0.1:5000/` in your web browser.

## Tests
   **Unit Tests:**
   ```Python
   python -m unittest discover [options]

   ```

   **Selenium Tests:**
   Instructions for how to run the Selenium tests TODO.
