from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, current_user
from bson.objectid import ObjectId
from bson.regex import Regex
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    search_query = request.args.get('search', '').strip()
    games_collection = current_app.config['games_collection']
    skins_collection = current_app.config['skins_collection']

    if search_query:
        # Tìm kiếm game theo tên (không phân biệt hoa thường)
        games = list(games_collection.find({
            'name': {'$regex': Regex(search_query, 'i')}
        }))
        # Tìm kiếm skin theo tên (không phân biệt hoa thường)
        skins = list(skins_collection.find({
            'name': {'$regex': Regex(search_query, 'i')}
        }))
        # Gộp skin vào game tương ứng cho kết quả tìm kiếm
        for game in games:
            game['skins'] = [skin for skin in skins if str(skin['game_id']) == str(game['_id'])]
        # Thêm thông tin game_name cho skin tìm được
        for skin in skins:
            game = games_collection.find_one({'_id': skin['game_id']})
            skin['game_name'] = game['name'] if game else None
        # Trả về kết quả tìm kiếm
        search_results = {'games': games, 'skins': skins}
        return render_template(
            'index.html',
            search_query=search_query,
            search_results=search_results,
            is_authenticated=current_user.is_authenticated,
            current_user=current_user,
            register_success=request.args.get('register_success', False, type=bool),
            games=[],  # Không hiển thị danh sách game mặc định
            skins=[]   # Không hiển thị danh sách skin mặc định
        )
    else:
        # Giao diện mặc định
        games = list(games_collection.find())
        skins = list(skins_collection.find())
        # Gộp skin vào game tương ứng
        for game in games:
            game['skins'] = [skin for skin in skins if str(skin['game_id']) == str(game['_id'])]
        return render_template(
            'index.html',
            games=games,
            skins=skins,
            is_authenticated=current_user.is_authenticated,
            current_user=current_user,
            register_success=request.args.get('register_success', False, type=bool),
            search_query='',
            search_results=None
        )

@auth_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    username = request.form.get('username')
    password = request.form.get('password').encode('utf-8')
    user = current_app.config['users_collection'].find_one({"username": username})
    if user and bcrypt.checkpw(password, user['password']):
        from models.user import User
        user_obj = User(str(user['_id']), user['username'])
        login_user(user_obj)
        flash('Đăng nhập thành công!', 'success')
        return redirect(url_for('auth.index'))
    flash('Tên người dùng hoặc mật khẩu không đúng.', 'error')
    return redirect(url_for('auth.index'))

@auth_bp.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    username = request.form.get('username')
    password = request.form.get('password').encode('utf-8')
    if not username or not password:
        flash('Vui lòng nhập đầy đủ thông tin.', 'error')
        return redirect(url_for('auth.index'))
    if current_app.config['users_collection'].find_one({"username": username}):
        flash('Tên người dùng đã tồn tại.', 'error')
        return redirect(url_for('auth.index'))
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    try:
        current_app.config['users_collection'].insert_one({
            '_id': ObjectId(),
            'username': username,
            'password': hashed_password
        })
        flash('Đăng ký thành công!', 'success')
        return redirect(url_for('auth.index', register_success=True))
    except Exception as e:
        flash('Lỗi hệ thống, vui lòng thử lại.', 'error')
        return redirect(url_for('auth.index'))

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Đã đăng xuất.', 'success')
    return redirect(url_for('auth.index'))