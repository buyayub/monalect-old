import bcrypt, string, secrets 

def generateKey(length):
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for i in range(length))
    return key
