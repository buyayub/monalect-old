from sqlalchemy import select, delete, update
from monalect.models import Goal
from monalect.database import db_session
from monalect.utils.shared import generateKey

def create(course_id, goal, metric=0):
    goal = Goal(course_id=course_id, goal=goal, metric=metric, complete=False)
    db_session.add(goal)
    db_session.commit()
    return goal

def getAll(course_id):
    goals = db_session.execute(select(Goal).where(Goal.course_id == course_id))
    return goals


