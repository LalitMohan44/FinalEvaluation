from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from lookup import *


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    ContactNo = StringField("ContactNo",
                            validators=[DataRequired(), Length(min=10, max=10)])
    notice = StringField('Notice Period',
                         validators=[DataRequired()])
    skills = StringField('Skills',
                         validators=[DataRequired()])
    jobid = IntegerField('JobID',
                         validators=[DataRequired(), NumberRange(100001, 100007)])
    picture = FileField('Update Your Resume', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class InterLoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class Search(FlaskForm):
    selectS = SelectField('Select Skills:', choices=skill)
    selectJ = SelectField('Select Job ID:', choices=job)
    selectN = StringField('Notice Period:')
    selectR = SelectField('Select Round:', choices=result2)
    selectT = SelectField('Select Status:', choices=result3)
    submit = SubmitField('Select')


class Track(FlaskForm):
    selectC = SelectField('Select Candidate:', choices=name)
    selectR = SelectField('Select Round:', choices=result2)
    selectS = SelectField('Select Status:', choices=result3)
    submit = SubmitField('Update')
