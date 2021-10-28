from flask import abort, current_app
from flask.helpers import url_for
from server.models import User
from server import db, sk, email
from sqlalchemy import exc
from flask_mail import Message
from server import mail
from flask_jwt_extended import (create_access_token,
                                create_refresh_token, 
                                get_jwt_identity,
                                decode_token,)
from server.jwt.jwt_util import add_token_to_database, revoke_token

def send_email(username, email):
    token = sk.dumps(email, salt='email-confirm')

    msg = Message('Confirm Email', 
                    sender=email, 
                    recipients=[email])

    link = url_for('api_user.confirm_email', username=username , token=token, _external=True)

    msg.body = 'Your link is {}'.format(link)

    mail.send(msg)

def register_user(user_info):
    keys = list(user_info.keys())

    if 'username' not in keys or 'password' not in keys:
        abort(400, 'Invalid request')
    
    if user_info['password'] != user_info['comfirm_password']:
        abort(400, 'Password does not match')
    
    if db.session.query(User).filter(User.email == user_info['email']).first():
        abort(400, 'Email is already in use.')

    if user_info['user_type'] == "admin" or user_info[
        'user_type'] == "travel":
        send_email(user_info['username'], email)
    
    new_user = User(
        username=user_info['username'],
        name=user_info['name'],
        surname=user_info['surname'],
        email=user_info['email'],
        user_type=user_info['user_type'],
        is_validated=False
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

def confirm_user(token, username):
    email = sk.loads(token, salt='email-confirm', max_age=86400)
    user = User.query.filter_by(username=username).first()
    user.is_validated = True
    db.session.commit()

    msg = Message('Confirmation Email', 
                    sender=email, 
                    recipients=[user.email])
    msg.body = 'Your account has been verifed'
    mail.send(msg)

def login(user_info):
    keys = list(user_info.keys())

    if 'username' not in keys or 'password' not in keys:
        abort(400, 'Invalid request')

    user = User.query.filter_by(username=user_info['username']).first()
    User.check_password

    if not user:
        abort(401, 'User does not exist')

    if not user.check_password(user_info['password']):
        abort(403, 'Invalid credentials')

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    add_token_to_database(
        access_token, current_app.config['JWT_IDENTITY_CLAIM'])
    add_token_to_database(
        refresh_token, current_app.config['JWT_IDENTITY_CLAIM'])

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

def logout(token_id):
    user_identity = get_jwt_identity()
    token_id = token_id.split(' ', 1)[1]
    jti = decode_token(token_id)['jti']

    try:
        revoke_token(jti, user_identity)
        return 'Logout successful'
    except:
        abort(404, 'Logout unsuccesful')

def upgrade(username, user_type):
    if db.session.query(User).filter(User.user_type == "travel").first():
        if user_type == "tourist":
            abort(400,
             'User with cannot type: Travel Guide cannot upgrade to Tourist type')
        user = User.query.filter_by(username=username).first()
        user.user_type = user_type
        db.session.commit()
        
        send_email(username, email)

    if db.session.query(User).filter(User.user_type == "tourist").first():
        user = User.query.filter_by(username=username).first()
        user.user_type = user_type
        db.session.commit()
    
        send_email(username, email)