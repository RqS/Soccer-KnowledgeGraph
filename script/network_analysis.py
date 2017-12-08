import json
import numpy as np
from scipy import sparse
from jellyfish import levenshtein_distance as ld

stop_lst = [u'and', u'St.', u'The', u'New', u'N/A']

player_f = open('entity_jl/player/player_entity.jl', "r")


player_lst = []
for line in player_f:
    data = json.loads(line)
    nation = []
    for a in data["nationality"]:
        if a == u'Gambia':
            nation.append(u'The Gambia')
        elif a == u'Zealand':
            nation.append(u'New Zealand')
        elif a not in stop_lst:
            nation.append(a)
    player_lst.append({"nationality":nation, "age": data["age"]})

player_f.close()

mygraph = np.zeros(len(player_lst), len(player_lst))
for a_idx, a_player in enumerate(player_lst):
    for b_idx in range(len(player_lst))[a_idx+1:]:
        b_player = player_lst[b_idx]
        if set(a_player["nationality"]).intersection(b_player["nationality"]) and a_player["age"].isdigit() and b_player["age"].isdigit() and abs(int(a_player["age"]) - int(b_player["age"])) <=5:
            mygraph[a_idx,b_idx] = 1
            mygraph[b_idx,a_idx] = 1
        else:
            mygraph[a_idx,b_idx] = 0
            mygraph[b_idx,a_idx] = 0

for i in range(len(player_lst)):
    mygraph[i,i] = 0


result = sparse.csgraph.connected_components(mygraph)
