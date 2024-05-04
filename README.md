# CITS3403-Project

## Team Members
| UWA ID    | Name           | GitHub Username   |
|-----------|----------------|-------------------|
| 23186998 | Carson Wolff | @cwolff13 |
| 23757264 | Duc Long Tran| @longtrann |
| 23169267  | Kaoma Kabange | @kaomakabange |
| 22716417 | Ryan Lam | @RyanZhiLam |

## Project Description
**TODO**
A description of the purpose of the application, explaining the its design and use.

## Architecture
**TODO**
A brief summary of the architecture of the application.

## Launch
To launch this Flask application, follow these steps:

1. **Set up your environment**:
   - Ensure Python is installed on your system.
   - Optionally, activate a virtual environment to manage dependencies:
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

4. **Run the application**:
   - Start the Flask server:
     ```bash
     flask run
     ```
   - Access the application via `http://127.0.0.1:5000/` in your web browser.

## Tests
**TODO**
Instructions for how to run the tests for the application.
