from flask import Flask, jsonify, request, escape, abort, Response
from werkzeug.utils import secure_filename
import datetime
import requests
import re
import traceback
import os
from monalect.database import db_session
from monalect.models import User
from monalect.utils import *

UPLOAD_FOLDER = "/home/zheng/projects/monalect/textbooks/"
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__, static_url_path='/static/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Remember to replace this and make it safe for production somewhere
RECAPTCHA_PRIVATE_KEY = "6LfJeYIeAAAAAO-PXK1qRuRAK_37acdTrKO7y0Zo"
ALLOWED_ATTEMPTS = 9

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def makeCORS(response, methods='GET,POST,OPTIONS'):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', methods)
    return response

"""
GLOBAL FUNCTIONS
"""

@app.route("/api/register", methods=['POST', 'OPTIONS'])
def apiRegister(): 
    """
    JSON field inputs, unordered:
        username (string)
        email (string)
        password (string)
        recaptcha (string): the g-recaptcha-code 

    HTTP Successful Responses:
        204: everything is good
            session_id (string)
            user_id (string)
            expiry_date (string)

    HTTP Error Responses: 
        400: if something went horribly wrong
        401: if captcha turns out false
        409: if json parameters bad
        415: if not json
        422: if the user puts in bad input
    """

    if request.method == 'POST':
        try:
            json_data = request.get_json() 

            if (json_data == None):
                abort(415)

            username = escape(json_data['username'])
            email = escape(json_data['email'])
            password = escape(json_data['password'])
            captcha = escape(json_data['recaptcha'])

            user_response = user.register(username, password, email)
            session_response = session.create(user_response.id)
            response = makeCORS(jsonify({'user_id': user_response.id, 'session_id' : session_response.id, 'expiry_date': session_response.expiry_date}))
            return response, 201
        except(KeyError):
            abort(409)
        except(ValueError):
            abort(422)

        abort(400)
    elif request.method == 'OPTIONS':
        response = makeCORS(Response(""))
        return response, 201

    return "", 400

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

        user_id = user.id(username)

        if (user.attempts(user_id) > ALLOWED_ATTEMPTS):
            if (user.authenticate(user_id, password) and check.captcha(captcha)):
                session_response = session.create(user_id)
                response = makeCORS(jsonify({'user_id' : session_response.user_id, 'session_id' : session_response.id, 'expiry_date' : session_response.expiry_date}))
                return response, 200
            else:
                user.addAttempt(user_id)
                return "", 403
        else: 
            if user.authenticate(user_id, password):
                session_response = session.create(user_id)
                response = makeCORS(jsonify({'user_id': session_response.user_id, 'session_id': session_response.id, 'expiry_date': session_response.expiry_date}))
                return response, 200
            else: 
                user.addAttempt(user_id)
                return "", 401
        return "", 400
    elif (request.method == 'OPTIONS'):
        response = makeCORS(Response(""))
        return response, 201
    return "", 400

@app.route("/api/course", methods=['GET', 'POST'])
def apiCourse():
    if (request.method == 'GET'):
        user_id = escape(request.cookies.get('user_id'))
        session_id = escape(request.cookies.get('session_id'))
        if (session.authenticate(user_id, session_id)):
            courses = course.getAll(user_id)
            response = makeCORS(jsonify(courses))
            return response, 201
        else:
            return "", 401
    elif (request.method == 'POST'):
        user_id = escape(request.cookies.get('user_id'))
        session_id = escape(request.cookies.get('session_id'))
        if (validateSession(user_id, session_id)):
            course = course.create(user_id)
            response = makeCORS(jsonify({'course_id' : course.id}))
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
        if (session.authenticate(user_id, session_id) and course.authenticate(course_id, user_id)):
            json_data = request.get_json()
            title = escape(json_data['title'])
            lesson = lesson.create(course_id, title)
            response = jsonify({'id' : lesson.id , 'title' : lesson.title})
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
        if (session.authenticate(user_id, session_id)) and course.authenticate(course_id, user_id):
            lesson.delete(lesson_id)
            response = Response("")
            response = makeCORS(response)
            return response, 201
    elif request.method == 'OPTIONS':
        response = Response("")
        response = makeCORS(response, "OPTIONS,POST,DELETE")
        return response, 201

