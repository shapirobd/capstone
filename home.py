import requests
import pdb
import os
import json
import mtgsdk
import flask_paginate

from app import g
from flask import Flask, Blueprint, session, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Friendship, Message, Card, Bookmark, Deck, CardDeck, Post
from forms import LoginForm, RegisterForm, TypeForm, DeckForm, EditUserForm, ColorForm, RarityForm, SetForm

home_blueprint = Blueprint('home_blueprint', __name__, static_folder='static',
                           template_folder='templates')

CURR_USER_KEY = 'curr-user'

TYPES = ['Artifact', 'Conspiracy', 'Creature', 'Enchantment', 'Instant', 'Land',
         'Phenomenon', 'Plane', 'Planeswalker', 'Scheme', 'Sorcery', 'Tribal', 'Vanguard']
# SETS = [mtg_set.name for mtg_set in mtgsdk.Set.all()]
SETS = ['Tenth Edition']
RARITIES = ['Common', 'Uncommon', 'Rare', 'Mythic Rare']
COLORS = ['White', 'Blue', 'Black', 'Green', 'Red']


def generate_forms():
    type_form = TypeForm()
    type_form.card_type.choices = TYPES

    color_form = ColorForm()
    color_form.color.choices = COLORS

    rarity_form = RarityForm()
    rarity_form.rarity.choices = RARITIES

    set_form = SetForm()
    set_form.set_name.choices = SETS

    # power_form = PowerForm()
    # toughness_form = ToughnessForm()

    return [type_form, color_form, rarity_form, set_form]


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
    base_url = '/home?'
    page = determine_page(request.args)
    index_range = determine_index_range(page)
    cards = Card.query.filter((Card.id + 1).in_(index_range)).all()

    return render_homepage(base_url=base_url, page=page, index_range=index_range, cards=cards)


@ home_blueprint.route('/home/search')
def search():

    term = request.args['term']
    category = request.args['category']

    if category == 'card':
        return render_card_search(term, category, request.args)

    elif category == 'deck':
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

    else:
        return


def render_card_search(term, category, req_args):

    base_url = f'/home/search?term={term}&category={category}&'

    page = determine_page(request.args)
    index_range = determine_index_range(page)

    all_cards = Card.query.filter(
        Card.name.ilike(f'%{term}%')).all()

    cards = [card for card in all_cards if (all_cards.index(
        card) + 1) in index_range]
    if len(cards) == 0:
        flash('No results found.', 'danger')
    return render_homepage(base_url=base_url, page=page, index_range=index_range, cards=cards)


@home_blueprint.route('/home/filter')
def filter_cards():

    types = generate_filter_terms('card_type', TYPES, request.args)
    sets = generate_filter_terms('set_name', SETS, request.args)
    colors = generate_filter_terms('colors', COLORS, request.args)
    rarities = generate_filter_terms('rarities', RARITIES, request.args)

    base_url = f'/home/filter?card_type={types}&sets={sets}&colors={colors}&rarities={rarities}&'

    page = determine_page(request.args)
    index_range = determine_index_range(page)

    filtered_cards = generate_filtered_cards(
        types, sets, colors, rarities, index_range)

    return render_homepage(base_url=base_url, page=page, index_range=index_range, cards=filtered_cards)

# ADD base_url, page, index_range


def render_homepage(cards, base_url, page, index_range):
    decks = Deck.query.all()

    bookmarks = Bookmark.query.all()
    bookmarked_card_ids = [bookmark.card_id for bookmark in bookmarks]

    forms = generate_forms()

    type_form = forms[0]
    color_form = forms[1]
    rarity_form = forms[2]
    set_form = forms[3]
    # power_form = forms[4]
    # toughness_form = forms[5]
    if len(cards) == 0:
        flash('No results found.', 'danger')
    return render_template('home.html', page=page, base_url=base_url, cards=cards, decks=decks, type_form=type_form, color_form=color_form, rarity_form=rarity_form, set_form=set_form, bookmarked_card_ids=bookmarked_card_ids)


def generate_filter_terms(category, default_terms, req_args):
    terms = default_terms
    if category in req_args and len(req_args[category]) > 0:
        terms = req_args[category].split(',')
    return terms


def determine_page(req_args):
    page = 1
    if 'page' in req_args:
        page = int(req_args['page'])
    return page


def determine_index_range(page):
    first_card_index = ((page-1)*100) + 1
    last_card_index = (page*100) + 1
    index_range = range(first_card_index, last_card_index)
    return index_range


def generate_filtered_cards(types, sets, colors, rarities, index_range):
    filtered_cards = Card.query.filter(Card.card_type.in_(types) & Card.set_name.in_(
        sets) & Card.colors.in_(colors) & Card.rarity.in_(rarities)).all()
    return [card for card in filtered_cards if (
        filtered_cards.index(card) + 1) in index_range]
