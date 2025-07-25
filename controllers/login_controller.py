from flask import Blueprint, request, jsonify
from services.login_service import login_user
from flask_cors import cross_origin

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/api/login', methods=['POST'])
def login():
    form = request.form  # 如果是 multipart/form-data 请求
    user = {
        "username": form.get("username", ""),
        "password": form.get("password", ""),
        "code": form.get("code", "")
    }

    try:
        cookies, totalCount, brand_id, status = login_user(user)
        if status == 200:
            return jsonify({
                "status": status,
                "data": {
                    "cookies": cookies,
                    "totalCount": totalCount,
                    "brand_id": brand_id
                },
                "error": ""
            })
        else:
            return jsonify({
                "status": status,
                "data": "",
                "error": cookies
            })
    except Exception as e:
        return jsonify({
            "status": 500,
            "data": "",
            "error": str(e)
        })
