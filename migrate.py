from app import app,db
from tables import Cards,Colors,Types,Subtypes, Clans
from loadjsoncards import data
from allsingletypes import types_flatten, subtypes_flatten
import re
# --------------------------------------------------------------

# THIS ROUTE IS ONLY FOR POPULATING DB WITH CARD FROM JSONFILE

# CARDS
 	
for card in data.values():
	card_name = card.get('name', '')
	card_mana_cost = re.sub("\W", "",card.get('manaCost', ''))
	if card_mana_cost != '':
		card_mana_cost = sorted(card_mana_cost)
		card_mana_cost = ''.join(card_mana_cost)
	card_text = card.get('text', '')
	dbcreate = Cards(card_name,card_mana_cost, 	  		             
 		             card_text)
  	db.session.add(dbcreate)
 	db.session.commit()
# --------------------------------------------------------------

# COLORS

colors = ["Red",
		  "Green",
		  "Blue",
		  "Black",
		  "White",
		  "empty"]

for color in colors:
	dbcreate = Colors(color)
	db.session.add(dbcreate)
	db.session.commit()

for card in data.values():
	colors = card.get('colors', [])
	name = card.get('name','')
	table_card = Cards.query.filter_by(name = name).first()
	for color in colors:
		color_table = Colors.query.filter_by(color = color).first()
		table_card.colors_ref.append(color_table)
	else:
		color_table = Colors.query.filter_by(color = "empty").first()
		table_card.colors_ref.append(color_table)
	db.session.commit()
# --------------------------------------------------------------

# CLANS

clans = ["Azorius",
		 "Dimir",
		 "Rakdos",
	 	 "Gruul",
	   	 "Selesnya",
		 "Orzhov",
		 "Izzet",
		 "Golgari",
		 "Boros",
		 "Simic"]

for clan in clans:
	dbcreate = Clans(clan)
	db.session.add(dbcreate)
	db.session.commit()
# --------------------------------------------------------------

# TYPES

for type in types_flatten:
	dbcreate = Types(type)
	db.session.add(dbcreate)
	db.session.commit()

for card in data.values():
	types = card.get('types', [])
	name = card.get('name', '')
	table_card = Cards.query.filter_by(name = name).first()
	for type in types:
		type_table = Types.query.filter_by(types = type).first()
		table_card.types_ref.append(type_table)
	else:
		type_table = Types.query.filter_by(types = "empty").first()
		table_card.types_ref.append(type_table)
	db.session.commit()
# --------------------------------------------------------------

# SUBTYPES

for subtype in subtypes_flatten:
	dbcreate = Subtypes(subtype)
	db.session.add(dbcreate)
	db.session.commit()


for card in data.values():
	subtypes = card.get('subtypes', [])
	name = card.get('name', '')
	table_card = Cards.query.filter_by(name = name).first()
	for subtype in subtypes:
		subtype_table = Subtypes.query.filter_by(subtype = subtype).first()
		table_card.subtypes_ref.append(subtype_table)
	else:
		subtype_table = Subtypes.query.filter_by(subtype = "empty").first()
		table_card.subtypes_ref.append(subtype_table)
	db.session.commit()



