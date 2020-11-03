# capstone

Link to proposal:

https://docs.google.com/document/d/1vihomjFiPxAEcT1a_XN5z64aQJ3TPLc6ZatwUhQOaoU/edit?usp=sharing


Title of my site: MTG Deck Builder
Link to the URL where it is deployed: 

MTG Deck Builder allows users to search for cards in the MTG library, see info on the cards, create their own decks, create posts, add friends, and view decks that other users have made.

Features implemented:
- The search bar at the top allows users to search for cards by card name, decks by deck name or type, and users/friends by username. This is what I believe would be the most common search criteria.
- There is AJAX involved in bookmarking a card, adding/removing a friend and adding a card to a deck - this way, a user does have to leave the page or refresh and can keep their momentum going through the site.
- You are able to see the owner of any given deck and click their username to immediately view their profile - this allows users to easily add a friend who has a deck they like, or simply view other decks from that user by visiting their profile.
- When you click "Add to Deck" under a card, at the end of the list of your decks that pops up under the card there is a button that says "Create Deck" - this allows you to add the selected card to a brand new deck. Upon making the new deck, the selected card will automatically be added to that deck.

Standard user flow:
1. Login/Register
2. View home page where all cards (paginated) are shown
3. Create new deck
4. Search for cards by name
5. Add cards to decks
6. You may also search for other decks for inspiration

Notes on MTG API:
- Requests for cards can take a very long time - if you want to retrieve every single card from the API, it can take around 2 hours. Also, the Python SDK suddenly stopped working one day, so there seems to be some issues that need fixing.

Technology stack used:
- astroid==2.4.2
- autopep8==1.5.4
- bcrypt==3.2.0
- blinker==1.4
- certifi==2020.6.20
- cffi==1.14.3
- chardet==3.0.4
- click==7.1.2
- dnspython==2.0.0
- email-validator==1.1.1
- Flask==1.1.2
- Flask-Bcrypt==0.7.1
- Flask-DebugToolbar==0.11.0
- flask-paginate==0.7.1
- Flask-SQLAlchemy==2.4.4
- Flask-WTF==0.14.3
- idna==2.10
- isort==5.6.4
- itsdangerous==1.1.0
- Jinja2==2.11.2
- lazy-object-proxy==1.4.3
- MarkupSafe==1.1.1
- mccabe==0.6.1
- mtgsdk==1.3.1
- psycopg2-binary==2.8.6
- pycodestyle==2.6.0
- pycparser==2.20
- pylint==2.6.0
- requests==2.24.0
- six==1.15.0
- SQLAlchemy==1.3.20
- toml==0.10.1
- typed-ast==1.4.1
- urllib3==1.25.11
- Werkzeug==1.0.1
- wrapt==1.12.1
- WTForms==2.3.3

There are still a lot of features that I want to add, but I need to move on with the curriculum so I am submitting my project with the features it currently has and will add more features as stretch goals.
