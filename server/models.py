from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
import uuid

from server import db
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4,
                   unique=True,
                   nullable=False)
    username = db.Column(db.String(255),
                         unique=True,
                         index=True,
                         nullable=False)
    password = db.Column(db.String(255), nullable=False)
    comfirm_password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return f'<User {self.id} {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)
        self.comfirm_password = self.password

    def check_password(self, password):
        return check_password_hash(self.password, password)