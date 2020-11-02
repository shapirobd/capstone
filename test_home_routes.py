from app import app, CURR_USER_KEY
import os
from unittest import TestCase
import requests
from home import determine_page, determine_index_range, render_homepage
from models import db, User, Card, Deck

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///mtg_db_test'))


class HomeRoutesTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.user1 = User.signup(email='email1@gmail.com', password='user1password', username='username_1',
                                 image_url=None)
        self.user2 = User.signup(email='email2@gmail.com', password='user2password', username='username_2',
                                 image_url=None)

        self.user1.friends.append(self.user2)

        self.deck = Deck(deck_name='Test Deck',
                         deck_type='Standard', username='username_1')

        self.user1.decks.append(self.deck)

        self.card = Card(name='Test Name', text='Sample Text', card_type='Creature', power='1',
                         toughness='2', colors='Blue', rarity='Common', set_name='Tenth Edition')
        db.session.add(self.card)

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_determine_page(self):
        """Test that determine_page function works"""
        req_args = {'page': 1}
        page = determine_page(req_args)
        self.assertEquals(page, 1)

    def test_determine_index_range(self):
        """Test that determine_index_range function works"""
        index_range = determine_index_range(2)
        self.assertEqual(index_range, range(101, 201))

    def test_welcome(self):
        """Test that root route takes you to welcome page when no user is logged in"""
        with self.client as c:
            c.get('/logout')
            resp = c.get('/')

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                'Welcome to MTG Deck Builder!', str(resp.data))

    def test_show_homepage(self):
        """Test that root route takes you to home page when user is logged in"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username
            resp = c.get('/', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Logout', str(resp.data))
            self.assertIn('Show Info', str(resp.data))
            self.assertIn('Add to Deck', str(resp.data))

    def test_search_card_exact(self):
        """Test that the search route for a card gives the proper result (using exact term)"""
        with self.client as c:
            resp = c.get('/home/search?category=card&term=Test+Name')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Show Info', str(resp.data))
            self.assertIn('Add to Deck', str(resp.data))
            self.assertIn('<div class="collapse" id="info-1">', str(resp.data))
            self.assertIn(
                '<h5 class="card-title">Test Name</h5>', str(resp.data))
            self.assertIn(
                '<small>Test Name</small>', str(resp.data))

    def test_search_card_substring(self):
        """Test that the search route for a card gives the proper result (using substring/casefold)"""
        with self.client as c:
            resp = c.get('/home/search?category=card&term=teSt')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Show Info', str(resp.data))
            self.assertIn('Add to Deck', str(resp.data))
            self.assertIn('<div class="collapse" id="info-1">', str(resp.data))
            self.assertIn(
                '<h5 class="card-title">Test Name</h5>', str(resp.data))
            self.assertIn('<small>Test Name</small>', str(resp.data))

    def test_search_user_exact(self):
        """Test that the search route for a user gives the proper result (using exact term)"""
        with self.client as c:
            resp = c.get('/home/search?category=user&term=username_1')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('View Profile', str(resp.data))
            self.assertIn('View Decks', str(resp.data))
            self.assertIn(
                '<h3>username_1</h3>', str(resp.data))

    def test_search_user_substring(self):
        """Test that the search route for a user gives the proper result (using substring/casefold)"""
        with self.client as c:
            resp = c.get('/home/search?category=user&term=Usern')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('View Profile', str(resp.data))
            self.assertIn('View Decks', str(resp.data))
            self.assertIn(
                '<h3>username_1</h3>', str(resp.data))

    def test_search_friend_exact(self):
        """Test that the search route for a friend gives the proper result (using exact term)"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 'username_1'
            resp = c.get('/home/search?category=friend&term=username_2')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('View Profile', str(resp.data))
            self.assertIn('View Decks', str(resp.data))
            self.assertIn(
                '<h3>username_2</h3>', str(resp.data))

    def test_search_friend_substring(self):
        """Test that the search route for a friend gives the proper result (using substring/casefold)"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 'username_1'
            resp = c.get('/home/search?category=friend&term=Usern')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('View Profile', str(resp.data))
            self.assertIn('View Decks', str(resp.data))
            self.assertIn(
                '<h3>username_2</h3>', str(resp.data))

    def test_search_deck_exact(self):
        """Test that the search route for a deck gives the proper result (using exact term)"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 'username_1'
            resp = c.get('/home/search?category=decks&term=Test+Deck')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('View Deck', str(resp.data))
            self.assertIn(
                '<h4 class="card-title mt-2">Test Deck</h4>', str(resp.data))

    def test_search_deck_substring(self):
        """Test that the search route for a deck gives the proper result (using substring/casefold)"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 'username_1'
            resp = c.get('/home/search?category=decks&term=tEsT+D')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('View Deck', str(resp.data))
            self.assertIn(
                '<h4 class="card-title mt-2">Test Deck</h4>', str(resp.data))
