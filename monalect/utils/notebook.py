from sqlalchemy import select, delete, update
from monalect.models import NotebookSection
from monalect.database import db_session
from monalect.utils.shared import generateKey

def get(course_id):
    notebook = db_sesssion(select(NotebookSection).where(NotebookSection.course_id==course_id))
    return notebook

