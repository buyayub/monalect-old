from monalect.database import init_db, db_session
from flask_testing import TestCase
from flask import Flask
import monalect.models as models 
import unittest
import flask_testing

class TestUser(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        init_db()
    
    def test_registration(self):
        user = "help"
        assert user == "halp"

if __name__ == "__main__":
    unittest.main()


