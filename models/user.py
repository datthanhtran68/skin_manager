from flask_login import UserMixin
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

def load_user(user_id):
    from app import app
    user = app.config['users_collection'].find_one({"_id": ObjectId(user_id)})
    if user:
        return User(str(user['_id']), user['username'])
    return None