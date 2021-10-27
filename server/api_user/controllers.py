from flask import abort
from flask.helpers import url_for
from server.models import User
from server import db, sk, email
from sqlalchemy import exc
from flask_mail import Message
from server import mail


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
