import json
import copy
from jellyfish import levenshtein_distance as ld
import re

team_stop = ["fc", "clube", "de", "do", "club"]
club_dict = json.load(open('dict/club_dict.json', 'r'))


player_f = open('entity_jl/player/player_no_id.jl', "r")
club_f = open('entity_jl/club/club_no_id.jl', "r")

o = open('entity_jl/club/club_entity.jl', "w")
oo = open('entity_jl/player/player_entity.jl', "w")

player_lst = []
for line in player_f:
	data = json.loads(line)
	this_player = {}
	this_player["name"] = data["name"]
	this_player["player_id"] = data["player_id"]
	this_player["club"] = data["current_club"]
	player_lst.append(this_player)

player_f.close()

club_lst = []
for line in club_f:
	data = json.loads(line)
	this_club = {}
	this_club["name"] = data["official_club_name"]
	this_club["club_id"] = data["club_id"]
	this_club["country"] = data["country"]
	club_lst.append(this_club)

club_f.close()

club_f = open('entity_jl/club/club_no_id.jl', "r")

ii = 0
player_f = open('entity_jl/player/player_no_id.jl', "r")
for line in player_f:
	ii += 1
	print ii
	data = json.loads(line)
	player_club = data["current_club"]
	player_club_country = data["league_country"]
	new_data = copy.deepcopy(data)
	for a_club in club_lst:
		if a_club["country"].lower() == player_club_country.lower() and player_club in club_dict and a_club["name"] in club_dict and club_dict[player_club] == club_dict[a_club["name"]]:
			new_data["current_club_id"] = a_club["club_id"]
			break
		else:
			if a_club["country"].lower() == player_club_country.lower() and ld(a_club["name"].lower(), player_club.lower())<=1:
				new_data["current_club_id"] = a_club["club_id"]
				break
	# if new_data["transfers"]:
	# 	for a_transfer in new_data["transfers"]:
	# 		a_transfer["move_from_club_id"] = ""
	# 		a_transfer["move_to_club_id"] = ""
	# 		for a_club in club_lst:
	# 			if a_transfer["move_from_club"] in club_dict and a_club["name"] in club_dict and club_dict[a_transfer["move_from_club"]] == club_dict[a_club["name"]]:
	# 				a_transfer["move_from_club_id"] = a_club["club_id"]
	# 			else:
	# 				if ld(a_club["name"].lower(), a_transfer["move_from_club"].lower())<=1:
	# 					a_transfer["move_from_club_id"] = a_club["club_id"]
	# 			if a_transfer["move_to_club"] in club_dict and a_club["name"] in club_dict and club_dict[a_transfer["move_to_club"]] == club_dict[a_club["name"]]:
	# 				a_transfer["move_to_club_id"] = a_club["club_id"]
	# 			else:
	# 				if ld(a_club["name"].lower(), a_transfer["move_to_club"].lower())<=1:
	# 					a_transfer["move_to_club_id"] = a_club["club_id"]
	del new_data["comparable_players"]
	new_data["comparable_players"] = []
	if data["comparable_players"]:
		for a_name in data["comparable_players"]:
			this_match = {}
			for a_player in player_lst:
				if ld(a_name.lower(), a_player["name"].lower()) <= 2:
					this_match["player_name"] = a_name
					this_match["player_id"] = a_player["player_id"]
					break
			if "player_name" in this_match:
				new_data["comparable_players"].append(this_match)
			else:
				new_data["comparable_players"].append({"player_name": a_name, "player_id": ""})
	json.dump(new_data, oo)
	oo.write('\n')
player_f.close()

ii = 0
for line in club_f:
	ii += 1
	print ii
	data = json.loads(line)
	club_name = data["official_club_name"]
	new_data = copy.deepcopy(data)
	del new_data["current_players"]
	new_data["current_players"] = []
	if data["current_players"]:
		for a_name in data["current_players"]:
			this_match = {}
			for a_player in player_lst:
				if a_player["club"] in club_dict and club_name in club_dict and club_dict[a_player["club"]] == club_dict[club_name] and ld(a_name.lower(), a_player["name"].lower()) <= 3:
					this_match["player_name"] = a_name
					this_match["player_id"] = a_player["player_id"]
					break
				else:
					if ld(a_player["club"].lower(), club_name.lower())<=1:
						this_match["player_name"] = a_name
						this_match["player_id"] = a_player["player_id"]
						break
			if "player_name" in this_match:
				new_data["current_players"].append(this_match)
			else:
				new_data["current_players"].append({"player_name": a_name, "player_id": ""})

	json.dump(new_data, o)
	o.write('\n')

club_f.close()
o.close()
oo.close()
