from sqlalchemy import select, delete, update
from monalect.models import Course
from monalect.database import db_session
from monalect.utils.shared import generateKey
import bcrypt, string, secrets, datetime

def authenticate(course_id, user_id):
    course = db_session.execute(select(Course.user_id).where(Course.id == course_id))
    return course.user_id == user_id

def create(user_id, title="Untitled", description=""):
    course = Course(user_id=user_id, title=title, description=description)
    db_session.add(course)
    db_session.commit()
    return None

def get(course_id):
    course = db_session.execute(select(Course).where(Course.course_id == course_id).first())
    return course

def getAll(user_id):
    courses = db_session.execute(select(Course).where(Course.user_id == user_id)).fetchall()
    return courses

def updateDescription(course_id, description):
    db_session.execute(update(Course).where(Course.id==course_id).values(description = description))
    return None

def updateTitle(course_id, title):
    db_session.execute(update(Course).where(Course.id==course_id).values(title = title))
    return None



