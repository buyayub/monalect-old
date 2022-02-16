from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, TextAreaField, StringField, validators

class RegisterForm(Form):
    username = StringField('username', [validators.DataRequired(), validators.Length(max=255)])
    password = PasswordField('password', [validators.DataRequired(),validators.Length(min=8)])
    email = StringField('email', [validators.DataRequired(), validators.Length(min=6, max=35)])
    recaptcha = RecaptchaField()
