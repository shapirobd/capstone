from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, RadioField, SelectField, FileField, TextAreaField
from wtforms.validators import InputRequired, Length, Email
from wtforms.widgets import CheckboxInput, ListWidget
import email_validator


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[
                        InputRequired(), Email("Invalid email address")])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=8)])
    confirmed_password = PasswordField(
        "Confirm Password", validators=[InputRequired()])
    image_url = StringField('Profile Picture')


class EditUserForm(FlaskForm):
    email = StringField('Email', validators=[
                        InputRequired(), Email("Invalid email address")])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=8)])
    confirmed_password = PasswordField(
        "Confirm Password", validators=[InputRequired()])
    image_url = StringField('Profile Picture')


class DeckForm(FlaskForm):
    deck_name = StringField('Name', validators=[InputRequired()])
    deck_type = SelectField('Deck Type')


class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[
        InputRequired()])
    content = TextAreaField('Content', validators=[
        InputRequired()])
