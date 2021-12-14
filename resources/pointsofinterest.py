from flask_login.utils import login_required
import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

from flask_login import current_user

favoriteplaces = Blueprint('pointsofinterest', 'pointsofinterest')

from amadeus import Client, ResponseError

amadeus = Client(
    client_id='M3RJq3uoqlOZYlK0g9Eau2AVrvCwuXgx',
    client_secret='aVf293vaVRV4aHDK'
)

try:
    '''
    What are the popular places in Barcelona (based on a geo location and a radius)
    '''
    response = amadeus.reference_data.locations.points_of_interest.get(latitude=41.397158, longitude=2.160873)
    print(response.data)
except ResponseError as error:
    raise error