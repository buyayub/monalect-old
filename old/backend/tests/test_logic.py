from sqlalchemy.orm import query 
from monalect.utils import user, course, lesson, goal, textbook, textbook_section, notebook
from monalect.app import db_session
from monalect.models import LoginAttempts
import monalect.utils.check as check

def _captcha(recaptcha):
    return recaptcha != None

def test_registration():
    check.captcha = _captcha

    user_response = user.register("timothy", "Test1234", "", "")
    
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

def test_courseCRUD():
    user_id = user.id("timothy")

    #CREATE
    created = course.create(user_id, "Test Course", "This is a test course")
    assert created.id
    assert created.title == "Test Course"
    assert created.description == "This is a test course"
    
    #READ
    read = course.get(created.id)
    assert read.id
    assert read.title == "Test Course"
    assert read.description == "This is a test course"

    #UPDATE
    updated = course.update(read.id, "Hello", "How you doing")
    assert updated.id 
    assert updated.title == "Hello"
    assert updated.description == "How you doing"

    #DELETE
    course.delete(created.id)
    created = lesson.get(created.id)
    read = lesson.get(read.id)
    updated = lesson.get(updated.id)

    assert created == None
    assert read == None
    assert updated == None

def test_lessonCRUD():
    user_id = user.id("timothy")
    original = course.create(user_id, "Text Course", "This is a test course")
    
    #CREATE
    created = lesson.create(original.id, "Hello")
    assert created.id != None
    assert created.title == "Hello"

    #CREATE UNTITLED
    untitled = lesson.create(original.id)
    assert untitled.id != None
    assert untitled.title == "Untitled"

    #READ
    read = lesson.get(created.id)
    assert created.id != None
    assert created.title == "Hello"

    #UPDATE
    updated = lesson.update(created.id, "Test")
    assert updated.id != None
    assert updated.title == "Test"

    #DELETE 
    lesson.delete(created.id)

    created = lesson.get(created.id)
    read = lesson.get(read.id)
    updated = lesson.get(updated.id)

    assert created == None
    assert read == None
    assert updated == None
    

def test_goalCRUD():
    user_id = user.id("timothy")
    goal_course = course.create(user_id, "Test Course", "This is a test course")

    #CREATE
    created = goal.create(goal_course.id, 'NOTEBOOK', 100)
    assert created.id != None
    assert created.goal == 0
    assert created.complete == False
    assert created.metric == 100
   
    #READ
    read = goal.get(created.id)
    assert created.id != None
    assert created.goal == 0 
    assert created.complete == False
    assert created.metric == 100

    #UPDATE 
    updated = goal.update(created.id, 'QUESTION', True, 20)
    assert created.id != None
    assert created.goal == 1
    assert created.complete == True
    assert created.metric == 20

    #DELETE
    goal.delete(created.id)

    created = goal.get(created.id)
    read = goal.get(read.id)
    updated = goal.get(updated.id)

    assert created == None
    assert read == None
    assert updated == None

def test_textbook():
    user_id = user.id("timothy")
    textbook_course = course.create(user_id, "Test Course", "This is a test course")
    
    #CREATE
    created = textbook.create(textbook_course.id, "Book of Proof", "9780989472128", "Richard Hammack", 368, "blah")

    assert created.id != None
    assert created.title == "Book of Proof"
    assert created.isbn == "9780989472128"
    assert created.author == "Richard Hammack"
    assert created.pages == 368
    assert created.filename == "blah"

    #CREATE ISBN10

    created_isbn = textbook.create(textbook_course.id, "Book of Proof", "0989472128", "Richard Hammack", 368, "blah")

    assert created_isbn.id != None
    assert created_isbn.title == "Book of Proof"
    assert created_isbn.isbn == "9780989472128"
    assert created_isbn.author == "Richard Hammack"
    assert created_isbn.pages == 368
    assert created_isbn.filename == "blah"

    #CREATE EMPTY

    created_empty = textbook.create(textbook_course.id)

    assert created_empty.id != None
    assert created_empty.title == None
    assert created_empty.isbn == None
    assert created_empty.author == None
    assert created_empty.pages == 0
    assert created_empty.filename == None

    #READ
    read = textbook.get(created.id)

    assert read.id != None
    assert read.title == "Book of Proof"
    assert read.isbn == "9780989472128"
    assert read.author == "Richard Hammack"
    assert read.pages == 368

    #UPDATE 
    updated = textbook.update(created.id, "Basic Mathematics", "9780387967875", "Serge Lang", 431)

    assert updated.id != None
    assert updated.title == "Basic Mathematics"
    assert updated.isbn == "9780387967875"
    assert updated.author == "Serge Lang"
    assert updated.pages == 431

    #DELETE
    textbook.delete(created.id)

    created = textbook.get(created.id)
    read = textbook.get(read.id)
    updated = textbook.get(updated.id)

    assert created == None
    assert read == None
    assert updated == None

