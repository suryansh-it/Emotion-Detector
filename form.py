from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class Signupform(FlaskForm):
    username = StringField('Username' , validators=[DataRequired()])
    email = StringField('Email' , validators=[DataRequired(),Email()])
    password = PasswordField('Password' , validators=[DataRequired()])
    confirm_password = StringField('Confirm Password' , validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    