@app.route("/api/<course_id>/textbook", methods=['OPTIONS', 'POST']) 
def apiTextbook(course_id):
    try:
        user_id = escape(request.cookies.get('user_id'))
        session_id = escape(request.cookies.get('session_id'))
        if (session.authenticate(user_id, session_id) and course.authenticate(course_id, user_id)):
            if (request.method == 'POST'):
                title = escape(request.form['title'])
                isbn = escape(request.form['ISBN'])
                pages = escape(request.form['pages'])
                author = escape(request.form['author'])
                if not check.isbn(isbn):
                    return "", 403
                if 'textbook' in request.files:
                    pdf_file = request.files['textbook']
                    if (pdf_file.filename != ''):
                        filename = generateKey(16)
                        pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename + ".pdf"))
                        data = textbook.create(course_id, isbn, title, author, pages, filename)
                        response = jsonify(data)
                        response = makeCORS(response)
                        return response, 201
                    else:
                        data = textbook.create(course_id, isbn, title, author, pages)
                        response = jsonify(data)
                        response = makeCORS(response)
                        return response, 201
                else:
                    data = textbook.create(course_id, isbn, title, author, pages)
                    response = jsonify(data)
                    response = makeCORS(response)
                    return response, 201
                return "", 401
            elif request.method == 'OPTIONS':
                response = Response("")
                response = makeCORS(response)
                return response, 201
            elif request.method == 'GET':
                response = jsonify(getTextbooks(course_id))
                response = makeCORS(response)
                return response, 201
        else:
            return "", 401
    except Exception as e: 
        print(traceback.format_exc())
        return "", 400
    
@app.route("/api/<course_id>/textbook/<textbook_id>", methods=['POST', 'DELETE', 'OPTIONS']) 
def apiTextbookId(course_id, textbook_id):
    try:
        user_id = escape(request.cookies.get('user_id'))
        session_id = escape(request.cookies.get('session_id'))
        if (session.authenticate(user_id, session_id) and course.authenticate(course_id, user_id)):
            if (request.method == 'DELETE'):
                textbook.delete(textbook_id)
                response = Response("")
                response = makeCORS(response, "OPTIONS,POST,DELETE")
                return response, 201
            elif (request.method == 'OPTIONS'):
                response = Response("")
                response = makeCORS(response, "OPTIONS,POST,DELETE")
                return response, 201
        else:
            return "", 401
    except Exception as e: 
        print(traceback.format_exc())
        return "", 400

@app.route("/api/<course_id>/section/<lesson_id>", methods=['POST', 'DELETE', 'OPTIONS'])
def apiSection(course_id, lesson_id):
    try:
        if (request.method == 'POST'):
                user_id = escape(request.cookies.get('user_id'))
                session_id = escape(request.cookies.get('session_id'))
                if (session.authenticate(user_id, session_id) and course.authenticate(course_id, user_id)):
                    json_data = request.get_json()
                    textbook_id = escape(json_data['textbook_id'])
                    start_page = escape(json_data['start_page'])
                    end_page = escape(json_data['end_page'])
                    payload = textbook_section.create(textbook_id, lesson_id, start_page, end_page)
                    response = jsonify(payload)
                    response = makeCORS(response, "OPTIONS,POST,DELETE")
                    return response, 201 
                else:
                    return "", 401
        elif (request.method == 'OPTIONS'):
            response = Response("")
            response = makeCORS(response, "OPTIONS,POST,DELETE")
            return response, 201
        else:
            return "", 400
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
        if session.authenticate(user_id, session_id):
            payload = {'username' : user.username(user_id), 'courses' : course.get(user_id)}
            response = makeCORS(jsonify(payload))
            return response, 201
        else: 
            raise Exception("session invalid")
    except Exception as e:
        print(traceback.format_exc())
        return "", 400
    return "", 400

@app.route("/api/website/course/<course_id>", methods=['GET'])
def websiteCourse(course_id):
    try:
        return response, 201
    except Exception as e:
        print(traceback.format_exc())
        return "", 400     

@app.route("/api/website/<course_id>/notebook", methods=['GET']) 
def websiteNotebook(course_id):
    try:
        return "", 201
    except Exception as e:
        print(traceback.format_exc())
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
