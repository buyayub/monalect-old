from sqlalchemy import select, delete, update
from sqlalchemy.orm import query
from monalect.models import User, LoginAttempts, Session
from monalect.database import db_session
from monalect.utils.shared import generateKey
from monalect.utils import check
import bcrypt, string, secrets, datetime


def register(username, password, email):
    #captcha = check.captcha(captcha)
    if check.username(username) and check.password(password) and (check.email(email) or email == ""): #and check.captcha(captcha):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf8'), salt)
        user_id = generateKey(32)

        user = User(username=username, id=user_id, passhash=hashed.decode())
        attempts = LoginAttempts(user_id=user_id)
        
        db_session.add(user)
        db_session.add(attempts)
        db_session.commit()
        return user
    else:
        raise ValueError("Invalid input")

def authenticate(user_id, password):
    user = db_session.query(User).filter(User.id == user_id).first()
    return bcrypt.checkpw(password.encode('utf8'), user.passhash.encode('utf8'))

#TO DO
def login(user_id, password):
    return None

def attempts(user_id):
    data = db_session.query(LoginAttempts).filter(LoginAttempts.user_id == user_id).first()
    return data.attempts

def addAttempt(user_id):
    #db_session.execute(select(LoginAttempts).where(LoginAttempts.user_id == user_id)).first()
    data = db_session.query(LoginAttempts).filter(LoginAttempts.user_id == user_id).first()
    data.attempts = data.attempts + 1 
    return None

def id(username):
    user = db_session.query(User).filter(User.username == username).first()
    return user.id

def username(user_id):
    user = db_session.query(User).filter(User.id == user_id).first()
    return user.username
