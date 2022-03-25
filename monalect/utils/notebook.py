from sqlalchemy import select, delete, update
from monalect.models import NotebookSection
from monalect.database import db_session
from monalect.utils.shared import generateKey

def get(course_id):
    notebook = db_session.query(NotebookSection).filter(NotebookSection.course_id==course_id).fetchall()
    return notebook

def getSection(section_id):
    section = db_session.query(NotebookSection).filter(NotebookSection.id==section_id)
    return section

def getByLesson(lesson_id):
    section = db_session.query(NotebookSection).filter(NotebookSection.id==section_id)
    return section

def create(course_id, lesson_id, body=None):
    section = NoteBookSection(course_id=course_id, lesson_id=lesson_id, body=body)
    db_session.add(section)
    db_session.commit()
    return section

def update(section_id, course_id, lesson_id, body):
    section = db_session.query(NotebookSection).filter(NotebookSection.id == section_id).first()
    section.course_id = course_id
    section.lesson_id = lesson_id
    section.body = body
    return section

def delete(section_id):
    db_session.query(NotebookSection).filter(NotebookSection.id == section_id).delete()
    
