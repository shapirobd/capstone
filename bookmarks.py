import requests
import pdb
import os

import mtgsdk
import flask_paginate

# from mtgsdk import Type
from app import g
from flask import Flask, session, Blueprint, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Friendship, Card, Bookmark, Deck, CardDeck, Post
from forms import LoginForm, RegisterForm, DeckForm, EditUserForm

bookmarks_blueprint = Blueprint('bookmarks_blueprint', __name__, static_folder='static',
                                template_folder='templates')

CURR_USER_KEY = 'curr-user'


@bookmarks_blueprint.route('/cards/<int:card_id>/bookmark', methods=['GET', 'POST'])
def add_bookmark(card_id):
    """Route for bookmarking a card"""
    if g.user:
        """If this is a post request, create a new bookmark instance"""
        bookmark = Bookmark(card_id=card_id, username=session[CURR_USER_KEY])
        db.session.add(bookmark)
        db.session.commit()
        return redirect('/home')
    flash('Permission denied - must be logged in to bookmark a card.')
    return redirect('/login')


@bookmarks_blueprint.route('/cards/<int:card_id>/unbookmark', methods=['GET', 'POST'])
def remove_bookmark(card_id):
    """Route for unbookmarking a card"""
    if g.user:
        bookmark = Bookmark.query.filter(Bookmark.card_id == card_id).first()
        db.session.delete(bookmark)
        db.session.commit()
        return redirect('/home')
    flash('Permission denied - must be logged in to bookmark a card.')
    return redirect('/login')


@bookmarks_blueprint.route('/bookmarks')
def show_bookmarked_cards():
    """Route for showing your bookmarked cards"""
    if g.user:
        bookmarked_cards = g.user.bookmarked_cards
        decks = Deck.query.all()

        bookmarked_card_ids = [
            bookmarked_card.id for bookmarked_card in bookmarked_cards]

        return render_template('bookmarks.html', bookmarked_cards=bookmarked_cards, decks=decks, bookmarked_card_ids=bookmarked_card_ids)
    return redirect('/login')
