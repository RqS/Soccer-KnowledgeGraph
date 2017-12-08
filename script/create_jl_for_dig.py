import json
import copy
import hashlib


f = open('entity_jl/player/player.jl')
o = open('entity_jl/player/player_no_id.jl', "w")

def get_value(s):
	s = s.lower().replace(",","").replace(" ", "").replace("mill", "0000").replace("th", "000").replace(".", "").replace("eur", "")
	return s

features = ["player_agent", "height", "current_club", "honors_in_national_team", "comparable_players", "title", "description",
"current_market_value", "weight", "bmi", "league_country", "main_positions", "outfitter", "fifa_statistics",
"current_statistics", "contract_until", "foot", "nationality", "honors_in_club","name", "player_id",
"highest_market_value", "url", "age", "other_positions", "social_media", "place_of_birth", "transfers", "doc_id", "raw_content"]

transfer_nest = ["move_to_club","market_value","move_from_club","move_from_country","transfer_fee","move_to_country","transfer_season"]


for line in f:
	data = json.loads(line)
	if "name" in data and "current club" in data and data["name"] and data["current club"]:
		url = "http://player.player_entity.com/" + data["name"].encode('utf-8').replace(" ", "_") + "/" + data["current club"].encode('utf-8').replace(" ", "_")
		doc_id = hashlib.sha256(url).hexdigest()
		new_data = {}
		new_data["url"] = url
		new_data["doc_id"] = doc_id
		new_data["player_id"] = data["name"].encode('utf-8').replace(" ", "_") + doc_id[:5]
		new_data["raw_content"] = "."
		for key in data:
			if data[key]:
				new_data[key.lower().replace(' ', '_').replace("'s", "")] = copy.deepcopy(data[key])
		temp = new_data["name"]
		new_data["name"] = temp.title()
		new_data["title"] = new_data["name"]+" profile"
		new_data["description"] = "Information of player: " + new_data["name"]
		if "position" in new_data:
			new_data["main_positions"] = new_data["position"] 
			del new_data["position"]
		if "detailed_positions" in new_data:
			new_data["other_positions"] = new_data["detailed_positions"]["other positions"]
			del new_data["detailed_positions"]
		if "club_honors" in new_data:
			new_data["honors_in_club"] = []
			for an_honor in new_data["club_honors"]:
				this_honor = an_honor + ": " + str(new_data["club_honors"][an_honor])
				new_data["honors_in_club"].append(this_honor)
			del new_data["club_honors"]
		if "international_honors" in new_data:
			new_data["honors_in_national_team"] = []
			for an_honor in new_data["international_honors"]:
				this_honor = an_honor + ": " + str(new_data["international_honors"][an_honor])
				new_data["honors_in_national_team"].append(this_honor)
			del new_data["international_honors"]
		new_data["transfers"] = []
		if "transfer_history" in new_data:
			for idx, a_transfer in enumerate(new_data["transfer_history"]):
				this_transfer = {}
				this_transfer["move_from_club"] = a_transfer["moving from"]["club"]
				this_transfer["move_from_country"] = a_transfer["moving from"]["country"]
				this_transfer["move_to_club"] = a_transfer["moving to"]["club"]
				this_transfer["move_to_country"] = a_transfer["moving to"]["country"]
				this_transfer["transfer_fee"] = get_value(a_transfer["transfer fee"])
				this_transfer["market_value"] = get_value(a_transfer["market value"])
				this_transfer["transfer_season"] = a_transfer["season"]
				this_transfer["title"] = "transfer of " + new_data["name"] + " in " + this_transfer["transfer_season"]
				this_transfer["description"] = new_data["name"] + " transfered from "+ this_transfer["move_from_club"] + " to " + this_transfer["move_to_club"] + " in season " + this_transfer["transfer_season"] + " with a fee of " + this_transfer["transfer_fee"]
				new_data["transfers"].append(copy.deepcopy(this_transfer))
			del new_data["transfer_history"]
		if "current_market_value" in new_data:
			current_market_value = get_value(new_data["current_market_value"]["value"])
			del new_data["current_market_value"]
			new_data["current_market_value"] = current_market_value
		if "social_media" in new_data:
			social_media = new_data["social_media"].values()
			del new_data["social_media"]
			new_data["social_media"] = social_media
		if "highest_market_value" in new_data:
			highest_market_value = get_value(new_data["highest_market_value"]["value"])
			del new_data["highest_market_value"]
			new_data["highest_market_value"] = highest_market_value
		if "nationality" in new_data:
			if type(new_data["nationality"]) != list:
				nationality = [new_data["nationality"]]
				del new_data["nationality"]
				new_data["nationality"] = nationality
		if "league_level" in new_data:
			new_data["league_country"] = new_data["league_level"]["country"]
			new_data["league_level"] = new_data["league_level"]["level"]
			del new_data["league_level"]
		if "statistics" in new_data:
			new_data["current_statistics"] = []
			for key in new_data["statistics"]:
				if type(new_data["statistics"][key]) != dict:
					this_stat = key.replace(" ", "_").replace(".", "") + ": " + new_data["statistics"][key]
					new_data["current_statistics"].append(this_stat)
				else:
					for sub_key in new_data["statistics"][key]:
						this_stat = sub_key.replace(" ", "_").replace(".", "") + ": " + new_data["statistics"][key][sub_key]
						new_data["current_statistics"].append(this_stat)
			del new_data["statistics"]
		new_data["fifa_statistics"] = []
		if "fifa_stat" in new_data:
			for key in new_data["fifa_stat"]:
				new_data["fifa_statistics"].append(key + ": " + str(new_data["fifa_stat"][key]))
		for a_feature in features:
			if a_feature not in new_data:
				new_data[a_feature] = ""
		del_lst = []
		for a_feature in new_data:
			if a_feature not in features:
				del_lst.append(a_feature)
		for a_feature in del_lst:
			del new_data[a_feature]
		json.dump(new_data, o)
		o.write('\n')

f.close()
o.close()



