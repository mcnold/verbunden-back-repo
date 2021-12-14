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

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    # when we start the app, set up our DB/tables as defined in models.py
    models.initialize() # remember in express we required db before we did app.listen
    app.run(debug=DEBUG, port=PORT)
