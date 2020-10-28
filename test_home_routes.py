from app import app, CURR_USER_KEY
import os
from unittest import TestCase
import requests
from home import COLORS, generate_filter_terms, determine_page, determine_index_range, generate_filtered_cards, render_homepage
from models import db, User, Card

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///mtg_db_test'))


class HomeRoutesTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()

        card = Card(name='Test Name', text='Sample Text', card_type='Creature', power='1',
                    toughness='2', colors='Blue', rarity='Common', set_name='Tenth Edition')
        db.session.add(card)
        db.session.commit()

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()

        self.user1 = User.signup(email='email1@gmail.com', password='user1password', username='username_1',
                                 image_url=None)

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_generate_filter_terms(self):
        category = 'colors'
        default_terms = COLORS
        req_args = {}
        terms = generate_filter_terms(category, default_terms, req_args)
        print(terms)
        # ^^ THIS LINE PRINTS ['White', 'Blue', 'Black', 'Green', 'Red'], NOT SURE WHY THE BELOW ASSERTS WON'T WORK (THEY RUN INFINITELY AND NEVER COMPLETE)
        self.assertIn('White', terms)
        self.assertIn('Black', terms)
        self.assertIn('Red', terms)
        self.assertIn('Blue', terms)
        self.assertIn('Green', terms)

    def test_determine_page(self):
        req_args = {'page': 1}
        page = determine_page(req_args)
        print(page)
        # ^^ THIS LINE PRINTS 1, NOT SURE WHY THE BELOW ASSERT DOESN'T WORK (IT RUNS INFINITELY AND NEVER COMPLETES)
        self.assertEquals(page, 1)

    def test_determine_index_range(self):
        index_range = determine_index_range(2)
        self.assertEqual(index_range, range(101, 201))

    def test_generate_filtered_cards(self):
        for page in range(1, 10):
            resp = requests.get('http://api.magicthegathering.io/v1/cards', {
                'key': "$2a$10$TNyqKQQQSzVjgGXY87waZuBIKAS78.NkY2o.H004TfBU.eISv.Pt6",
                'page': page
            }).json()
            cards = resp['cards']
            Card.create_all_cards(cards)

        types = ['Instant']
        sets = ['Tenth Edition']
        colors = ['White', 'Black']
        rarities = ['Common', 'Uncommon']
        index_range = range(1, 101)

        filtered_cards = generate_filtered_cards(
            types, sets, colors, rarities, index_range)
        all_matching_cards = Card.query.filter(Card.card_type.in_(types) & Card.set_name.in_(
            sets) & Card.colors.in_(colors) & Card.rarity.in_(rarities)).all()

        filtered_cards_comparison = [
            card for card in all_matching_cards if all_matching_cards.index(card) in range(0, len(filtered_cards))]

        self.assertEqual(filtered_cards, filtered_cards_comparison)

    def test_welcome(self):
        with self.client as c:
            c.get('/logout')
            resp = c.get('/')

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                'Welcome to MTG Deck Builder!', str(resp.data))

    def test_show_homepage(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.username
            resp = c.get('/', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Logout', str(resp.data))
            self.assertIn('Type', str(resp.data))
            self.assertIn('Set', str(resp.data))
            self.assertIn('Rarity', str(resp.data))
            self.assertIn('Color', str(resp.data))
            self.assertIn('Show Info', str(resp.data))
            self.assertIn('Add to Deck', str(resp.data))

    def test_search(self):
        with self.client as c:
            resp = c.get('/home/search?category=card&term=Test+Name')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Show Info', str(resp.data))
            self.assertIn('Add to Deck', str(resp.data))
            self.assertIn('<div class="collapse" id="info-1">', str(resp.data))
            self.assertIn(
                '<h5 class="card-title">Test Name</h5>', str(resp.data))
            self.assertIn(
                '<p><b>name:</b> Test Name</p>', str(resp.data))

    def test_filter_cards(self):
        with self.client as c:
            card2 = Card(name='Second Name', text='Second Text', card_type='Instant',
                         colors='White', rarity='Uncommon', set_name='Tenth Edition')
            db.session.add(card2)

            resp = c.get(
                '/home/filter?card_type=&sets=Tenth+Edition&colors=White&rarities=Uncommon')

            self.assertIn('<div class="collapse" id="info-2">', str(resp.data))
            self.assertIn(
                '<h5 class="card-title">Second Name</h5>', str(resp.data))
            self.assertIn(
                '<p><b>name:</b> Second Name</p>', str(resp.data))
