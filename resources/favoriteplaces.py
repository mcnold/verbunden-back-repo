from flask_login.utils import login_required
import models


from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

from flask_login import current_user

favoriteplaces = Blueprint('favoriteplaces', 'favoriteplaces')

@favoriteplaces.route('/', methods=['GET'])
@login_required
def favorites_index():
    favorite_dicts = [model_to_dict(favoriteplace) for favoriteplace in current_user.favoriteplaces]
    return jsonify({
        'data': favorite_dicts,
        'message': f"Successfully found {len(favorite_dicts)} places",
        'status': 200
    }), 200

@favoriteplaces.route('/', methods=['POST'])
def create_favoriteplace():
    payload = request.get_json()
    print(payload)
    new_place = models.Favorite.create(username=current_user, url=payload['url'], place=payload['place'], city=payload['city'], country=payload['country'], type=payload['type'], latitude=payload['latitude'], longitude=payload['longitude'])
    
    print(new_place) 
    
    place_dict = model_to_dict(new_place)
    return jsonify(
        data = place_dict,
        message = "Successfully created a new favorite place",
        status = 201
    ), 201
    
@favoriteplaces.route('/<id>', methods=['GET'])
def get_one_place(id):
    place = models.Favorite.get_by_id(id)
    print(place)
    return jsonify(
        data = model_to_dict(place),
        message = 'Success!',
        status = 200
    ), 200
    
@favoriteplaces.route('/<id>', methods=['PUT'])
def update_place(id):
    payload = request.get_json()
    models.Favorite.update(**payload).where(models.Favorite.id==id).execute()
    
    return jsonify(
        data = model_to_dict(models.Favorite.get_by_id(id)),
        message = 'Resource updated successfully',
        status = 200,
    ), 200
    
@favoriteplaces.route('/<id>', methods=['DELETE'])
def delete_place(id):
    delete_query = models.Favorite.delete().where(models.Favorite.id==id)
    nums_of_rows_deleted = delete_query.execute()
    print(nums_of_rows_deleted)
    
    return jsonify(
        data={},
        message=f"Successfully deleted {nums_of_rows_deleted} place with id {id}",
        status = 200
    ), 200