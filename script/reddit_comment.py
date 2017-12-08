import json

f = open('page_jl/reddit_dig.jl')

comments = {}

for line in f:
	data = json.loads(line)
	topic = data['topic']
	if data['topic'] not in comments:
		comments[topic] = []
	topic_comments = data['comments'].split('\n\n')
	for a_comment in topic_comments:
		comment_lst = a_comment.replace('children', 'child').split('child)')
		for aa_comment in comment_lst:
			if aa_comment not in comments[topic] and 'permalink' not in aa_comment and '[' not in aa_comment:
				comments[topic].append(aa_comment)

f.close()
