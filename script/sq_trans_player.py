import json
import re
import copy
import codecs
from pyjarowinkler import distance

club_dict = json.load(open('dict/club_dict.json', 'r'))

def compare_team(s1, s2):
	# s1 = s1.lower()
	# s2 = s2.lower()
	ss1 = [x for x in re.sub(r'[^\w\s]','',s1.lower().replace("-", " ")).split() if x not in team_stop and len(x) > 2]
	ss2 = [x for x in re.sub(r'[^\w\s]','',s2.lower().replace("-", " ")).split() if x not in team_stop and len(x) > 2]
	# if ss1 and ss2:
	# 	jaccard = len(set(ss1).intersection(ss2)) / float(len(set(ss1).union(ss2)))
	# 	if jaccard > 0.85:
	# 		result = jaccard * (1 - (1-0.85) / jaccard)
	# 	else:
	# 		jaro = distance.get_jaro_distance(s1, s2)
	# 		inverse_jaro = distance.get_jaro_distance(s1[::-1], s2[::-1])
	# 		if len(ss1) != len(ss2):
	# 			this_jaro = max(jaro, inverse_jaro)
	# 		else:
	# 			word_jaro_lst = [jaro, inverse_jaro]
	# 			if len(ss1) == 1:
	# 				this_jaro = sum(word_jaro_lst) / 2
	# 			else:
	# 				for idx in range(len(ss1)):
	# 					word_jaro_lst.append(distance.get_jaro_distance(ss1[idx], ss2[idx]))
	# 					word_jaro_lst.append(distance.get_jaro_distance(ss1[idx][::-1], ss2[idx][::-1]))
	# 				avg_jaro = sum(word_jaro_lst) / len(word_jaro_lst)
	# 				if avg_jaro > 0.7:
	# 					this_jaro = max(jaccard, avg_jaro)
	# 				else:
	# 					this_jaro = min(jaccard, avg_jaro)
	# 		result = max(jaccard, this_jaro)
	# else:
	# 	result = 0
	# return result
	if ss1 and ss2:
		return len(set(ss1).intersection(ss2)) / float(min(len(set(ss1)), len(set(ss2))))
	else:
		return 0

def compare_age(a1, a2):
	if abs(a2 - a1) <= 1:
		return 1
	else:
		if abs(a1 - a2) >= 4:
			return (-1)
		else:
			return 0

def compare_name(s1, s2):
	s1 = s1.lower()
	s2 = s2.lower()
	ss1 = [x for x in re.sub(r'[^\w\s]','',s1.lower().replace("-", " ")).split() if len(x) > 2]
	ss2 = [x for x in re.sub(r'[^\w\s]','',s2.lower().replace("-", " ")).split() if len(x) > 2]
	if ss1 and ss2:
		jaccard = len(set(ss1).intersection(ss2)) / float(len(set(ss1).union(ss2)))
		if jaccard > 0.9:
			result = jaccard * (1 - (1-0.9) / jaccard)
		else:
			jaro = distance.get_jaro_distance(s1, s2)
			inverse_jaro = distance.get_jaro_distance(s1[::-1], s2[::-1])
			if len(ss1) != len(ss2):
				this_jaro = max(jaro, inverse_jaro)
			else:
				word_jaro_lst = [jaro, inverse_jaro]
				if len(ss1) == 1:
					this_jaro = sum(word_jaro_lst) / 2
				else:
					for idx in range(len(ss1)):
						word_jaro_lst.append(distance.get_jaro_distance(ss1[idx], ss2[idx]))
						word_jaro_lst.append(distance.get_jaro_distance(ss1[idx][::-1], ss2[idx][::-1]))
					avg_jaro = sum(word_jaro_lst) / len(word_jaro_lst)
					if avg_jaro > 0.7:
						this_jaro = max(jaccard, avg_jaro)
					else:
						this_jaro = min(jaccard, avg_jaro)
			result = max(jaccard, this_jaro)
		return result
	else:
		return 0

