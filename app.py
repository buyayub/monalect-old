from flask import Flask, render_template, jsonify
from form import RegisterForm
import psycopg2
import bcrypt
import secrets

app = Flask(__name__)

RECAPTCHA_PRIVATE_KEY = "6LeDC4IeAAAAADiJ0WtOEus6G9OyKQXSSPhDgxaj"
RECAPTCHA_PUBLIC_KEY = "6LeDC4IeAAAAAEF4IvI3tcv7zbeb7EuBAXHNMoc8"

"""
Bunch of functions before I put them in a seperate file
"""

DATABASE = "dbname=monalectTest user=zheng"

def sendEmail(email):
    # Honestly, fuck email registration, what the fuck there is no documentation on that fucking shit everyone uses it what the fuck. if self hosting an email is so fucking ridiculous, then why are there no other existing fucking options, what the fuck.
    # I'm going with username+password and recaptcha for now
    # later on I'll use mailgun

def registerUser(username, password, email="DEFAULT"):
    conn = psycopg2.connect(DATABASE)
    cur = conn.cursor()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    cur.execute("INSERT INTO users VALUES (%s, %s, %s, DEFAULT, %s)", (username, email, "none", hashed))
    cur.commit()
    cur.close()
    conn.close()

def checkUser(username, password):
    conn = psycopg2.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT %s FROM users", (username,))
    user = cur.fetchone()

     


"""
Router
"""

@app.route("/")
def dashboard():
    return ""

@app.route("/api/")
def api():
    return ""
