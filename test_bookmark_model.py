from app import app
import os
from unittest import TestCase
import requests

from models import db, User, Card, Bookmark, Deck, bcrypt
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

os.environ['DATABASE_URL'] = "postgresql:///mtg_db_test"


class BookmarkModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.user = User.signup(email='email@gmail.com', password='userpassword', username='usernametest',
                                image_url=None)

        self.resp = requests.get('http://api.magicthegathering.io/v1/cards', {
            'key': "$2a$10$TNyqKQQQSzVjgGXY87waZuBIKAS78.NkY2o.H004TfBU.eISv.Pt6",
            'page': 1
        }).json()

        self.cards = self.resp['cards']

        Card.create_all_cards(self.cards)
        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_bookmark_model(self):
        bookmark = Bookmark(username=self.user.username,
                            card_id=1)
        db.session.add(bookmark)
        db.session.commit()
        print(bookmark.username)
        # ^^ THIS PRINTS 'usernametest', SO I HAVE NO IDEA WHY THE BELOW ASSERTION IS NOT WORKING (IT JUST PAUSES INFINITELY WITH NO OUTPUT). COULD NOT FIND A SOLUTION ONLINE
        print(bookmark.card_id)
        # ^^ THIS PRINTS '1', SO I HAVE NO IDEA WHY THE BELOW ASSERTION IS NOT WORKING (IT JUST PAUSES INFINITELY WITH NO OUTPUT). COULD NOT FIND A SOLUTION ONLINE
        self.assertEqual(bookmark.username, 'usernametest')
        self.assertEqual(bookmark.card_id, 1)
