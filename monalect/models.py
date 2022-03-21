from sqlalchemy import Column,String,Date,Integer,Text,SmallInteger,Boolean,CheckConstraint,ForeignKey
from sqlalchemy.sql import func
import bcrypt, secrets, string
from monalect.database import Base

class User(Base):
    __tablename__ = 'users'

    MEMBER = {'NONE' : 0, 'BASIC' :  1, 'PRO' : 2 }

    id = Column(String(32), primary_key=True, unique=True,nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    email = Column(Text, unique=True)
    membership = Column(SmallInteger, CheckConstraint('membership in (0, 1, 2)'), default=0)
    joined = Column(Date, unique=True, default=func.now())
    passhash = Column(Text, nullable=False)

class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    user_id = Column(String(32), ForeignKey("users.id"), nullable=False)
    created = Column(Date, nullable=False, default=func.now())
    title = Column(String(255))
    description = Column(Text) 

class Lesson(Base):
    __tablename__ = 'lesson'
    
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    title = Column(String(255), nullable=False)

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    lesson = Column(Integer, ForeignKey("lesson.id"), nullable=False)
    question = Column(Text)
    answer = Column(Text)

class Textbook(Base):
    __tablename__ = 'textbook'
    
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    filename = Column(String(16))
    author = Column(String(255))
    isbn = Column(String(13)) #remember to convert ISBN-10 to ISBN-13
    title = Column(String(255), default=None)
    pages = Column(Integer, default=0)

class TextbookSection(Base):
    __tablename__ = 'textbook_section'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lesson.id"), nullable=False)
    textbook_id = Column(Integer, ForeignKey("textbook.id"), nullable=False)
    start_page = Column(Integer)
    end_page = Column(Integer)

class NotebookSection(Base):
    __tablename__  = 'notebook_section'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    lesson_id = Column(Integer, ForeignKey("lesson.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    body = Column(Text)

class Goal(Base):
    __tablename__ = 'goal'

    TYPE = {'NOTEBOOK' : 0, 'QUESTION' : 1, 'TEST' : 2}

    id = Column(Integer, primary_key=True, unique=True)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    goal = Column(SmallInteger, CheckConstraint('goal in (0, 1, 2)'))
    complete = Column(Boolean)
    metric = Column(Integer)

class Session(Base):
    __tablename__ = 'session'

    id = Column(String(32), primary_key=True, unique=True, nullable=False)
    user_id = Column(String(32), ForeignKey("users.id"), unique=True, nullable=False)
    expiry_date = Column(Date, nullable=False)

class LoginAttempts(Base):
    __tablename__ = 'login_attempts'
    
    user_id = Column(String(32), ForeignKey("users.id"), primary_key=True, unique=True, nullable=False)
    attempts = Column(Integer, nullable=False, default=0)
