from magic import db
from magic.models.tables import Cards, Users, Colors, Types, Subtypes
from flask import request, jsonify, Blueprint, json
import re
import requests

cards_blueprint = Blueprint('cards_routes', __name__)


# HEALTH-CHECK

@cards_blueprint.route('/health-check')
def health_check():
	return 'It lives!!!'

# --------------------------------------------------------------------
# TABLE CARDS ROUTES
# --------------------------------------------------------------


@cards_blueprint.route('/')
def welcome_page():
	return 'WELCOME TO MAGICAPI'

# SHOWING CARDS BY NAME

@cards_blueprint.route('/name/', methods = ['GET'])
def show_card_by_name():

	name = request.args.get('name','')
	body = json.dumps({ "query": { "match": { "name": name}} })
	url = 'http://127.0.0.1:9200/magic/card/_search'
	headers = { 'Content-Type': 'application/json'}
	r = requests.get(url, headers = headers, data = body)
	response =  json.loads(r.text).get('hits')
	hits = response['hits'][0]
	data = hits.get('_source')
	return jsonify(data)
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR

@cards_blueprint.route('/colors/')
def show_card_colors():

  	colors = request.args.get('colors', '')
  	colors = colors.split(',')
  	colors_keyword = ''
	for color in colors:
		if color == 'Blue':
			colors_keyword += 'U'
		else:
			colors_keyword += color[0]
	colors_keyword = sorted(colors_keyword)
	colors_keyword = ''.join(colors_keyword)
	body = {"from": 0,"size": 50,"query": {"nested": {"path": "colors","query": {"bool": {"must": [{ "match": { "colors.colors_keyword": colors_keyword }}]}}}}}
	url = 'http://127.0.0.1:9200/magic/card/_search'
	headers = { 'Content-Type': 'application/json'}
	r = requests.get(url, headers = headers, data = json.dumps(body))
	response =  json.loads(r.text).get('hits')
	total = response['total']
	hits = response['hits']
	cards = []
	for hit in hits:
		source = hit.get('_source', '')
		name = source.get('name', '')
		url = source.get('url', '')
		cards.append(dict(name = name, url = url))
	cards.append(dict(total = total))
	return jsonify(cards)
# --------------------------------------------------------------

# SHOW CARD USERS

@cards_blueprint.route('/users/')
def show_card_users():

	cardname = request.args.get('name','')
	users = Cards.query.filter_by( name = cardname).first()
	usernames = []
	for user in users.owner:
		usernames.append(user.username)
	return jsonify(dict(usernames = usernames))
# --------------------------------------------------------------

# SHOWING CARDS BY TEXT

@cards_blueprint.route('/text/')
def show_card_by_text():

	text = request.args.get('text','')
	print text
	body = { "from": 0,"size": 50, "query": { "match": { "text":{ "query": text, "operator":"and"}}}}
	url = 'http://127.0.0.1:9200/magic/card/_search'
	headers = { 'Content-Type': 'application/json'}
	r = requests.get(url, headers = headers, data = json.dumps(body))
	response =  json.loads(r.text).get('hits')
	total = response['total']
	hits = response['hits']
	cards = []
	for hit in hits:
		source = hit.get('_source', '')
		name = source.get('name', '')
		url = source.get('url', '')
		cards.append(dict(name = name, url = url))
	cards.append(dict(total = total))
	return jsonify(cards)

	
# --------------------------------------------------------------

# SHOWING CARDS BY SUBTYPES

@cards_blueprint.route('/subtypes/')
def show_card_by_subtypes():

	subtypes = request.args.get('subtypes','')
	body = { "from": 0,"size": 50, "query": { "match": { "subtypes":{ "query": subtypes, "operator":"and"}}}}
	url = 'http://127.0.0.1:9200/magic/card/_search'
	headers = { 'Content-Type': 'application/json'}
	r = requests.get(url, headers = headers, data = json.dumps(body))
	response =  json.loads(r.text).get('hits')
	total = response['total']
	hits = response['hits']
	cards = []
	for hit in hits:
		source = hit.get('_source', '')
		name = source.get('name', '')
		url = source.get('url', '')
		cards.append(dict(name = name, url = url))
	cards.append(dict(total = total))
	return jsonify(cards)
	
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR,TEXT

