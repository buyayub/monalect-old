from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static/')

@app.route("/")
def home():
    return render_template("landing.j2")

@app.route("/about")
def about():
    return render_template("about.j2")

@app.route("/docs")
def docs():
    return render_template("docs.j2")

@app.route("/contact")
def contact():
    return render_template("contact.j2")

@app.route("/monalect/")
def monalect():
    return render_template("monalect.j2")

@app.route("/monalect/create")
def create():
    return render_template("create.j2")

@app.route("/monalect/<course>/overview")
def course(course):
    return render_template("course.j2")

@app.route("/monalect/<course>/notebook")
def notebook(course):
    return render_template("notebook.j2")

@app.route("/monalect/<course>/textbook")
def textbook(course):
    return render_template("textbook.j2")

@app.route("/monalect/<course>/questions/")
def questions(course):
    return render_template("questions.j2")

@app.route("/monalect/<course>/test")
def test(course):
    return render_template("test.j2")
