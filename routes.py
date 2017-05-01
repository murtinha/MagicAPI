from app import app,db
from loadjsoncards import data
from tables import Cards, Users
from flask import request, json

# HEALTH-CHECK

@app.route('/health-check')
def health_check():
	return 'It lives!!!'


@app.route('/data')
def data_request():
	print data['Sen Triplets']
	return 'printed'

# --------------------------------------------------------------------
# TABLE CARDS ROUTES
# --------------------------------------------------------------

# ADDING CARDS TO CARDS-DB

@app.route('/add', methods = ['POST'])
def add_cards():
	card_name =''
	card_manaCost = ''
	card_colors = []
	card_types = []
	card_text = ''
	card_artist = ''
	for card in data.values():
		if 'name' in card:
			card_name = card['name']
		if 'manaCost' in card:
			card_manaCost = card['manaCost']
		if 'colors' in card:
			card_colors = card['colors']
		if 'types' in card:
			card_types = card['types']
		if 'text' in card:
			card_text = card['text']
		if 'artist' in card:
			card_artist = card['artist']
  		dbcreate = Cards(card_name,card_manaCost,
	  		             str(card_colors),str(card_types),
	  		             card_text,card_artist)
	  	db.session.add(dbcreate)
	 	db.session.commit()
	return 'added'
# --------------------------------------------------------------

# SHOWING CARDS BY NAME

@app.route('/name')
def show_card_by_name():

	user_input = request.get_json()
	name = user_input['name']
	card = Cards.query.filter_by(name = name).first()
	return str(card)
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR

# @app.route('/colors')
# def show_card_colors():

#  	user_input = request.get_json()
#  	print user_input['colors'][0]
#  	return 'ok'
#   card = Cards.query.filter_by(colors = colors).all()
#   cardnames = []
#   for number in range(len(card)):
# 	cardnames.append(card[number].name)
#   return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOW CARD USERS

@app.route('/users')
def show_card_users():

	user_input = request.get_json()
	card = user_input['name']
	users = Cards.query.filter_by( name = card).first()
	usernames = []
	for user in users.owner:
		usernames.append(user.username)
	return json.dumps(dict(usernames = usernames))
# --------------------------------------------------------------

# SHOWING CARDS BY ARTIST

@app.route('/artist')
def show_card_by_artist():

	user_input = request.get_json()
	artist = user_input['artist']
	card = Cards.query.filter_by(artist = artist).all()
	cardnames = []
	for number in range(len(card)):
		cardnames.append(card[number].name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY MANACOST

@app.route('/manacost')
def show_card_by_manacost():

	user_input = request.get_json()
	manacost = user_input['manaCost']
	formated_mana_cost = ''
	cardnames = []
	for letter in manacost:
		formated_mana_cost += '{%s}' % letter # To get input in {letter}{letter} format
	card = Cards.query.filter_by(manaCost = formated_mana_cost).all()
	for number in range(len(card)):
		cardnames.append(card[number].name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY RARITY

@app.route('/rarity')
def show_card_by_rarity():
	
	user_input = request.get_json()
	rarity = user_input['rarity']
	card = Cards.query.filter_by(rarity = rarity).all()
	cardnames = []
	for number in range(len(card)):
		cardnames.append(card[number].name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# DELETING CARDS

# @app.route('/delete/<name>', methods = ['DELETE'])
# def delete_card_by_name(name):

# 	card = Cards.query.filter_by(name = name).first()
# 	db.session.delete(card)
# 	db.session.commit()
# 	return '%s deleted' % name

# --------------------------------------------------------------
# TABLE USERS ROUTES
# --------------------------------------------------------------

# ADDING USER

@app.route('/adduser', methods = ['POST'])
def add_user():

	user_input = request.get_json()
	user_username = user_input['username']
	user_email = user_input['email']
	dbcreate = Users(user_username, user_email)

	db.session.add(dbcreate)
	db.session.commit()

	return 'User %s added' % user_username
# --------------------------------------------------------------

# ADDING CARDS TO A SPECIFIC USER

@app.route('/add/<username>', methods = ['POST'])
def add_card_to_user(username):

	user_input = request.get_json()
	card_name = user_input['name']
	user = Users.query.filter_by(username = username).first()
	for number in range(len(card_name)):
		card = Cards.query.filter_by(name = card_name[number]).first()
		card.owner.append(user)
		db.session.commit()
	return json.dumps(dict(names = card_name)) + 'added to %s' % user.username
# --------------------------------------------------------------

# SHOWING USER CARDS

@app.route('/cards/<username>')
def show_user_cards(username):
	cardsnames = []
	user = Users.query.filter_by(username = username).first()
	for card in user.mycards:
		cardsnames.append(card.name)
	return json.dumps(dict(name = cardsnames))
# --------------------------------------------------------------

# SHOWING CARDS BY ARTIST

@app.route('/artist/<username>')
def show_user_card_by_artist(username):

	user_input = request.get_json()
	artist = user_input['artist']
	user = Users.query.filter_by(username = username).first()
	cardnames = []
	for card in user.mycards:
		if card.artist == artist:
			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY MANACOST

@app.route('/manacost/<username>')
def show_user_card_by_manacost(username):

	user_input = request.get_json()
	manacost = user_input['manaCost']
	formated_mana_cost = ''
	cardnames = []
	for each in manacost:
		formated_mana_cost += '{%s}' % each # To get input in {letter}{letter} format
	user = Users.query.filter_by(username = username).first()
	for card in user.mycards:
		if card.manaCost == formated_mana_cost:
			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY RARITY

@app.route('/rarity/<username>')
def show_card_user_by_rarity(username):
	
	user_input = request.get_json()
	rarity = user_input['rarity']
	user = Users.query.filter_by(username = username).first()
	cardnames = []
	for card in user.mycards:
		if card.rarity == rarity:
			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------