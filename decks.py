import requests
import pdb
import os

import mtgsdk
import flask_paginate

# from mtgsdk import Type
from app import g
from flask import Flask, Blueprint, session, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Card, Bookmark, Deck, CardDeck
from forms import DeckForm

decks_blueprint = Blueprint('decks_blueprint', __name__, static_folder='static',
                            template_folder='templates')

CURR_USER_KEY = 'curr-user'


@decks_blueprint.route('/decks', methods=['GET', 'POST'])
def view_decks():
    """Route for viewing your own decks"""
    if g.user:
        user = g.user
        decks = g.user.decks
        return render_template('decks.html', decks=decks, user=user)
    return redirect('/login')


@decks_blueprint.route('/decks/<int:deck_id>')
def show_deck(deck_id):
    """Route for viewing contents of deck"""
    if g.user:
        deck = Deck.query.get(deck_id)

        bookmarks = Bookmark.query.all()
        bookmarked_card_ids = [bookmark.card_id for bookmark in bookmarks]
        return render_template('deck.html', deck=deck, bookmarked_card_ids=bookmarked_card_ids)
    return redirect('/login')


@decks_blueprint.route('/decks/<int:deck_id>/delete', methods=['POST'])
def delete_deck(deck_id):
    """Route for deleting a deck"""
    if g.user:
        deck = Deck.query.get(deck_id)
        db.session.delete(deck)
        db.session.commit()
        return redirect('/decks')
    return redirect('/login')


@decks_blueprint.route('/new', methods=['GET', 'POST'])
def create_deck():
    """Route for creating a deck"""
    if g.user:
        form = DeckForm()
        form.deck_type.choices = ['Standard', 'Commander']

        if form.validate_on_submit():
            """If this is a post request, created a new deck instance"""
            deck = Deck(deck_name=form.deck_name.data,
                        deck_type=form.deck_type.data, username=session[CURR_USER_KEY])

            if 'card-to-add' in request.args:
                card_id = int(request.args['card-to-add'])
                card_to_add = Card.query.get(card_id)
                deck.cards.append(card_to_add)

            db.session.add(deck)
            db.session.commit()

            return redirect('/decks')
        return render_template('new_deck.html', form=form)
    return redirect('/login')


@decks_blueprint.route('/cards/<int:card_id>/decks/<int:deck_id>', methods=['POST'])
def add_to_deck(card_id, deck_id):
    """Route for adding a card to your deck"""
    if g.user:
        card = Card.query.get(card_id)
        deck = Deck.query.get(deck_id)

        deck.cards.append(card)

        db.session.commit()
        return redirect('/home')
    return redirect('/login')


@decks_blueprint.route('/cards/<int:card_id>/decks/<int:deck_id>/delete', methods=['POST'])
def delete_from_deck(card_id, deck_id):
    """Route for deleting a card from your deck"""
    if g.user:
        card_deck = CardDeck.query.filter(
            CardDeck.card_id == card_id and CardDeck.deck_id == deck_id).first()

        db.session.delete(card_deck)
        db.session.commit()

        return redirect(f'/decks/{deck_id}')
    return redirect('/login')


@decks_blueprint.route('/users/<string:username>/decks')
def show_users_decks(username):
    """Route for viewing someone else's decks"""
    user = User.query.get(username)
    decks = user.decks
    return render_template('decks.html', decks=decks, user=user)
