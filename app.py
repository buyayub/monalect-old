from flask import Flask, render_template, jsonify, request, escape, abort, Response
from werkzeug.utils import secure_filename
import datetime
import psycopg2
import bcrypt
import requests
import re
import secrets
import string
import traceback
import os

UPLOAD_FOLDER = "/home/zheng/projects/monalect/textbooks/"
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__, static_url_path='/static/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

def makeCORS(response, methods='GET,POST,OPTIONS'):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', methods)
    return response

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
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
    course = sql("SELECT title, description, created FROM courses WHERE id = %s", (course_id,))
    title = course[0][0]
    description = course[0][1]
    created = course[0][2]
    return {'title': title, 'description' : description, 'created' : created}

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
    lessons = sql("SELECT id, title FROM lesson WHERE course_id = %s", (course_id,))
    payload = []
    for i in lessons:
        lesson_id = i[0]
        textbook_sections = sql("SELECT book, textbook.title, textbook_section.textbook, start_page, end_page FROM textbook_section, textbook WHERE lesson_id=%s AND textbook.id = textbook", (lesson_id,))
        question_count = sql("SELECT COUNT(*) FROM question WHERE course_id = %s AND question.lesson = %s", (course_id, lesson_id))[0][0]
        notebook_words = sql("SELECT sum(array_length(regexp_split_to_array(text_content ,'\s'),1)) FROM notebook_section WHERE course_id = %s AND lesson_id = %s", (course_id, lesson_id))[0][0]
        payload.append({ "id": lesson_id, "title" : i[1], "textbook_sections": textbook_sections, "question_count" : question_count, "notebook_words" : notebook_words})
    return payload

def getLessonId(course_id, lesson_order):
    lesson_id = sql("SELECT title FROM lesson WHERE (course_id = %s AND lesson_order = %s)", (course_id, lesson_order))
    return lesson_id     

def deleteLesson(lesson_id):
    sql("DELETE FROM lesson WHERE id = %s", (lesson_id,))
    return None

def createLesson(course_id, title):
    lesson_id = generateKey(32)
    sql("INSERT INTO lesson VALUES (%s, %s, %s)", (lesson_id, course_id, title))
    return lesson_id

def updateLessonOrder(lesson_order, lesson_id):
    sql("UPDATE lesson SET lesson_order = %s WHERE id = %s", (lesson_order, lesson_id))
    return None

def updateLessonTitle(lesson_title, lesson_id):
    sql("UPDATE lesson SET title = %s WHERE id = %s", (lesson_title, lesson_id))
    return None

# TEXTBOOK 

def createTextbook(course_id, isbn, title, author, pages, filename=None):
    textbook_id = generateKey(16)
    sql("INSERT INTO textbook VALUES (%s, %s, %s, %s, %s, %s, %s)", (textbook_id, course_id, filename, author, isbn, title, pages))
    
    return {"id" : textbook_id, "author" : author, "pages" : pages}

def createTextbookSection(textbook_id, lesson_id, start_page, end_page):
    sql("INSERT INTO textbook_section VALUES (%s, %s, %s, %s)", (textbook_id, lesson_id, start_page, end_page))
    return None

def getTextbook(textbook_id):
    textbook = sql("select book, title, pages from textbook where id = %s", (textbook_id,))
    return none

def getTextbooks(course_id):
    textbooks = sql("SELECT id, book, title, pages from TEXTBOOK where course_id = %s", (course_id,))
    return textbooks

def getTextbookSections(lesson_id):
    textbook_sections = sql("SELECT book, textbook.title, textbook_section.textbook, start_page, end_page FROM textbook_section, textbook WHERE lesson_id=%s AND textbook.id = textbook_section.textbook", (lesson_id,))
    return textbook_sections

def checkISBN(isbn):
   return (re.fullmatch(r'^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$'))

# GOALS

def getGoals(course_id):
    goals = sql("SELECT goal, metric FROM goals WHERE course_id=%s", (course_id,))
    return goals

def createGoal(course_id, goal_type, metric):
    sql("INSERT INTO goals VALUES (%s, %s, %s)", (course_id, goal_type, metric))
    return None


"""
API Router
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

@app.route("/api/course/<course_id>/lesson", methods=['OPTIONS', 'GET', 'POST'])
def apiLesson(course_id):
    if (request.method == 'POST'):
        user_id = escape(request.cookies.get('user_id'))
        session_id = escape(request.cookies.get('session_id'))
        if (validateSession(user_id, session_id)) and verifyCourse(course_id, user_id):
            json_data = request.get_json()
            title = escape(json_data['title'])
            lesson_id = createLesson(course_id, title)
            response = jsonify({'id' : lesson_id, 'title' : title})
            response = makeCORS(response)
            return response, 201
    elif request.method == 'OPTIONS':
        response = Response("")
        response = makeCORS(response)
        return response, 201
    return "", 400 

@app.route("/api/course/<course_id>/lesson/<lesson_id>", methods=['OPTIONS', 'POST', 'DELETE'])
def apiLessonId(course_id, lesson_id):
    if (request.method == 'POST'):
        return "", 404
    elif (request.method == 'DELETE'):
        user_id = escape(request.cookies.get('user_id'))
        session_id = escape(request.cookies.get('session_id'))
        if (validateSession(user_id, session_id)) and verifyCourse(course_id, user_id):
            deleteLesson(lesson_id)
            response = Response("")
            response = makeCORS(response)
            return response, 201
    elif request.method == 'OPTIONS':
        response = Response("")
        response = makeCORS(response, "OPTIONS,POST,DELETE")
        return response, 201

@app.route("/api/<course_id>/textbook", methods=['OPTIONS', 'POST']) 
def apiTextbook():
    try:
        if (request.method == 'POST'):
            title = escape(request.form['title'])
            isbn = escape(request.form['ISBN'])
            pages = escape(request.form['pages'])
            author = escape(request.form['author'])
            if not checkISBN(isbn):
                return "", 401

            if 'textbook' in request.files:
                pdf_file = request.files['textbook']
                if (pdf_file.filename != ''):
                    filename = generateKey(16)
                    pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    data = createTextbook(course_id, isbn, title, author, pages, filename)
                    response = jsonify(data)
                    response = makeCORS(response)
                    return response, 201
            else:
                data = createTextbook(course_id, isbn, title, author, pages)
                response = jsonify(data)
                response = makeCORS(response)
                return response, 201

                        
            return "", 401
        elif request.method == 'OPTIONS':
            response = Response("")
            response = makeCORS(response)
            return response, 201
    except Exception as e: 
        print(traceback.format_exc())
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

@app.route("/api/website/course/<course_id>", methods=['GET'])
def websiteCourse(course_id):
    try:
        user_id = escape(request.cookies.get('user_id'))
        session_id = escape(request.cookies.get('session_id'))
        if (validateSession(user_id, session_id) and verifyCourse(course_id, user_id)):
            course = getCourse(course_id)
            lessons = getLessons(course_id)
            textbooks = getTextbooks(course_id)
            goals = getGoals(course_id)
            payload = {'username': getUsername(user_id), 'course': course, 'lessons': lessons, 'textbooks': textbooks, 'goals' : goals}
            response = jsonify(payload)
            response = makeCORS(response)
            return response, 201
        else:
            return "", 400
    except Exception as e:
        print(traceback.format_exc())
        return "", 400     

@app.route("/api/website/<course_id>/notebook") 
def websiteNotebook(course_id):
    return "", 400

@app.route("/api/website/<course_id>/textbook")
def websiteTextbook(course_id):
    return "", 400

@app.route("/api/website/<course_id>/questions")
def websiteQuestions(course_id):
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
