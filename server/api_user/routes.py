from server.api_user import bp
from flask import request, jsonify
from server.api_user.controllers import (register_user, 
                                        confirm_user, 
                                        login,
                                        logout,
                                        upgrade)
from itsdangerous import SignatureExpired
from flask_jwt_extended import jwt_required

from server.models import User
from server import db


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

@bp.route('/user/login', methods=['POST'])
def user_login():
    if request.is_json:
        data = request.get_json()
        token = login(data)

        return jsonify({'message' : token})

@bp.route('/user/logout', methods=['PUT'])
@jwt_required()
def user_logout():
    encoded_token = request.headers.get('Authorization')
    result = logout(encoded_token)

    return jsonify({'message' : result})

@bp.route('/user/upgrade/<username>', methods=['PATCH'])
@jwt_required()
def upgrade_user(username):
    data = request.get_json()

    upgrade(username, data["user_type"])
    return jsonify({'message' : "successful upgrade"})