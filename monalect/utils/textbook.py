from sqlalchemy import select, delete, update
from monalect.models import Textbook
from monalect.database import db_session
from monalect.utils.shared import generateKey
import bcrypt, string, secrets, datetime

def getAll(course_id):
    textbooks = db_session.execute(select(Textbook).where(Textbook.course_id == course_id)).fetchall()
    return textbooks

def get(textbook_id):
    textbook = db_session.execute(select(Textbook).where(Textbook.id == textbook_id)).first()
    return textbook

def delete(textbook_id):
    db_session.execute(delete(Textbook).where(Textbook.id == textbook_id))
    return None

def create(course_id, title=None, author=None, pages=0, filename=None):
    textbook = Textbook(course_id=course_id, title=title, author=author, pages=pages, filename=filename)
    db_session.add(lesson)
    db_session.execute()
    return textbook 

def updateTitle(textbook_id, title):
    db_session.execute(update(Textbook).where(Textbook.id == textbook_id).values(title = title))
    return None

