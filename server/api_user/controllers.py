from flask import abort, current_app
from server.models import User
from server import db
from sqlalchemy import exc


def register_user(user_info):
    keys = list(user_info.keys())

    if 'username' not in keys or 'password' not in keys:
        abort(400, 'Invalid request')
    
    if user_info['password'] != user_info['comfirm_password']:
        abort(400, 'Passwords does not match')
    
    new_user = User(
        username=user_info['username'],
        name=user_info['name'],
        surname=user_info['surname'],
        email=user_info['email'],
        user_type=user_info['user_type']
    )
    new_user.set_password(user_info['password'])

    try:
        db.session.add(new_user)
        db.session.commit()
    except exc.IntegrityError:
        abort(400, 'User already exists')
    except exc.SQLAlchemyError:
        abort(500, 'Internal server error')

    return new_user