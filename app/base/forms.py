# -*- encoding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired

## login and registration

class LoginForm(FlaskForm):
    username = StringField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = StringField('Username'     , id='username_create' , validators=[DataRequired()])
    email    = StringField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])
class MovieForm(FlaskForm):
    mychoices = ['2016','2017','2018','2019','2020','2021','2022']
    movie = SelectField ('Movie',choices=mychoices, id='mtitle'   , validators=[DataRequired()])

class PopupForm(FlaskForm):
    movie = StringField ('Title', id='movie_title')