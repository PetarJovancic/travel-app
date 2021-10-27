import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = os.environ.get('SERVER_MAIL')
    MAIL_USERNAME = os.environ.get('USERNAME_MAIL')
    MAIL_MAIL = os.environ.get('MAIL_MAIL')
    MAIL_PASSWORD = os.environ.get('PASSWORD_MAIL')
    MAIL_PORT = os.environ.get('PORT_MAIL')
    MAIL_USE_SSL=True
    MAIL_USE_TLS=False