def test_textbookSectionCRUD():
    user_id = user.id("timothy")
    textbook_course = course.create(user_id, "Test Course", "This is a test course")
    section_lesson = lesson.create(textbook_course.id, "Sets")
    section_textbook = textbook.create(textbook_course.id, "Book of Proof", "9780989472128", "Richard Hammack", 368, "blah")

    #CREATE
    created = textbook_section.create(textbook_course.id, section_lesson.id, section_textbook.id, start_page=3, end_page=32)
    assert created.id != None
    assert created.course_id == textbook_course.id
    assert created.lesson_id == section_lesson.id
    assert created.textbook_id == section_textbook.id
    assert created.start_page == 3
    assert created.end_page == 32

    #CREATE EMPTY
    created_empty = textbook_section.create(textbook_course.id, section_lesson.id, section_textbook.id)
    assert created_empty.id != None
    assert created_empty.course_id == textbook_course.id
    assert created_empty.lesson_id == section_lesson.id
    assert created_empty.textbook_id == section_textbook.id
    assert created_empty.start_page == None
    assert created_empty.end_page == None

    #READ
    read = textbook_section.get(created.id)
    assert read.id != None
    assert read.course_id == textbook_course.id
    assert read.lesson_id == section_lesson.id
    assert read.textbook_id == section_textbook.id
    assert read.start_page == 3
    assert read.end_page == 32

    #UPDATE

    section_lesson2 = lesson.create(textbook_course.id, "Logic")
    section_textbook2 = textbook.create(created.id, "Basic Mathematics", "9780387967875", "Serge Lang", 431)
    updated = textbook_section.update(created.id, section_lesson2.id, section_textbook2.id, 93, 106)
    
    assert updated.id != None
    assert updated.course_id == textbook_course.id
    assert updated.lesson_id == section_lesson2.id
    assert updated.textbook_id == section_textbook2.id
    assert updated.start_page == 93 
    assert updated.end_page == 106

    #DELETE
    textbook_section.delete(created.id)

    created = textbook_section.get(created.id)
    read = textbook_section.get(read.id)
    updated = textbook_section.get(updated.id)

    assert created == None
    assert read == None
    assert updated == None

def test_notebookCRUD():
    user_id = user.id("timothy")
    notebook_course = course.create(user_id, "Test Course", "This is a test course")

    notebook_lesson = lesson.create("Algebra")
    
    #CREATE
    created = notebook.create(notebook_course.id, notebook_lesson.id, "<b>One</p>")
    assert created.id != None
    assert created.lesson_id == notebook_lesson.id
    assert created.course_id == notebook_course.id
    assert created.body == "<b>One</p>"

    #READ
    read = notebook.getByLesson(notebook_lesson.id)
    assert read.id != None
    assert read.lesson_id == notebook_lesson.id
    assert read.course_id == notebook_course.id
    assert created.body == "<b>One</p>"

    #UPDATE
    updated = notebook.update(created.id, created.course_id, created.lesson_id, "<b>Two</b>")
    assert updated.id != None
    assert updated.lesson_id == notebook_lesson.id
    assert updated.course_id == notebook_course.id
    assert updated.body == "<b>Two</b>"

    #DELETE
    notebook.delete(created.id)

    created = notebook.getSection(created.id)
    read = notebook.getSection(read.id)
    updated = notebook.getSection(updated.id)

    assert created == None
    assert read == None
    assert updated == None
