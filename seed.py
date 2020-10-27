import requests

from app import db
from models import connect_db, Card

db.drop_all()
db.create_all()

# for page in range(1, 546):
resp = requests.get('http://api.magicthegathering.io/v1/cards', {
    'key': "$2a$10$TNyqKQQQSzVjgGXY87waZuBIKAS78.NkY2o.H004TfBU.eISv.Pt6"
}).json()
cards = resp['cards']
# print(f'Page: {page}, Count: {len(cards)}')
Card.create_all_cards(cards)

for page in range(1, 10):
    resp = requests.get('http://api.magicthegathering.io/v1/cards', {
        'key': "$2a$10$TNyqKQQQSzVjgGXY87waZuBIKAS78.NkY2o.H004TfBU.eISv.Pt6",
        'page': page
    }).json()
    cards = resp['cards']
    print('*****')
    print(cards)
    Card.create_all_cards(cards)
db.session.commit()
