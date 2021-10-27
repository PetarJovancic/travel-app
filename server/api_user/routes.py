from server.api_user import bp
from flask import request, jsonify
from server.api_user.controllers import register_user, confirm_user
from itsdangerous import SignatureExpired


@bp.route('/user/register', methods=['POST'])
def add_new_user():
    if request.is_json:
        data = request.get_json()
        result = register_user(data)

    return jsonify({'message' : 'New user created!'})

@bp.route('/confirm_email/<username>/<token>')
def confirm_email(token, username):
    try:
        confirm_user(token, username)
    except SignatureExpired:
        return jsonify({'message' : 'Token has expired!'})

    return jsonify({'message' : 'User is verified!'})