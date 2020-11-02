import requests

from app import db
from models import connect_db, Card
print('STARTING SEED...')
db.drop_all()
db.create_all()

for page in range(1, 546):
    print(f"Page: {page}...")
    resp = requests.get('http://api.magicthegathering.io/v1/cards', {
        'key': "$2a$10$TNyqKQQQSzVjgGXY87waZuBIKAS78.NkY2o.H004TfBU.eISv.Pt6",
        'page': page
    }).json()
    cards = resp['cards']
    Card.create_all_cards(cards)
    print('** DONE **')
db.session.commit()
