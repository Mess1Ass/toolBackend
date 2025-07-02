from flask import Blueprint, request, jsonify
from models.user import User
from services.login_service import login_user

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/api/login', methods=['POST'])
def login():
    form = request.form
    user = User(
        username=form.get('username', '') or '',
        password=form.get('password', '') or '',
        code=form.get('code', '') or ''
    )

    try:
        result = login_user(user)
        print(result)
        return jsonify({'status': 200, 'data': result, 'error': ''})
    except Exception as e:
        return jsonify({'status': -1, 'data': '代理请求失败', 'error': str(e)})
