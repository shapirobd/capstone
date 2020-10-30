from app import app, CURR_USER_KEY
import mtgsdk
import os
from unittest import TestCase
from users import check_confirmed_pwd
from flask import g
from models import db, User, Card, Deck, bcrypt
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///mtg_db_test'))


class DeckRoutesTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.user1 = User.signup(email='email1@gmail.com', password='user1password', username='username_1',
                                 image_url=None)
        print(self.user1)
        self.deck1 = Deck(username=self.user1.username,
                          deck_name='Test Deck', deck_type='Standard')
        db.session.add(self.deck1)
        db.session.commit()
        print(self.deck1)

    # def tearDown(self):
    #     db.session.rollback()

    def test_view_decks(self):
        """Test that route for viewing your own decks works"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username

            resp = c.get('/decks')
            print(resp)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<h4 class="card-title mt-2">Test Deck</h4>', str(resp.data))
            self.assertIn(
                '<h6 class="">Standard</h6>', str(resp.data))

    def test_show_deck(self):
        """Test that route for viewing contents of your own deck works"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username

            resp = c.get(f'/decks/1')

            self.assertEqual(resp.status_code, 200)

    def test_delete_deck(self):
        """Test that route for deleting a deck works"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username
            resp = c.post(f'/decks/1/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

    def test_add_to_deck(self):
        """Test that route for adding a card to your deck works"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username

            card = mtgsdk.Card.where(name='Abundance').all()[0]
            new_card = Card(name=card.name, card_type=card.type,
                            colors=card.colors, rarity=card.rarity, set_name=card.set_name)
            db.session.add(new_card)
            db.session.commit()
            print(card)
            resp = c.post(f'/cards/{new_card.id}/decks/1',
                          follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

    def test_delete_from_deck(self):
        """Test that route for removing a card from your deck works"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username

            card = mtgsdk.Card.where(name='Abundance').all()[0]
            new_card = Card(name=card.name, card_type=card.type,
                            colors=card.colors, rarity=card.rarity, set_name=card.set_name)
            db.session.add(new_card)
            db.session.commit()
            c.post(f'/cards/1/decks/1',
                   follow_redirects=True)
            resp = c.post(f'/cards/1/decks/1/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

    def test_show_users_deck(self):
        """Test that route for showing a user's deck works"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username

            resp = c.get(f'/users/{self.user1.username}/decks')
            self.assertEqual(resp.status_code, 200)
