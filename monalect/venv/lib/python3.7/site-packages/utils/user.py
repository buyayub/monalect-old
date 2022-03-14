from monalect.models import User
from monalect.database import db_session
import bcrypt, string, secrets

def generateKey(length):
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for i in range(length))
    return key

def register(username, password, email=None):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
    user_id = generateKey(32)
    user = User(username=username, id=user_id, passhash=hashed)
    db_session.add(user)
    db_session.commit()
    return None


