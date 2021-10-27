from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from server.extensions import db, migrate, mail
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
mail.init_app(app)
sk = URLSafeTimedSerializer(app.secret_key)
email = Config.MAIL_MAIL


from server.api_user import bp as api_user_bp
app.register_blueprint(api_user_bp)



from server import models