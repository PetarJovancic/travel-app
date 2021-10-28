from flask_jwt_extended import decode_token
from server.models import TokenBlacklist
from server import db
from flask import abort
from sqlalchemy import exc
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

def _epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).
    """
    return datetime.fromtimestamp(epoch_utc)

def add_token_to_database(encoded_token, identity_claim):
    """
    Adds a new token to the database. It is not revoked when it is added.
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token[identity_claim]
    expires = _epoch_utc_to_datetime(decoded_token['exp'])
    revoked = False

    db_token = TokenBlacklist(
        jti=jti,
        token_type=token_type,
        user_identity=user_identity,
        expires=expires,
        revoked=revoked,
    )

    try:
        db.session.add(db_token)
        db.session.commit()
    except exc.SQLAlchemyError:
        abort(500, 'Internal server error')

def revoke_token(jti, user):
    """
    Revokes the given token. Raises an error if the token does
    not exist in the database
    """
    try:
        token = TokenBlacklist.query.filter_by(
            jti=jti, user_identity=user).one()
        token.revoked = True
        db.session.commit()
    except NoResultFound:
        abort(401, 'Token not found')
    except exc.SQLAlchemyError:
        abort(500, 'Internal server error')