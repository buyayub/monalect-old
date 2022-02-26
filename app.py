from flask import Flask, render_template, jsonify, request, escape, abort, Response
import datetime
import psycopg2
import bcrypt
import requests
import re
import secrets
import string

app = Flask(__name__, static_url_path='/static/')

RECAPTCHA_PRIVATE_KEY = "6LfJeYIeAAAAAO-PXK1qRuRAK_37acdTrKO7y0Zo"

"""
GLOBAL FUNCTIONS
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

def generateKey(length):
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for i in range(length))
    return key

def makeCORS(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

"""
USER REGISTRATION & LOGIN & SESSIONS

To-do:
    1. error if username taken
    2. error if email already used
    3. setup crontab to run an instruction that clears login attempts every day
"""

def registerUser(username, password, email=None):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
    user_id = generateKey(32)
    sql("INSERT INTO users VALUES (%s, %s, %s, %s, DEFAULT, %s)", (user_id, username, email, "none", hashed.decode()))
    sql("INSERT INTO login_attempts VALUES (%s, 0)", (user_id,))
    return user_id

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
    session_id = generateKey(32)
    expiry_date = datetime.datetime.today() + datetime.timedelta(days=7)
    while True:
        try:
            sql("INSERT INTO sessions VALUES (%s, %s, %s)", (session_id, user_id, expiry_date.isoformat())) #automatically translates it into ISO 8601, or .isoformat()
            break;
        except psycopg2.errors.UniqueViolation:
            sql("DELETE FROM sessions WHERE user_id = %s", (user_id,))
            continue
    return session_id, expiry_date


def getUserId(username):
    return (sql("SELECT id FROM users WHERE username = %s", (username,))[0][0])

def getUsername(user_id):
    return (sql("SELECT username FROM users WHERE id = %s", (user_id,))[0][0])

def addLoginAttempt(user_id):
    sql("UPDATE login_attempts SET attempts = attempts + 1 WHERE user_id = %s", (user_id,))
    return None

def deleteSession(user_id):
    sql("DELETE FROM sessions WHERE user_id = %s", (user_id,))
    return None

def validateSession(user_id, session_id):
    row = sql("SELECT user_id, session_id, expiry_date FROM sessions WHERE user_id = %s", (user_id,))
    if row != []:
        ruser_id = row[0][0]
        rsession_id = row[0][1]
        rexpiry_date = row[0][2]
        validated = ((ruser_id == user_id) and (rsession_id == session_id) and (datetime.date.today() < rexpiry_date))
    else:
        validated = False

    return validated

"""
Course CORS
"""


# COURSE

def verifyCourse(course_id, user_id):
    cuser_id = sql("SELECT user_id FROM courses WHERE id = %s", (course_id,))
    return user_id == cuser_id[0][0]

def createCourse(user_id):
    course_id = secrets.token_hex(8)
    sql("INSERT INTO courses VALUES (%s, %s, DEFAULT, NULL)", (course_id, user_id))
    return course_id

def getCourse(course_id):
    course = sql("SELECT title, description FROM courses WHERE id = %s", (course_id,))
    title = course[0][0]
    description = course[0][1]
    return {'title': title, 'description' : description}

def getCourses(user_id):
    data = sql ("SELECT id, title, description FROM courses WHERE user_id = %s", (user_id,))
    courses = [] 
    for i in data:
        course_id = i[0]
        textbook_pages = sql("SELECT sum(pages) FROM textbook WHERE course_id = %s", (course_id,))[0][0]
        notebook_words = sql("SELECT sum(array_length(regexp_split_to_array(text_content ,'\s'),1)) FROM notebook_section WHERE course_id = %s", (course_id,))[0][0]
        question_count = sql("SELECT COUNT(*) FROM question WHERE course_id = %s", (course_id,))[0][0]
        courses.append({"course_id" : course_id, "title" : i[1], "description": i[2], "textbook_pages": textbook_pages, "notebook_words": notebook_words, "question_count": question_count})
    return courses

def updateCourseDescription(course_id, description):
    sql("UPDATE courses SET description = %s WHERE id = %s", (description, course_id))
    return None

def updateCourseTitle(course_id, title):
    sql("UPDATE courses SET title = %s WHERE id = %s", (title, course_id))

# LESSON

def getLessons(course_id):
    title = sql("SELECT title FROM lesson WHERE course_id = %s", (course_id,))
    question_num = sql("")
    lessons = []
    for i in lessons:
        lesson.append({ "title" : i[0]})
    return lessons

def getLessonId(course_id, lesson_order):
    lesson_id = sql("SELECT title FROM lesson WHERE (course_id = %s AND lesson_order = %s)", (course_id, lesson_order))
    return lesson_id     

def createLesson(course_id, title, lesson_order):
    sql("INSERT INTO courses VALUES (DEFAULT, %s, %s, %s)", (course_id, title, lesson_order))
    return None

"""
Router
"""


@app.route("/api/register", methods=['POST', 'OPTIONS'])
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
    
    if request.method == 'POST':
        json_data = request.get_json() 
        try:
            username = escape(json_data['username'])
            email = escape(json_data['email'])
            password = escape(json_data['password'])
            captcha = escape(json_data['recaptcha'])
        except(KeyError):
            abort(400)

        if checkUsername(username) and checkPassword(password) and checkCaptcha(captcha):
            if checkEmail(email):
                user_id = registerUser(username, password, email)
                session_id, expiry_date  = createSession(user_id)
                response = makeCORS(jsonify({'user_id': user_id, 'session_id' : session_id, 'expiry_date': expiry_date}))
                return response, 201
            elif email == "":
                user_id = registerUser(username, password)
                session_id, expiry_date  = createSession(user_id)
                response = makeCORS(jsonify({'user_id': user_id, 'session_id' : session_id, 'expiry_date': expiry_date}))
                return response, 201
        else: 
            abort(400)
    elif request.method == 'OPTIONS':
        response = makeCORS(Response(""))
        return response, 201

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


@app.route("/api/login", methods=['POST', 'OPTIONS'])
def apiLogin():
    """
    JSON FIELD inputs, unordered:
        username(string)
        password(string)
        recaptcha(string)
    """
     
    json_data = request.get_json()
    if (request.method == 'POST'):
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
                    response = makeCORS(jsonify({'user_id': user_id, 'session_id' : session_id, 'expiry_date': expiry_date}))
                    return response, 200
                else:
                    addLoginAttempt(user_id)
                    return "", 403
            else: 
                if authenticateUser(user_id, password):
                    session_id, expiry_date = createSession(user_id)
                    response = makeCORS(jsonify({'user_id': user_id, 'session_id': session_id, 'expiry_date': expiry_date}))
                    return response, 200
                else: 
                    addLoginAttempt(user_id)
                    return "", 401
        except Exception as e:
            print(e)
            abort(400)
    elif (request.method == 'OPTIONS'):
        response = makeCORS(Response(""))
        return response, 201
    return "", 400


@app.route("/api/course", methods=['GET', 'POST'])
def apiCourse():
    if (request.method == 'GET'):
        user_id = escape(request.cookies.get('user_id'))
        session_id = escape(request.cookies.get('session_id'))
        if (validateSession(user_id, session_id)):
            courses = getCourses(user_id)
            response = makeCORS(jsonify(courses))
            return response, 201
        else:
            return "", 401
    elif (request.method == 'POST'):
        user_id = escape(request.cookies.get('user_id'))
        session_id = escape(request.cookies.get('session_id'))
        if (validateSession(user_id, session_id)):
            course_id = createCourse(user_id)
            response = makeCORS(jsonify({'course_id' : course_id}))
            return response, 201
        else:
            return "", 401
    elif request.method == 'OPTIONS':
        response = Response("")
        response = makeCORS(response)
        return response, 201

    return "", 400

@app.route("/api/course/<course_id>", methods=['DELETE', 'GET', 'POST'])
def apiCourseId(course_id):
    return "", 400

"""
API INITIAL LOAD FOR THE WEBSITE
"""

@app.route("/api/website/monalect", methods=['GET'])
def websiteOverview():
    try:
        user_id = escape(request.cookies.get('user_id'))
        session_id = escape(request.cookies.get('session_id'))
        if validateSession(user_id, session_id):
            payload = {'username': getUsername(user_id), 'courses' : getCourses(user_id) }
            response = makeCORS(jsonify(payload))
            return response, 201
        else: 
            raise Exception("session invalid")
    except Exception as e:
        print(e)
        return "", 400
    return "", 400

@app.route("/api/website/course", methods=['GET'])
def websiteCourse():
    return "", 400     

@app.route("/api/website/notebook") 
def websiteNotebook():
    return "", 400

@app.route("/api/website/textbook")
def websiteTextbook():
    return "", 400

@app.route("/api/website/questions")
def websiteQuestions():
    return "", 400

"""
TEST functions

@app.route("/")
def home():
    return render_template("home.j2")

@app.route("/login")
def login():
    return render_template("login.j2")

@app.route("/session")
def session():
    return render_template("session.j2")

@app.route("/course/overview/")
    return render_template("overview.j2")
"""
