from monalect.database import db_session
from flask import Flask
import monalect.models as models 
import monalect.app as monalect
import monalect.utils.check as check

def _login(client):
    response = client.post("/api/login", json={
        "username": "yella",
        "password": "Test1234",
        "recaptcha": ""
        })

    client.set_cookie('localhost', 'user_id', response.json["user_id"])
    client.set_cookie('localhost', 'session_id', response.json["session_id"])
    client.set_cookie('localhost', 'expiry_date', response.json["expiry_date"])

    return None

def _captcha(recaptcha):
    return recaptcha != None

def test_registration(client):

    check.captcha = _captcha

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

def test_courseCreate(client):
    _login(client)
    
    response = client.post("/api/course", json={"title": "Test Course", "description" : "This is a description"})
    assert response.status_code == 201

    assert response.json["id"] != None
    assert response.json["title"] == "Test Course"
    assert response.json["description"] == "This is a description"
    assert response.json["created"] != None

def test_courseInit(client):
    _login(client)

    response = client.get("/api/website/monalect")
    assert response != None
    assert response.status_code == 201
    assert response.json["courses"][0]["id"] != None
    assert response.json["courses"][0]["title"] == "Test Course"
    assert response.json["courses"][0]["description"] == "This is a description"
    assert response.json["courses"][0]["created"] != None

def test_textbookCreate(client):
    _login(client)

    course_response = client.get("/api/website/monalect")
    course_id = course_response.json["courses"][0]["id"]
    #Data instead of json
    response =  client.post("/api/" + str(course_id) + "/textbook", data={"title":"Book of Proof","isbn" : "9780989472128", "pages" : 368, "author" : "Richard Hammack"})

    assert response.json["id"] != None
    assert response.json["title"] == "Book of Proof"
    assert response.json["isbn"] == "9780989472128"
    assert response.json["pages"] == 368
    assert response.json["author"] == "Richard Hammack"

def test_lessonCreate(client):
    _login(client)

    course_respons = client.get("/api/website/monalect")
    course_id = course_response.json["courses"][0]["id"]
    

def test_courseOverviewInit(client):
    _login(client)

    course_response = client.get("/api/website/monalect")
    course_id = course_response.json["courses"][0]["id"]

    response = client.get("/api/website/course/" + str(course_id))

    assert response != None
    assert response.json['username'] == "yella"
    assert response.json['course']['id'] == course_id
    assert response.json['course']['description'] == "This is a description"
    assert response.json['textbooks'][0]["title"] ==  "Book of Proof"
    assert response.json['textbooks'][0]["isbn"] ==  "9780989472128"
    assert response.json['textbooks'][0]["pages"] == 368
    assert response.json['textbooks'][0]["author"] == "Richard Hammack"
