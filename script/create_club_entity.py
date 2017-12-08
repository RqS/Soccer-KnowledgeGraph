import json
import copy
import hashlib

f = open('entity_jl/club/club.jl', 'r')
o = open('entity_jl/club/club_no_id.jl', "w")

features = ["title", "tel", "total_market_value", "club_id", "reddit_neutral_count", "reddit_positive_count", "official_club_name",
	"reddit_negative_count", "location", "league_level", "current_rank", "average_age", "foundation", "fax", "foreign_players_count",
	"foreign_players_percentage", "squad_size", "club_honors", "url", "country", "raw_content", "league_name", "overall_stat", "current_players", "doc_id"]

def get_value(s):
	s = s.lower().replace(",","").replace(" ", "").replace("mill", "0000").replace("th", "000").replace(".", "").replace("eur", "")
	return s

for line in f:
	data = json.loads(line)
	if "Official club name" in data and data["Official club name"]:
		url = "http://club.club_entity.com/" + data["Official club name"].encode('utf-8').replace(" ", "_")
		doc_id = hashlib.sha256(url).hexdigest()
		new_data = {}
		new_data["url"] = url
		new_data["doc_id"] = doc_id
		new_data["club_id"] = data["Official club name"].encode('utf-8').replace(" ", "_") + doc_id[:5]
		new_data["raw_content"] = "."
		for key in data:
			if data[key]:
				new_data[key.lower().replace(' ', '_').replace("'s", "")] = copy.deepcopy(data[key])
		new_data["title"] = new_data["official_club_name"]+" profile"
		new_data["description"] = "Information of club: " + new_data["official_club_name"]
		if "foreign_players" in new_data:
			new_data["foreign_players_count"] = new_data["foreign_players"]["count"] if "count" in new_data["foreign_players"] else ""
			new_data["foreign_players_percentage"] = new_data["foreign_players"]["percentage"] if "percentage" in new_data["foreign_players"] else ""
			del new_data["foreign_players"]
		if "forum_opinion" in new_data:
			new_data["reddit_positive_count"] = str(new_data["forum_opinion"]["positive"]) if "positive" in new_data["forum_opinion"] and new_data["forum_opinion"]["positive"] else ""
			new_data["reddit_negative_count"] = str(new_data["forum_opinion"]["negative"]) if "negative" in new_data["forum_opinion"] and new_data["forum_opinion"]["negative"] else ""
			new_data["reddit_neutral_count"] = str(new_data["forum_opinion"]["plain"]) if "plain" in new_data["forum_opinion"] and new_data["forum_opinion"]["plain"] else ""
			del new_data["forum_opinion"]
		if "players" in new_data:
			new_data["current_players"] = []
			for a_player in new_data["players"]:
				new_data["current_players"].append(a_player["name"])
			del new_data["players"]
		else:
			new_data["current_players"] = ""
		if "total_market_value" in new_data:
			total_market_value = get_value(new_data["total_market_value"])
			new_data["total_market_value"] = total_market_value
		if "season_performance" in new_data:
			new_data["current_rank"] = new_data["season_performance"]["League Rank"] if "League Rank" in new_data["season_performance"] else ""
			if "Overall matches stats" in new_data["season_performance"]:
				new_data["overall_stat"] = []
				for a_stat in new_data["season_performance"]["Overall matches stats"]:
					new_data["overall_stat"].append(a_stat + ": " + new_data["season_performance"]["Overall matches stats"][a_stat])
			del new_data["season_performance"]
		if "honors" in new_data:
			new_data["club_honors"] = []
			for a_honor in new_data["honors"]:
				if a_honor and new_data["honors"][a_honor]:
					new_data["club_honors"].append(a_honor + ": " + str(new_data["honors"][a_honor]))
			del new_data["honors"]
		if "club_address" in new_data:
			new_data["location"] = new_data["club_address"]
			del new_data['club_address']
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