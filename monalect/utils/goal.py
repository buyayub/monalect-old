from sqlalchemy import select, delete, update
from sqlalchemy.orm import query
from monalect.models import Goal
from monalect.database import db_session
from monalect.utils.shared import generateKey

def create(course_id, goal, metric=0):
    goal = Goal(course_id=course_id, goal = Goal.TYPE[goal], metric=metric, complete=False)
    db_session.add(goal)
    db_session.commit()
    return goal

def getAll(course_id):
    goalAll = db_session.query(Goal).filter(Goal.course_id == course_id))
    return goalAll

def get(goal_id):
    goal = db_session.query(Goal).filter(Goal.id == goal_id).first()
    return goal

def delete(goal_id):
    db_session.query(Goal).filter(Goal.id == goal_id).delete()
    return None

def update(goal_id, goal, complete, metric):
    goal = db_session.query(Goal).filter(Goal.id == goal_id).first()
    goal.goal = Goal.TYPE[goal]
    goal.complete = complete
    goal.metric = metric
    return goal

