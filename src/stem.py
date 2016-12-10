from nltk.stem import SnowballStemmer
import json

def load_json(path):
    return json.load(open(path))

if __name__=='__main__':
	stemmer = SnowballStemmer("english")

	type_names = ['nationality', 'profession']
	for type_name in type_names:
		obj = load_json("../data/intermediate_data/old_" + type_name +"_words_table.txt")
	  # save old version to pretty print format
		# with open("../data/intermediate_data/" + type_name +"_words_table.txt",'w') as f:
		# 	json.dump(obj, f, sort_keys=True, indent=4, separators=(',', ': '))

		# words = obj['accountant']
		# print words,"\nBEFORE!!", len(words)
		# for i in range(len(words)):
		# 	words[i] = stemmer.stem(words[i])
		# obj['accountant'] = list(set(words))
		# print obj['accountant'],"\nAFTER!!", len(obj['accountant'])

		new_obj = {}
		for center, words in obj.iteritems():
			# center = stemmer.stem(center)
			for i in range(len(words)):
				words[i] = stemmer.stem(words[i])
			new_obj[center] = list(set(words))

		with open("../data/intermediate_data/" + type_name +"_words_table.txt",'w') as f:
			json.dump(new_obj, f, sort_keys=True, indent=4, separators=(',', ': '))
	# # print(" ".join(SnowballStemmer.languages))