@cards_blueprint.route('/colors/text/')
def show_card_by_sub_color_text():

	args = request.args
	colors = request.args.get('colors','')
	colors_list = colors.split(',')
	if len(colors_list) > 1:
		colors_list = sorted(colors_list)
	text = request.args.get('text','')
	text_list = text.split(',')
	color_column = Colors.query.filter_by(color = colors_list[0]).first()
	card_filter_text = 0 
	cardnames = []
	cardurl = []
	subtype_filter = 0
	for card in color_column.colorcards:
		color_tostring = []
		for color in card.colors_ref:
			color_tostring.append(str(color))
		if sorted(color_tostring) == colors_list:
			split_text = re.split(r'\s+|[,;.-]\s*', card.text.lower())
			for word in text_list:
				if word in split_text:
					card_filter_text = 1
				else:
					card_filter_text = 0
					break
			if card_filter_text == 1:
				cardnames.append(card.name)
				cardurl.append(card.img_url)
	return jsonify(dict(names = cardnames, url = cardurl))


# --------------------------------------------------------------

# SHOWING CARDS BY MANACOST

@cards_blueprint.route('/manacost/')
def show_card_by_manacost():

	manacost = request.args.get('manacost','')
	manacost_sorted = sorted(manacost)
	manacost_sorted = ''.join(manacost_sorted)
	body = json.dumps({ "from": 0,"size": 50,"query": { "match": { "manaCost": manacost_sorted}} })
	url = 'http://127.0.0.1:9200/magic/card/_search'
	headers = { 'Content-Type': 'application/json'}
	r = requests.get(url, headers = headers, data = body)
	response =  json.loads(r.text).get('hits')
	total = response['total']
	hits = response['hits']
	cards = []
	for hit in hits:
		source = hit.get('_source', '')
		name = source.get('name', '')
		url = source.get('url', '')
		cards.append(dict(name = name, url = url))
	cards.append(dict(total = total))
	return jsonify(cards)
# --------------------------------------------------------------

# SHOWING CARDS BY TYPES

@cards_blueprint.route('/types/')
def show_card_by_types():

	types = request.args.get('types','')
	body = { "from": 0,"size": 50, "query": { "match": { "types":{ "query": types, "operator":"and"}}}}
	url = 'http://127.0.0.1:9200/magic/card/_search'
	headers = { 'Content-Type': 'application/json'}
	r = requests.get(url, headers = headers, data = json.dumps(body))
	response =  json.loads(r.text).get('hits')
	total = response['total']
	hits = response['hits']
	cards = []
	for hit in hits:
		source = hit.get('_source', '')
		name = source.get('name', '')
		url = source.get('url', '')
		cards.append(dict(name = name, url = url))
	cards.append(dict(total = total))
	return jsonify(cards)

# --------------------------------------------------------------


# SHOWING CARDS BY MANACOST AND COLOR

@cards_blueprint.route('/manacost/colors/')
def show_card_by_mana_color():

	manacost = request.args.get('manacost','')
	manacost_sorted = sorted(manacost)
	manacost_sorted = ''.join(manacost_sorted)
	colors = request.args.get('colors','')
	colors_list = colors.split(',')
	colors_keyword = ''
	for color in colors_list:
		if color == 'Blue':
			colors_keyword += 'U'
		else:
			colors_keyword += color[0]
	colors_keyword = sorted(colors_keyword)
	colors_keyword = ''.join(colors_keyword)
	body = {"from": 0,"size": 50,"query": {"bool": {"must": [{"match": {"manaCost": manacost_sorted}},{"nested": {"path": "colors","query": {"match": {"colors.colors_keyword":colors_keyword}}}}]}}}
	url = 'http://127.0.0.1:9200/magic/card/_search'
	headers = { 'Content-Type': 'application/json'}
	r = requests.get(url, headers = headers, data = json.dumps(body))
	response =  json.loads(r.text).get('hits')
	total = response['total']
	hits = response['hits']
	cards = []
	for hit in hits:
		source = hit.get('_source', '')
		name = source.get('name', '')
		url = source.get('url', '')
		cards.append(dict(name = name, url = url))
	cards.append(dict(total = total))
	return jsonify(cards)
# --------------------------------------------------------------