from sqlalchemy import select, delete
from monalect.models import Session
from monalect.database import db_session
from monalect.utils.shared import generateKey
import datetime

def create(user_id):
    session_id = generateKey(32)
    expiry_date = datetime.datetime.today() + datetime.timedelta(days=7)
    while True: 
        try:
            session = Session(id=session_id, user_id=user_id, expiry_date=expiry_date)
            db_session.add(session)
            db_session.commit()
            break
        except:
            db_session.execute(delete(Session).where(Session.user_id == user_id))
            continue
    return session

def delete(user_id):
    db_session.execute(delete(Session).where(Session.user_id == user_id))
    return None

def authenticate(user_id, session_id):
    session = db_session.execute(select(Session).where(Session.user_id == user_id)).first()
    authenticated = False
    if session:
        authenticated = (\
            session.user_id == user_id and \
            session.id == session_id and \
            datetime.date.today() < session.expiry_date)
    return authenticated

