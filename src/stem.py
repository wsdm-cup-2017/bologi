from nltk.stem import SnowballStemmer
from collections import defaultdict
import json

def load_json(path):
    return json.load(open(path))

if __name__=='__main__':
	stemmer = SnowballStemmer("english")

	type_names =  ['profession']
	for type_name in type_names:
		obj = load_json("../data/intermediate_data/old_" + type_name +"_words_table.txt")
	  # save old version to pretty print format
		# with open("../data/intermediate_data/" + type_name +"_words_table.txt",'w') as f:
		# 	json.dump(obj, f, sort_keys=True, indent=4, separators=(',', ': '))

		new_obj = defaultdict(set)
		for center, words in obj.iteritems():
			# center = stemmer.stem(center)

			for i in range(len(words)):
				for token in words[i].split():
					 stem_token = stemmer.stem(token)
					 new_obj[center].add(stem_token)
				         new_obj[center].add(token)
			#	new_obj[center].add(words[i])
			for noise in ["of", "and"]:
				if noise in new_obj[center]:
					new_obj[center].remove(noise)

			new_obj[center] = list(new_obj[center])

		with open("../data/intermediate_data/" + type_name +"_words_table.txt",'w') as f:
			json.dump(new_obj, f, sort_keys=True, indent=4, separators=(',', ': '))