def compare_height(s1, s2):
	if abs(s1 - s2) <= 0.02:
		return 1
	else:
		if abs(s1 - s2) >= 0.1:
			return (-1)
		else:
			return 0

def compare_position(s1, s2):
	if s1 == s2:
		return 1
	else:
		if (s1 == "Midfielder" and s2 == "Forward") or (s2 == "Midfielder" and s1 == "Forward"):
			return 0.05
		elif s1 == "Goalkeeper" or s2 == "Goalkeeper":
			return (-0.2)
		else:
			return 0

def compare_clubs(s1, l2):
	this_score_l = []
	for s2 in l2:
		this_score_l.append(compare_team(s1, s2))
	return max(this_score_l)

def get_score(p1, p2):
	score = 0
	if p1['team'] and p2['team']:
		if compare_team(p1['team'], p2['team']) > 0:
			score += 0.5 * compare_team(p1['team'], p2['team'])
		elif "pre_clubs" in p2 and p2["pre_clubs"]:
			score += 0.45 * compare_clubs(p1['team'], p2['pre_clubs'])
	if p1['age'] and p2['age']:
		score += 0.25 * compare_age(p1['age'], p2['age'])
	if p1['name']:
		if p2['name'] and compare_name(p1['name'], p2['name']) > 0.3:
			name_score = 1 * compare_name(p1['name'], p2['name'])
			score += name_score
		elif p2['complete_name']:
			name_score = 0.5 * compare_name(p1['name'], p2['complete_name'])
			score += name_score
	if p1['height'] and p2['height']:
		score += 0.25 * compare_height(p1['height'], p2['height'])
	if p1['position'] and p2['position']:
		score += 0.2 * compare_position(p1['position'], p2['position'])
	return score

f1 = open('kg_jl/squawka.json', 'r')
f2 = open('kg_jl/transfermarket_player_extracted.jl', 'r')

team_stop = ["fc", "clube", "de", "do", "club"]

position_map = {
	"Midfield": "Midfielder",
	"Goalkeeper": "Goalkeeper",
	"Defence": "Defender",
	"Striker": "Forward"
}

def is_float(string):
  try:
    return float(string) and '.' in string
  except ValueError:
    return False


player_lst1 = json.load(f1)
player_dict1 = {}
for idx, player1 in enumerate(player_lst1):
	player_dict1[idx] = player1
	player1_d = {}
	player1_d['name'] = player1["Name"] if "Name" in player1 else None
	if "Team" in player1:
		player1_d['team'] = player1['Team']
		if player1['Team'] in club_dict:
			player1_d['team'] = club_dict[player1['Team']]
		else:
			for key in club_dict:
				if player1['Team'].lower() in key.lower():
					player1_d['team'] = club_dict[key]
					break
	else:
		player1_d['team'] = None
	player1_d['position'] = player1["Position"] if "Position" in player1 else None
	player1_d['age'] = int(player1["Age"]) if "Age" in player1 and player1["Age"].isdigit() else None
	player1_d['height'] = float(player1["Height"].lower().replace('m', '').strip()) if "Height" in player1 and is_float(player1["Height"].lower().replace('m', '').strip()) else None
	player_dict1[idx]['inf'] = player1_d


player_dict2 = {}
for idx, line in enumerate(f2):
	player2 = json.loads(line)
	player_dict2[idx] = player2
	player2_d = {}
	player2_d['age'] = int(player2["age"]) if "age" in player2 and player2["age"].isdigit() else None
	player2_d['team'] = player2["current club"] if "current club" in player2 else None
	player2_d['height'] = float(player2['height'].lower().replace(',', '.').replace('m', '').replace(' ','').strip()) if 'height' in player2 and is_float(player2['height'].lower().replace(',', '.').replace('m', '').replace(' ','').strip()) else None
	player2_d['position'] = position_map[player2["position"].split('-')[0].strip()]
	player2_d['name'] = player2["name"] if "name" in player2 else None
	player2_d['complete_name'] = player2["complete name"] if "complete name" in player2 else None
	if "transfer history" in player2:
		player2_d['pre_clubs'] = [x["moving from"]["club"] for x in player2["transfer history"] if len(x["moving from"]["club"]) >= 4 and "free" not in x["moving from"]["club"].lower() and "season" in x and x["season"][:2].isdigit() and int(x["season"][:2])>=16]
	player_dict2[idx]['inf'] = player2_d

