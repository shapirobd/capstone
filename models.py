from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask import jsonify

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


class Friendship(db.Model):
    __tablename__ = 'friendships'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user1_username = db.Column(db.Text, db.ForeignKey(
        'users.username', ondelete="cascade"))
    user2_username = db.Column(db.Text, db.ForeignKey(
        'users.username', ondelete="cascade"))


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(25), primary_key=True,
                         unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    image_url = db.Column(
        db.Text, default="/static/images/default_prof_pic.png")
    bookmarked_cards = db.relationship(
        'Card', secondary='bookmarks', backref='user')
    decks = db.relationship('Deck', backref='user')
    friends = db.relationship('User', secondary='friendships', primaryjoin=(
        Friendship.user1_username == username), secondaryjoin=(Friendship.user2_username == username))
    posts = db.relationship('Post', backref='user')

    @classmethod
    def signup(cls, username, password, email, image_url):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, password=hashed_pwd,
                    email=email, image_url=image_url)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False


class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text, nullable=False, index=True)
    image_url = db.Column(
        db.Text)
    text = db.Column(db.Text)
    card_type = db.Column(db.Text, nullable=False, index=True)
    power = db.Column(db.Text or db.String)
    toughness = db.Column(db.Text)
    colors = db.Column(db.Text, nullable=False, index=True)
    rarity = db.Column(db.Text, nullable=False, index=True)
    set_name = db.Column(db.Text, nullable=False, index=True)
    users = db.relationship('User', secondary='bookmarks', backref='cards')
    decks = db.relationship('Deck', secondary='cards_decks', backref='cards')

    @classmethod
    def create_all_cards(cls, cards):

        for card in cards:

            colors = ' '.join(card['colors'])

            image_url = card.get(
                'imageUrl', 'https://upload.wikimedia.org/wikipedia/en/a/aa/Magic_the_gathering-card_back.jpg')
            text = card.get('text')

            power = card.get('power')
            if isinstance(power, str) and (power.find('*') != -1 or power.find('X') != -1 or power.find('?') != -1 or power.find('x') != -1 or power.find('+') != -1 or power.find('-') != -1 or power.find('N')) != -1:
                power = 0

            toughness = card.get('toughness')
            if isinstance(toughness, str) and (toughness.find('*') != -1 or toughness.find('X') != -1 or toughness.find('?') != -1 or toughness.find('x') != -1 or toughness.find('+') != -1 or toughness.find('-') != -1 or toughness.find('N')) != -1:
                toughness = 0

            new_card = Card(name=card['name'], image_url=image_url, text=text, card_type=card['type'],
                            power=power, toughness=toughness, rarity=card['rarity'], set_name=card['setName'], colors=colors)
            db.session.add(new_card)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_url': self.image_url,
            'text': self.text,
            'card_type': self.card_type,
            'power': self.power,
            'toughness': self.toughness,
            'colors': self.colors,
            'rarity': self.rarity,
            'set_name': self.set_name,
        }


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.ForeignKey('users.username'))
    card_id = db.Column(db.ForeignKey('cards.id'))

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'card_id': self.card_id
        }


class Deck(db.Model):
    __tablename__ = 'decks'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    deck_name = db.Column(db.String(30), nullable=False)
    deck_type = db.Column(db.Text, nullable=False)
    username = db.Column(db.ForeignKey('users.username'))


class CardDeck(db.Model):
    __tablename__ = 'cards_decks'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id'))


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.ForeignKey('users.username'))
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
