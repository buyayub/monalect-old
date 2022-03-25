from sqlalchemy import delete
from sqlalchemy.orm import query
from monalect.models import Lesson
from monalect.database import db_session
from monalect.utils.shared import generateKey
from monalect.utils import notebook

def getAll(course_id):
    lessonAll = db_session.query(Lesson).filter(Course.course_id==course_id).fetchall()
    return lessonAll

def get(lesson_id):
    lesson = db_session.query(Lesson).filter(Lesson.id == lesson_id).first()
    return lesson

def delete(lesson_id):
    db_session.query(Lesson).filter(Lesson.id==lesson_id).delete()
    return None

def create(course_id, title="Untitled"):
    lesson = Lesson(course_id=course_id, title=title)
    db_session.add(lesson)
    db_session.commit()
    return lesson

def updateTitle(lesson_id, title):
    lesson = db_session.query(Lesson).filter(Lesson.id==lesson_id).first()
    lesson.title = title
    return lesson

#Pretty much the same as updateTitle until I add more stuff to it
def update(lesson_id, title):
    lesson = db_session.query(Lesson).filter(Lesson.id==lesson_id).first()
    lesson.title = title
    return lesson

