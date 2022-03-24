from sqlalchemy import select, delete
from monalect.models import TextbookSection
from monalect.database import db_session
from monalect.utils.shared import generateKey

def create(course_id, lesson_id, textbook_id, start_page=None, end_page=None):
    section = TextbookSection(course_id=course_id, lesson_id=lesson_id, textbook_id=textbook_id, start_page=start_page, end_page=end_page)
    db_session.add(section)
    db_session.execute()
    return section

def get(section_id):
    section = db_session.query(TextbookSection).filter(TextbookSection.id == section_id).first()
    return section

def getByTextbook(textbook_id):
    sectionAll = db_session.query(TextbookSection).filter(TextbookSection.textbook_id == textbook_id).fetchall()
    return section_all

def getByLesson(lesson_id):
    sectionAll = db_session.query(TextbookSection).filter(TextbookSection.lesson_id == lesson_id).fetchall()
    return sectionAll 

def delete(section_id):
    db_session.query(TextbookSection).filter(TextbookSection.id == section_id).delete()
    return None
    
def deleteByLesson(lesson_id):
    db_session.query(TextbookSection).filter(TextbookSection.lesson_id == lesson_id).delete()
    return None

def deleteByTextbook(textbook_id):
    db_session.query(TextbookSection).filter(TextbookSection.textbook_id == textbook_id).delete()
    return None

def update(section_id, lesson_id, textbook_id, start_page=None, end_page=None):
    section = db_session.query(TextbookSection).filter(TextbookSection.id == section_id).first()
    
    if lesson_id:
        section.lesson_id = lesson_id
    if textbook_id:
        section.textbook_id = textbook_id

    section.start_page = start_page
    section.end_page = end_page
    return section
