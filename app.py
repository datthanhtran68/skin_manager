import os
from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from routes.auth import auth_bp
from routes.games import games_bp
from routes.skins import skins_bp
from models.user import load_user
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'

# Sửa ở đây
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)

db = client['skin_manager']
app.config['games_collection'] = db['games']
app.config['skins_collection'] = db['skins']
app.config['users_collection'] = db['users']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.index'
login_manager.user_loader(load_user)

app.register_blueprint(auth_bp)
app.register_blueprint(games_bp, url_prefix='/api')
app.register_blueprint(skins_bp, url_prefix='/api')

if __name__ == "__main__":
<<<<<<< HEAD
    port = int(os.environ.get("PORT", 5000))  # Render sẽ set biến PORT
    app.run(host="0.0.0.0", port=port)
=======
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
>>>>>>> 39f6686a873da61a2163480fe10de7c2b0c5ec26
