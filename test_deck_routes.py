from app import app, CURR_USER_KEY
import mtgsdk
import os
from unittest import TestCase
from users import check_confirmed_pwd
from flask import g
from models import db, User, Card, Deck, bcrypt
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

os.environ['DATABASE_URL'] = "postgresql:///mtg_db_test"


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

    def tearDown(self):
        db.session.rollback()

    def test_view_decks(self):
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
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username

            resp = c.get(f'/decks/{self.deck1.id}')

            self.assertEqual(resp.status_code, 200)
    # def test_delete_deck(self):
    # def test_create_deck(self):

    def test_add_to_deck(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username

            card = mtgsdk.Card.where(name='Abundance').all()[0]
            new_card = Card(name=card.name, card_type=card.type,
                            colors=card.colors, rarity=card.rarity, set_name=card.set_name)
            db.session.add(new_card)
            db.session.commit()
            print(card)
            resp = c.post(f'/cards/{new_card.id}/decks/{self.deck1.id}',
                          follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
    # def test_delete_from_deck(self):
    # def test_show_users_deck(self):
