from sqlalchemy import select, delete, update
from monalect.models import User, LoginAttempts, Session
from monalect.database import db_session
from monalect.utils.shared import generateKey
import bcrypt, string, secrets, datetime

def register(username, password, email=None):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
    user_id = generateKey(32)
    user = User(username=username, id=user_id, passhash=hashed.decode())
    db_session.add(user)
    db_session.commit()
    return user_id

def authenticate(user_id, password):
    user = db_session.execute(select(User.passhash).where(User.id == user_id)).first()
    return bcrypt.checkpw(password.encode('utf8'), user.passhash.encode('utf8'))

def attempts(user_id):
    data = db_session.execute(select(LoginAttempts.attempts).where(LoginAttempts.user_id == user_id)).first()
    return data.attempts

def addAttempt(user_id):
    db_session.execute(update(LoginAttempts).where(LoginAttempts.user_id == user_id).values(attempts = attempts + 1))
    return None

def id(username):
    user = db_session.execute(select(User.id).where(User.username == username)).first()
    return user.id

def username(user_id):
    user = db_session.execute(select(User.username).where(User.id == user_id)).first()
    return user.username