f1.close()
f2.close()

player2_result = {}
ii=0
o = open('oo.txt', "w")
for player1_id in player_dict1:
	print ii
	ii += 1
	player1_d = player_dict1[player1_id]['inf']
	sim_lst = []
	for player2_id in player_dict2:
		player2_d = player_dict2[player2_id]['inf']
		this_score = get_score(player1_d, player2_d)
		sim_lst.append((this_score, player2_id))

	max_sim = max(sim_lst, key=lambda item:item[0])
	max_idx = max_sim[1]
	o.write(str(max_sim))
	o.write('\n')
	o.write(str(player1_d))
	o.write('\n')
	o.write(str(player_dict2[max_idx]['inf']))
	o.write('\n\n')
	if max_sim[0] > 1.794:
		max_idx = max_sim[1]
		if max_idx not in player2_result:
			player2_result[max_idx] = []
		player2_result[max_idx].append((max_sim, player1_id))
o.close()

oo = open('sq_trans/oo.txt', 'w')
output_dict = copy.deepcopy(player_dict2)
for player2_id in player2_result:
	most_sim = sorted(player2_result[player2_id])[-1]
	most_sim_id = most_sim[1]
	if most_sim_id in player_dict1:
		output_dict[player2_id]['statistics'] = player_dict1[most_sim_id]['Statistics'] if 'Statistics' in player_dict1[most_sim_id] else None
		output_dict[player2_id]['weight'] = player_dict1[most_sim_id]['Weight'] if 'Weight' in player_dict1[most_sim_id] else None
		output_dict[player2_id]['BMI'] = player_dict1[most_sim_id]['BMI'] if 'BMI' in player_dict1[most_sim_id] else None
		oo.write(str(player_dict1[most_sim_id]['inf']))
		oo.write('\n')
		oo.write(str(player_dict2[player2_id]['inf']))
		oo.write('\n\n')
		del player_dict1[most_sim_id]

oo.close()

length = len(output_dict)
for rest_id in player_dict1:
	output_dict[rest_id + length + 1] = {}
	output_dict[rest_id + length + 1]['statistics'] = player_dict1[rest_id]['Statistics'] if 'Statistics' in player_dict1[rest_id] else None
	output_dict[rest_id + length + 1]['weight'] = player_dict1[rest_id]['Weight'] if 'Weight' in player_dict1[rest_id] else None
	output_dict[rest_id + length + 1]['BMI'] = player_dict1[rest_id]['BMI'] if 'BMI' in player_dict1[rest_id] else None
	output_dict[rest_id + length + 1]['name'] = player_dict1[rest_id]['Name'] if 'Name' in player_dict1[rest_id] else None
	output_dict[rest_id + length + 1]['age'] = player_dict1[rest_id]['Age'] if 'Age' in player_dict1[rest_id] else None
	output_dict[rest_id + length + 1]['current club'] = player_dict1[rest_id]['Team'] if 'Team' in player_dict1[rest_id] else None
	output_dict[rest_id + length + 1]['position'] = player_dict1[rest_id]['Position'] if 'Position' in player_dict1[rest_id] else None
	output_dict[rest_id + length + 1]['height'] = player_dict1[rest_id]['Height'] if 'Height' in player_dict1[rest_id] else None
		
output_f = codecs.open('entity_jl/player_medium.jl', 'w')
for output_id in output_dict:
	if 'inf' in output_dict[output_id]:
		del output_dict[output_id]['inf']
	json.dump(output_dict[output_id], output_f)
	output_f.write("\n")

output_f.close()
