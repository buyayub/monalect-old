from flask import Flask, render_template, jsonify, request, escape, abort, Response
from werkzeug.utils import secure_filename
import datetime
import requests
import re
import traceback
import os
from api.database import db_session, init_db
from api.models import User

UPLOAD_FOLDER = "/home/zheng/projects/monalect/textbooks/"
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__, static_url_path='/static/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

RECAPTCHA_PRIVATE_KEY = "6LfJeYIeAAAAAO-PXK1qRuRAK_37acdTrKO7y0Zo"

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

print(User.query.all())
"""
GLOBAL FUNCTIONS
"""

@app.route("/api/register", methods=['POST', 'OPTIONS'])
def apiRegister(): 
    if request.method == 'POST':
        return response, 201
    elif request.method == 'OPTIONS':
        return response, 201

    return "", 400

@app.route("/api/login", methods=['POST', 'OPTIONS'])
def apiLogin():
    if (request.method == 'POST'):
        return response, 201
    elif (request.method == 'OPTIONS'):
        return response, 201
    return "", 400

@app.route("/api/course", methods=['GET', 'POST'])
def apiCourse():
    if (request.method == 'GET'):
        return "", 201
    elif (request.method == 'POST'):
        return "", 201
    elif request.method == 'OPTIONS':
        return "", 201
    return "", 400

@app.route("/api/course/<course_id>", methods=['DELETE', 'GET', 'POST'])
def apiCourseId(course_id):
    return "", 400

@app.route("/api/course/<course_id>/lesson", methods=['OPTIONS', 'GET', 'POST'])
def apiLesson(course_id):
    if (request.method == 'POST'):
        return "", 201
    elif request.method == 'OPTIONS':
        return "", 201
    return "", 400 

@app.route("/api/course/<course_id>/lesson/<lesson_id>", methods=['OPTIONS', 'POST', 'DELETE'])
def apiLessonId(course_id, lesson_id):
    if (request.method == 'POST'):
        return "", 201
    elif (request.method == 'DELETE'):
        return "", 201
    elif request.method == 'OPTIONS':
        return "", 201

@app.route("/api/<course_id>/textbook", methods=['OPTIONS', 'POST']) 
def apiTextbook(course_id):
    try:
            if (request.method == 'POST'):
                return "", 201
            elif request.method == 'OPTIONS':
                return "", 201
            elif request.method == 'GET':
                return "", 201
    except Exception as e: 
        print(traceback.format_exc())
        return "", 400
    
@app.route("/api/<course_id>/textbook/<textbook_id>", methods=['POST', 'DELETE', 'OPTIONS']) 
def apiTextbookId(course_id, textbook_id):
    try:
        if (request.method == 'DELETE'):
            return "", 201
        elif (request.method == 'OPTIONS'):
            return "", 201
        else:
            return "", 401
    except Exception as e: 
        print(traceback.format_exc())
        return "", 400

@app.route("/api/<course_id>/section/<lesson_id>", methods=['POST', 'DELETE', 'OPTIONS'])
def apiSection(course_id, lesson_id):
    try:
        if (request.method == 'POST'):
            return "", 201 
        elif (request.method == 'OPTIONS'):
            return "", 201
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
            return response, 201
    except Exception as e:
        print(e)
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
