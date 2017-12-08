import json
import copy
import hashlib

f = open('entity_jl/reddit.jl', 'r')
o = open('entity_jl/reddit4dig.jl', "w")

for line in f:
	data = json.loads(line)
	del data["fake_html"]
	if "opinion" in data:
		json.dump(data, o)
		o.write('\n')

f.close()
o.close()