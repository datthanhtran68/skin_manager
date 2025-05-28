from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required
from bson.objectid import ObjectId

games_bp = Blueprint('games', __name__)

@games_bp.route('/games', methods=['POST'])
@login_required
def add_game():
    data = request.json
    game_name = data.get('name')
    genre = data.get('genre')
    release_year = data.get('release_year')
    if not game_name or not genre or not release_year:
        return jsonify({"error": "Tên game, thể loại và năm phát hành là bắt buộc"}), 400
    game = {"_id": ObjectId(), "name": game_name, "genre": genre, "release_year": release_year}
    current_app.config['games_collection'].insert_one(game)
    return jsonify({"_id": str(game['_id']), "name": game_name, "genre": genre, "release_year": release_year}), 201

@games_bp.route('/games/<game_id>', methods=['PUT'])
@login_required
def update_game(game_id):
    data = request.json
    game_name = data.get('name')
    genre = data.get('genre')
    release_year = data.get('release_year')
    if not game_name or not genre or not release_year:
        return jsonify({"error": "Tên game, thể loại và năm phát hành là bắt buộc"}), 400
    result = current_app.config['games_collection'].update_one(
        {"_id": ObjectId(game_id)},
        {"$set": {"name": game_name, "genre": genre, "release_year": release_year}}
    )
    if result.matched_count:
        return jsonify({"_id": game_id, "name": game_name, "genre": genre, "release_year": release_year})
    return jsonify({"error": "Game not found"}), 404

@games_bp.route('/games/<game_id>', methods=['DELETE'])
@login_required
def delete_game(game_id):
    result = current_app.config['games_collection'].delete_one({"_id": ObjectId(game_id)})
    if result.deleted_count:
        current_app.config['skins_collection'].delete_many({"game_id": ObjectId(game_id)})
        return jsonify({"message": "Game and related skins deleted"})
    return jsonify({"error": "Game not found"}), 404