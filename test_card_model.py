from app import app
import os
from unittest import TestCase
import requests

from models import db, User, Card, Bookmark, bcrypt
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

os.environ['DATABASE_URL'] = "postgresql:///mtg_db_test"


class CardModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.create_all()

        self.client = app.test_client()

        self.resp = requests.get('http://api.magicthegathering.io/v1/cards', {
            'key': "$2a$10$TNyqKQQQSzVjgGXY87waZuBIKAS78.NkY2o.H004TfBU.eISv.Pt6",
            'page': 1
        }).json()
        print(self.resp)
        self.cards = self.resp['cards']
        print(self.cards)
        Card.create_all_cards(self.cards)
        print('Cards Created')
        db.session.commit()

        self.card = Card.query.filter(Card.name == 'Abundance').first()

    def tearDown(self):
        db.drop_all()

    def test_card_model(self):
        # <-- THIS PRINTS 'Abundance', SO I HAVE NO IDEA WHY THE BELOW ASSERTION IS NOT WORKING (IT JUST PAUSES INFINITELY WITH NO OUTPUT). COULD NOT FIND A SOLUTION ONLINE
        print(self.card.name)
        self.assertEqual(self.card.name, 'Abundance')
