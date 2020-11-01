import requests
import pdb
import os
import json
import mtgsdk
import flask_paginate
import math

from app import g
from flask import Flask, Blueprint, session, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Friendship, Card, Bookmark, Deck, CardDeck, Post
from forms import LoginForm, RegisterForm, DeckForm, EditUserForm

home_blueprint = Blueprint('home_blueprint', __name__, static_folder='static',
                           template_folder='templates')

CURR_USER_KEY = 'curr-user'


@ home_blueprint.route('/')
def welcome():
    """
    If we're not logged in, show the welcome page to login/signup.
    If we are logged in, show the user's home page.
    """
    if not g.user:
        return render_template('welcome.html')
    return redirect('/home')


@ home_blueprint.route('/home')
def show_homepage():
    """Route for showing the home page with nav bar and all cards paginated"""
    if g.user:
        base_url = '/home?'
        page = determine_page(request.args)
        index_range = determine_index_range(page)
        all_cards = Card.query.all()
        last_page = determine_last_page(all_cards)
        cards = Card.query.filter((Card.id + 1).in_(index_range)).all()

        return render_homepage(all_cards=all_cards, last_page=last_page, base_url=base_url, page=page, index_range=index_range, cards=cards)
    return redirect('/login')


@ home_blueprint.route('/home/search')
def search():
    """Route for showing all the cards/users/friends/decks resulting from a search"""
    term = request.args['term']
    category = request.args['category']

    if category == 'card':
        return search_cards(term, category, request.args)
    else:
        return handle_category(category, term)


def handle_category(category, term):
    """Executes the render_template function accordingly depending on the search category & term"""
    keyword = category
    if category == 'decks':
        decks = Deck.query.filter(
            (Deck.deck_name.ilike(f'%{term}%')) | (
                Deck.deck_type.ilike(f'%{term}%'))).all()
        if len(decks) == 0:
            flash('No results found.', 'danger')
        return render_template('decks.html', decks=decks)
    elif category == 'friend':
        friends = [friend for friend in g.user.friends if term.casefold()
                   in friend.username.casefold()]
        if len(friends) == 0:
            flash('No results found.', 'danger')
        return render_template('friends.html', friends=friends)
    elif category == 'user':
        users = [user for user in User.query.filter(
            User.username.ilike(f'%{term}%')).all()]
        if len(users) == 0:
            flash('No results found.', 'danger')
        return render_template('users.html', users=users)


def search_cards(term, category, req_args):
    """Executes the render_template function for cards specifically"""
    base_url = f'/home/search?term={term}&category={category}&'

    page = determine_page(request.args)
    index_range = determine_index_range(page)

    all_cards = Card.query.filter(
        Card.name.ilike(f'%{term}%')).all()

    last_page = determine_last_page(all_cards)

    cards = [card for card in all_cards if (all_cards.index(
        card) + 1) in index_range]
    return render_homepage(all_cards=all_cards, last_page=last_page, base_url=base_url, page=page, index_range=index_range, cards=cards)


def render_homepage(all_cards, last_page, cards, base_url, page, index_range):
    """Determines how the home page should be rendered depending on the results from previous functions"""
    decks = Deck.query.all()

    bookmarks = Bookmark.query.all()
    bookmarked_card_ids = [bookmark.card_id for bookmark in bookmarks]

    if len(cards) == 0:
        flash('No results found.', 'danger')
    return render_template('home.html', all_cards=all_cards, page=page, last_page=last_page, base_url=base_url, cards=cards, decks=decks, bookmarked_card_ids=bookmarked_card_ids)


def determine_page(req_args):
    """Determines which page of cards the user should be on"""
    page = 1
    if 'page' in req_args:
        page = int(req_args['page'])
    return page


def determine_index_range(page):
    """Determines the range of cards that should be on this page"""
    first_card_index = ((page-1)*100) + 1
    last_card_index = (page*100) + 1
    index_range = range(first_card_index, last_card_index)
    return index_range


def determine_last_page(cards):
    return math.ceil(len(cards)/100)
