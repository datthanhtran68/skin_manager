from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required
from bson.objectid import ObjectId
from utils.validators import is_valid_url

skins_bp = Blueprint('skins', __name__)

@skins_bp.route('/games/<game_id>/skins', methods=['POST'])
@login_required
def add_skin(game_id):
    try:
        data = request.json
        skin_name = data.get('name')
        rarity = data.get('rarity')
        price = data.get('price')
        image = data.get('image')

        if not skin_name or not rarity or not price or not image:
            return jsonify({"error": "Thiếu thông tin bắt buộc"}), 400
        if not is_valid_url(image):
            return jsonify({"error": "URL hình ảnh không hợp lệ"}), 400

        skin = {
            "_id": ObjectId(),
            "game_id": ObjectId(game_id),
            "name": skin_name,
            "rarity": rarity,
            "price": int(price),
            "image": image
        }
        current_app.config['skins_collection'].insert_one(skin)
        return jsonify({
            "_id": str(skin['_id']),
            "game_id": game_id,
            "name": skin_name,
            "rarity": rarity,
            "price": price,
            "image": image
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@skins_bp.route('/games/<game_id>/skins/<skin_id>', methods=['PUT'])
@login_required
def update_skin(game_id, skin_id):
    data = request.json
    skin_name = data.get('name')
    rarity = data.get('rarity')
    price = data.get('price')
    image = data.get('image')
    if not skin_name or not rarity or not price or not image:
        return jsonify({"error": "Thiếu thông tin bắt buộc"}), 400
    if not is_valid_url(image):
        return jsonify({"error": "URL hình ảnh không hợp lệ"}), 400

    result = current_app.config['skins_collection'].update_one(
        {"_id": ObjectId(skin_id), "game_id": ObjectId(game_id)},
        {"$set": {
            "name": skin_name,
            "rarity": rarity,
            "price": int(price),
            "image": image
        }}
    )
    if result.matched_count:
        return jsonify({
            "_id": skin_id,
            "game_id": game_id,
            "name": skin_name,
            "rarity": rarity,
            "price": price,
            "image": image
        })
    return jsonify({"error": "Không tìm thấy skin hoặc game"}), 404

@skins_bp.route('/games/<game_id>/skins/<skin_id>', methods=['DELETE'])
@login_required
def delete_skin(game_id, skin_id):
    result = current_app.config['skins_collection'].delete_one({"_id": ObjectId(skin_id), "game_id": ObjectId(game_id)})
    if result.deleted_count:
        return jsonify({"message": "Skin đã được xóa"})
    return jsonify({"error": "Không tìm thấy skin hoặc game"}), 404