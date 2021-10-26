from server.api_user import bp
from flask import request, jsonify
from server.api_user.controllers import register_user

@bp.route('/user/register', methods=['POST'])
def add_new_user():
    if request.is_json:
        data = request.get_json()
        result = register_user(data)

    return jsonify({'message' : 'New user created!'})