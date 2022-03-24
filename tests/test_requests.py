from monalect.database import db_session
from flask import Flask
import monalect.models as models 
import monalect.app as monalect

def _register(client):
    return client.post("/api/register", json={
        "username": "yella",
        "password": "Test1234",
        "email": "",
        "recaptcha": ""})

def test_registration(client):
    response = client.post("/api/register", json={
        "username": "yella",
        "password": "Test1234",
        "email": "",
        "recaptcha": ""})

    assert response.status_code == 201
    assert response.json["user_id"] != None
    assert response.json["session_id"] != None
    assert response.json["expiry_date"] != None

def test_login(client):
    response = client.post("/api/login", json={
        "username": "yella",
        "password": "Test1234",
        "recaptcha": ""
        })

    assert response.status_code == 200
    assert response.json["user_id"] != None
    assert response.json["session_id"] != None
    assert response.json["expiry_date"] != None

