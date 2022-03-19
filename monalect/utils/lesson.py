from sqlalchemy import select, delete, update
from monalect.models import Lesson
from monalect.database import db_session
from monalect.utils.shared import generateKey

def getAll(course_id):
    lessons = db_session.execute(select(Lesson).where(Course.course_id==course_id)).fetchall()
    return lessons

def get(lesson_id):
    lesson = db_session.execute(select(Lesson).where(Lesson.id == lesson_id)).first()
    return lesson

def delete(lesson_id):
    db_session.execute(delete(Lesson).where(Lesson.id==lesson_id))
    return None

def create(course_id, title="Untitled"):
    lesson = Lesson(course_id==course_id, title==title)
    db_session.add(lesson)
    db_session.execute()
    return lesson

def updateTitle(lesson_id, title):
    db_session.execute(update(Lesson).where(Lesson.id==lesson_id).values(title=title))
    return None

