from sqlalchemy import delete 
from sqlalchemy.orm import query
from monalect.models import Course
from monalect.database import db_session
from monalect.utils.shared import generateKey
import bcrypt, string, secrets, datetime

def authenticate(course_id, user_id):
    course = db_session.query(Course).filter(Course.id == course_id).first()
    return course.user_id == user_id

def create(user_id, title="Untitled", description=""):
    course = Course(user_id=user_id, title=title, description=description)
    db_session.add(course)
    db_session.commit()
    return course 

def delete(course_id):
   db_session.query(Course).filter(Course.id == course_id).delete()
   return None

def get(course_id):
    course = db_session.query(Course).filter(Course.id == course_id).first()
    return course

def getAll(user_id):
    courseAll = db_session.query(Course).filter(Course.user_id == user_id).fetchall()
    return courseAll

def update(course_id, title, description):
    course = db_session.query(Course).filter(Course.id == course_id).first()
    course.title = title
    course.description = description
    return course

def updateDescription(course_id, description):
    course = db_session.query(Course).filter(Course.id == course_id).first()
    course.description = description
    return course

def updateTitle(course_id, title):
    course = db_session.query(Course).filter(Course.id == course_id).first()
    course.title = title
    return course



