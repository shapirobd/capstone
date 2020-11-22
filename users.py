import requests
import pdb
import os

import mtgsdk
import flask_paginate

from app import g
from flask import Flask, Blueprint, session, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Friendship, Card, Bookmark, Deck, CardDeck, Post, bcrypt
from forms import LoginForm, RegisterForm, DeckForm, EditUserForm, NewPostForm

users_blueprint = Blueprint('users_blueprint', __name__, static_folder='static',
                            template_folder='templates')

CURR_USER_KEY = 'curr-user'


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:

        user = User.query.get(session[CURR_USER_KEY])
        del session[CURR_USER_KEY]
        # flash(f"Goodbye, {user.username}!")


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: Renders the template for a user to login
    POST: Submits register form and creates new user & logs in
    """
    if g.user:
        return redirect('/home')

    form = RegisterForm()

    if form.validate_on_submit():
        return handle_register_form_errors(form)
    return render_template('register.html', form=form)


def handle_register_form_errors(form):
    """Determines & handles errors found in register user form. If no errors found, creates new user."""
    if User.query.get(form.username.data):
        flash(
            f'The username "{form.username.data}" is already taken', 'danger')
        return redirect('/register')
    if len(User.query.filter(User.email == form.email.data).all()) > 0:
        flash('That email address is already taken', 'danger')
        return redirect('/register')
    if not check_confirmed_pwd(form.password.data, form.confirmed_password.data):
        flash('Passwords must match - please try again.', 'danger')
        return redirect('/register')
    return complete_register(form)


def complete_register(form):
    """Creates a new user from the form data and logs that user in"""
    image_url = form.image_url.data or "/static/images/default_prof_pic.png"
    if User.signup(username=form.username.data, password=form.password.data,
                   email=form.email.data, image_url=image_url):
        db.session.commit()
        session[CURR_USER_KEY] = form.username.data
        return redirect('/home')
    return redirect('/login')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: Renders the template for a user to login
    POST: Submits login form and signs in user if correct username & password
    """
    if g.user:
        return redirect('/home')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data, password=form.password.data)
        if user:
            db.session.add(user)
            db.session.commit()
            session[CURR_USER_KEY] = form.username.data
            return redirect('/home')
        flash('Username or password is incorrect', 'danger')
        return redirect('/login')
    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
def logout():
    """Logs out a user and redirets them to the login page"""
    if g.user:
        do_logout()
    return redirect('/login')


def check_confirmed_pwd(pwd, confirmed_pwd):
    """Checks that the confirmed password matches upon registering"""
    if pwd != confirmed_pwd:
        return False
    return True


@users_blueprint.route('/users/<string:username>', methods=['GET', 'POST'])
def user_profile(username):
    """
    GET: Route for viewing a user's profile
    POST: Create a new Post instance and put it on your page
    """
    if g.user:
        form = NewPostForm()
        if g.user.username == username:
            if form.validate_on_submit():
                post = Post(username=username, title=form.title.data,
                            content=form.content.data)
                db.session.add(post)
                db.session.commit()
                return redirect(f'/users/{username}')
        user = User.query.get(username)
        return render_template('user.html', user=user, form=form)
    return redirect('/login')


@users_blueprint.route('/users/<string:username>/edit', methods=['GET', 'POST'])
def edit_profile(username):
    """
    GET: Route for editting your profile
    POST: Update the user's data
    """
    if g.user:
        form = EditUserForm()
        user = User.query.get(g.user.username)

        if form.validate_on_submit():
            user.email = form.email.data
            user.image_url = form.image_url.data or "/static/images/default_prof_pic.png"
            if check_confirmed_pwd(form.password.data, form.confirmed_password.data):
                user.password = bcrypt.generate_password_hash(
                    form.password.data).decode('UTF-8')
            else:
                flash('Passwords do not match - please try again.', 'danger')
                return redirect(f'/users/{user.username}/edit')

            db.session.add(user)
            db.session.commit()
            return redirect('/home')

        populate_edit_profile_fields(form, user)
        return render_template('edit_user.html', form=form)
    return render_template('/login')


def populate_edit_profile_fields(form, user):
    """Populates edit user form fields"""
    form.email.data = user.email
    form.password.data = user.password
    form.confirmed_password.data = user.password
    form.image_url.data = user.image_url
