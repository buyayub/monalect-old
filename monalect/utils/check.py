import re

def username(username):
    return ((username.isalnum() or (username.isalnum() and ("_" in username))) and len(username) < 256)

def email(email):
    return re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)

def password(password):
    return (re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password) and len(password) < 256)

def isbn(isbn):
   return (re.fullmatch(r'^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$', isbn))

def captcha(captchaResponse):
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={ 'secret': RECAPTCHA_PRIVATE_KEY, 'response': captchaResponse})
    jsonData = response.json()
    return jsonData['success']
