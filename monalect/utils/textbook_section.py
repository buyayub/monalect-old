from sqlalchemy import select, delete
from monalect.models import TextbookSection
from monalect.database import db_session
from monalect.utils.shared import generateKey

def create(course_id, lesson_id, textbook_id, start_page=None, end_page=None):
    textbook_section = TextbookSection(course_id=course_id, lesson_id=lesson_id, textbook_id=textbook_id, start_page=start_page, end_page=end_page)
    db_session.add(textbook_section)
    db_session.execute()
    return textbook_section

def get(section_id):
    textbook_section = db_session.execute(select(TextbookSection).where(TextbookSection.id == section_id)).first()
    return textbook_section

def getByTextbook(textbook_id):
    textbook_sections = db_session.execute(select(TextbookSection).where(TextbookSection.textbook_id == textbook_id)).fetchall()
    return textbook_sections

def getByLesson(lesson_id):
    textbook_sections = db_session.execute(select(TextbookSection).where(TextbookSection.lesson_id == lesson_id)).fetchall()
    return textbook_sections

