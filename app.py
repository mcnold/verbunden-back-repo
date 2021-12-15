from flask import Flask, jsonify, after_this_request
import flask

from resources.favoriteplaces import favoriteplaces
from resources.users import users

import models

from flask_cors import CORS

from flask_login import LoginManager
import os

DEBUG=True
PORT=8000
app = Flask(__name__)
app.secret_key = "LEFFERINA"

app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(user_id)
    except models.DoesNotExist:
        return None 

CORS(favoriteplaces, origins=['http://localhost:3000'], supports_credentials=True)  
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(favoriteplaces, url_prefix='/favoriteplaces')
app.register_blueprint(users, url_prefix='/users')

# we don't want to hog up the SQL connection pool
# so we should connect to the DB before every request
# and close the db connection after every request

@app.before_request # use this decorator to cause a function to run before reqs
def before_request():

    """Connect to the db before each request"""
    print("you should see this before each request") # optional -- to illustrate that this code runs before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
    models.DATABASE.connect()

    @after_this_request # use this decorator to Executes a function after this request
    def after_request(response):
        """Close the db connetion after each request"""
        print("you should see this after each request") # optional -- to illustrate that this code runs after each request
        models.DATABASE.close()
        return response # go ahead and send response back to client
                      # (in our case this will be some JSON)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    # when we start the app, set up our DB/tables as defined in models.py
    models.initialize() # remember in express we required db before we did app.listen
    app.run(debug=DEBUG, port=PORT)
    
# ADD THESE THREE LINES -- because we need to initialize the
# tables in production too!
if os.environ.get('FLASK_ENV') != 'development':
  print('\non heroku!')
  models.initialize()
