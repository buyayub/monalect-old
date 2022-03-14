from monalect.models import User
import bcrypt, string, secrets

def generateKey(length):
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for i in range(length))
    return key

def register(username, password, email=None):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password)
    user_id = generateKey(32)
     

