from sqlalchemy.orm import query 
from monalect.utils import user
from monalect.app import db_session
from monalect.models import LoginAttempts

def test_registration():
    user_response = user.register("timothy", "Test1234", "")
    
    assert user_response.id != None
    assert len(user_response.id) == 32

    assert user_response.username == "timothy"
    assert user_response.passhash != None

def test_authenticate():
    user_id = user.id("timothy")
    assert user.authenticate(user_id, "Test1234") == True
    assert user.authenticate(user_id, "wrong1234") == False

def test_addAttempt():
    user_id = user.id("timothy")

    original = db_session.query(LoginAttempts).filter(LoginAttempts.user_id == user_id).first().attempts

    user.addAttempt(user_id)

    new = db_session.query(LoginAttempts).filter(LoginAttempts.user_id == user_id).first().attempts
    assert new == original + 1


