from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from server.extensions import db, migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)


from server.api_user import bp as api_user_bp
app.register_blueprint(api_user_bp)



from server import models