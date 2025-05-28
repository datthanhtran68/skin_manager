from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from routes.auth import auth_bp
from routes.games import games_bp
from routes.skins import skins_bp
from models.user import load_user

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'  # Thay bằng key an toàn trong production

# Kết nối MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['skin_manager']
app.config['games_collection'] = db['games']
app.config['skins_collection'] = db['skins']
app.config['users_collection'] = db['users']

# Cấu hình Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.index'
login_manager.user_loader(load_user)

# Đăng ký blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(games_bp, url_prefix='/api')
app.register_blueprint(skins_bp, url_prefix='/api')

if __name__ == '__main__':
    print("🔥 Flask app is rolling like VinFast...")
    app.run(debug=True)