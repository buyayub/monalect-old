from flask import Flask, render_template, jsonify, request, escape, abort
import datetime
import psycopg2
import bcrypt
import requests
import re
import secrets

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

def sql(command, values):
    conn = psycopg2.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(command, values)
    response = None
    if "SELECT" in command:
        response = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return response

"""
USER REGISTRATION & LOGIN

To-do:
    1. error if username taken
    2. error if email already used
    3. setup crontab to run an instruction that clears login attempts every day
"""

def registerUser(username, password, email=None):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
    user_id = secrets.token_hex(16)
    sql("INSERT INTO users VALUES (%s, %s, %s, %s, DEFAULT, %s)", (user_id, username, email, "none", hashed.decode()))
    sql("INSERT INTO login_attempts VALUES (%s, 0)", (user_id,))
    return None

def authenticateUser(user_id, password):
    hashed = sql("SELECT passhash FROM users WHERE id = %s", (user_id,))[0][0]
    return bcrypt.checkpw(password.encode('utf8'), hashed.encode('utf8'))

def checkCaptcha(captchaResponse):
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={ 'secret': RECAPTCHA_PRIVATE_KEY, 'response': captchaResponse})
    jsonData = response.json()
    return jsonData['success']

def checkUsername(username):
    return ((username.isalnum() or (username.isalnum() and ("_" in username))) and len(username) < 256)

def checkEmail(email):
    return re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)

def checkPassword(password):
    return (re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password) and len(password) < 256)

def tooManyAttempts(user_id):
    attempts = sql("SELECT attempts FROM login_attempts WHERE user_id = %s", (user_id,))[0][0]
    return (attempts > 9)

def createSession(user_id):
    session_id = secrets.token_hex(32)
    expiry_date = datetime.datetime.today() + datetime.timedelta(days=7)
    print(expiry_date.isoformat())
    sql("INSERT INTO sessions VALUES (%s, %s, %s)", (session_id, user_id, expiry_date.isoformat())) #automatically translates it into ISO 8601, or .isoformat()
    return session_id, expiry_date.isoformat()

def getUserId(username):
    return (sql("SELECT id FROM users WHERE username = %s", (username,))[0][0])

def addLoginAttempt(user_id):
    sql("UPDATE login_attempts SET attempts = attempts + 1 WHERE user_id = %s", (user_id,))
    return None

def deleteSession(user_id):
    sql("DELETE FROM sessions WHERE user_id = %s", (user_id,))
    return None

def validateSession(user_id, session_id):
    row = sql("SELECT user_id, session_id, expiry_date FROM sessions WHERE user_id = %s", (user_id,))
    ruser_id = row[0][0]
    rsession_id = row[0][1]
    rexpiry_date = row[0][2]

    return ((ruser_id == user_id) and (rsession_id == session_id) and (datetime.date.today() < rexpiry_date))

"""
Router
"""

@app.route("/")
def home():
    return render_template("home.j2")

@app.route("/login")
def login():
    return render_template("login.j2")

@app.route("/session")
def session():
    return render_template("session.j2")

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

@app.route("/api/session", methods=['POST'])
def apiSession():
    # This is just a test, there isn't any error checking here
    """
    JSON field inputs, unordered:
        user_id (string)
        session_id (string)
    """
    json_data = request.get_json()
    user_id = escape(json_data['user_id'])
    session_id = escape(json_data['session_id'])

    valid_session = validateSession(user_id, session_id)
    if (valid_session):
        return "", 200
    else:
        return "", 401


@app.route("/api/login", methods=['POST'])
def apiLogin():
    """
    JSON FIELD inputs, unordered:
        username(string)
        password(string)
        recaptcha(string)
    """
     
    json_data = request.get_json()
    try:
        username = escape(json_data['username'])
        password = escape(json_data['password'])
        captcha = escape(json_data['recaptcha'])
    except KeyError as e:
        print(e)
        abort(400)
    
    try: 
        user_id = getUserId(username)
        if tooManyAttempts(user_id):
            if (authenticateUser(user_id, password) and checkCaptcha(captcha)):
                session_id, expiry_date = createSession(user_id)
                return jsonify({'user_id': user_id, 'session_id' : session_id, 'expiry_date': expiry_date}), 200
            else:
                addLoginAttempt(user_id)
                return "", 403
        else: 
            if authenticateUser(user_id, password):
                session_id = createSession(user_id)
                return jsonify({'user_id': user_id, 'session_id': session_id}), 200
            else: 
                addLoginAttempt(user_id)
                return "", 401
    except Exception as e:
        print(e)
        abort(400)

    return "", 400

