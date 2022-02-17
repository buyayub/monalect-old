from flask import Flask, render_template, jsonify, request, escape, abort
import psycopg2
import bcrypt
import requests
import re

app = Flask(__name__, static_url_path='/static/')

RECAPTCHA_PRIVATE_KEY = "6LfJeYIeAAAAAO-PXK1qRuRAK_37acdTrKO7y0Zo"

"""
Bunch of functions before I put them in a seperate file
"""

DATABASE = "dbname=monalecttest user=zheng"

def sendEmail(email):
    # Honestly, fuck email registration, what the fuck there is no documentation on that fucking shit everyone uses it what the fuck. if self hosting an email is so fucking ridiculous, then why are there no other existing fucking options, what the fuck.
    # I'm going with username+password and recaptcha for now
    # later on I'll use mailgun
    return None

"""
USER REGISTRATION

To-do:
    1. error if username taken
    2. error if email already used
"""

def registerUser(username, password, email="NULL"):
    conn = psycopg2.connect(DATABASE)
    cur = conn.cursor()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
    cur.execute("INSERT INTO users VALUES (DEFAULT, %s, %s, %s, DEFAULT, %s)", (username, email, "none", hashed))
    conn.commit()
    cur.close()
    conn.close()
    return None

def authenticateUser(username, password):
    conn = psycopg2.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT %s FROM users", (username,))
    user = cur.fetchone()
    return None

def checkCaptcha(captchaResponse):
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={ 'secret': RECAPTCHA_PRIVATE_KEY, 'response': captchaResponse})
    jsonData = response.json()
    return jsonData['success']

def checkUsername(username):
    valid = False
    if (username.isalnum() or (username.isalnum() and ("_" in username))):
        valid = True
    return valid

def checkEmail(email):
    return re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)

def checkPassword(password):
    return re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password)


"""
Router
"""

@app.route("/")
def dashboard():
    return render_template("home.j2")

@app.route("/api/register", methods=['POST'])
def apiRegister(): 
    """
    JSON field inputs, unordered:
        username (string)
        email (string)
        password (string)
        recaptcha (string): the g-recaptcha-code 
    HTTP Response outputs:
        204: if everything is good
        400: if input bad
        401: if captcha turns out false
        
    """
    json_data = request.get_json() 

    try:
        username = escape(json_data['username'])
        email = escape(json_data['email'])
        password = escape(json_data['password'])
        captcha = escape(json_data['recaptcha'])
    except(KeyError):
        abort(400)
    
    if not checkCaptcha(captcha):
        abort(401)
    if not checkUsername(username):
        abort(400)
    if not checkPassword(password):
        abort(400)

    if checkEmail(email):
        registerUser(username, password, email)
        return "", 201
    elif email == "":
        registerUser(username, password)
        return "", 201
    else: 
        abort(400)

    return "", 400
