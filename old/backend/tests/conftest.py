import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from monalect.app import app as monalect_app

@pytest.fixture()
def app():
    monalect_app.config['TESTING'] = True
    return monalect_app 

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope='session')
def db_session(request):
    db_url = request.config.getoption("--dburl")

"""
@pytest.fixture(scope='session')
def connection():
    engine = create_engine("sqlite//:memory:")
    engine.connect()
"""
