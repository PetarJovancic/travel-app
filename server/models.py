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
    is_validated = db.Column(db.Boolean())


    def __repr__(self):
        return f'<User {self.id} {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)
        self.comfirm_password = self.password

    def check_password(self, password):
        return check_password_hash(self.password, password)


class TokenBlacklist(db.Model):
    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4,
                   unique=True,
                   nullable=False)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'token_id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'expires': self.expires
        }
