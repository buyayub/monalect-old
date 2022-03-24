from sqlalchemy import select, delete, update
from monalect.models import Textbook
from monalect.database import db_session
from monalect.utils.shared import generateKey
import bcrypt, string, secrets, datetime

def getAll(course_id):
    textbookAll = db_session.query(Textbook).filter(Textbook.course_id == course_id).fetchall()
    return textbookAll

def get(textbook_id):
    textbook = db_session.query(Textbook).filter(Textbook.id == textbook_id).first()
    return textbook

def delete(textbook_id):
    db_session.query(Textbook).filter(Textbook.id == textbook_id).delete()
    return None

def create(course_id, title=None, isbn=None, author=None, pages=0, filename=None):

    if len(isbn) == 10:
        isbn = "978" + isbn

    if (len(isbn) != 13 and isbn != None) or not isbn.isnumeric():
        raise ValueError

    textbook = Textbook(course_id=course_id, title=title, author=author, pages=pages, filename=filename)
    db_session.add(lesson)
    db_session.execute()
    return textbook 

def updateTitle(textbook_id, title):
    textbook = db_session.query(Textbook).filter(Textbook.id == textbook_id).first()
    textbook.title = title
    return textbook

def update(textbook_id, author, isbn, title, pages):
    textbook = db_session.query(Textbook).filter(Textbook.id == textbook_id).first()

    if len(isbn) == 10:
        isbn = "978" + isbn

    if len(isbn) != 13 and isbn != None:
        raise ValueError

    textbook.isbn = isbn
    textbook.author = author
    textbook.title = title
    textbook.pages = pages
    return textbook
