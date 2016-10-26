from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import json
import operator
from NameSentenceGenerator import Read_NameJob_pair_from_kb
from NameSentenceGenerator import Read_name_from_kb
from NameSentenceGenerator import Read_NameJob_pair_from_profession

#input: list of sentence
#output: td-idf value for each word in all sentences
def calculate_tfidf_for_sentences(sentences):
	vectorizer = TfidfVectorizer()
	X = vectorizer.fit_transform(sentences)
	idf = vectorizer.idf_
	return dict(zip(vectorizer.get_feature_names(), idf))

#input: dict of job sentence pair
#output: dict of each job with 12 highest tdidf value
def Find_specific_word_each_occupation(job_sentence):
	result = {}
	table  = [1, 0.5 , 0.333 , 0.25, 0.2 , 0.167 , 0.143 , 0.125, 0.111,0.1,0.091, 0.083 ]

	for job,sentences in job_sentence.iteritems():
		word_tfidf = calculate_tfidf_for_sentences(sentences)
		words_rank = {}
		rank 	   = 0
		sorted(word_tfidf.values())
		word_tfidf = word_tfidf.keys()
		for i in xrange(12):
			words_rank[word_tfidf[i]] = table[rank]
			rank= rank+1
		rank = 0 
		result[job] = words_rank

	return result


def read_data_write_file(path):
	with open(path) as data_file:
		data = json.load(data_file)	
	job_words_dict = Find_specific_word_each_occupation(data)
	fo = open("job_word_table2.txt", 'w')
	json.dump(job_words_dict, fo)

def read_data_all_words(path):
	with open(path) as data_file:
		data = json.load(data_file)
	all_sentence = []
	for job, sentences in data.iteritems():
		for sentence in sentences:
			all_sentence+=sentence
	tfidf = calculate_tfidf_for_sentences(all_sentence)
	return tfidf

def write_tfidf_all_words(path):
	fo = open("tfidf_all.txt",'w')
	tfidf_all = read_data_all_words(path)
	json.dump(tdidfall,fo)

def Predict_Output_Structure_train(train_path):
	NameJob_pair = Read_NameJob_pair_from_profession(train_path)
	result = {}
	for idx,row in NameJob_pair.iterrows():
		Name = row['name']
		#print Name
		Job  = row['occupation']
		#print Job
		if not Name in result.keys():
			jobScore_pair = {}
			jobScore_pair[Job] = 0
			result[Name] = jobScore_pair
		else:
			result[Name][Job]  = 0

	return result


def Predict_Output_Structure_kb(kb_path):
	NameJob_pair = Read_NameJob_pair_from_kb(kb_path)
	result = {}
	for idx,row in NameJob_pair.iterrows():
		Name = row['name']
		#print Name
		Job  = row['occupation']
		#print Job
		if not Name in result.keys():
			jobScore_pair = {}
			jobScore_pair[Job] = 0
			result[Name] = jobScore_pair
		else:
			result[Name][Job]  = 0

	return result


#input: 3 paths 
#output: A dict  {'Obama':{'Laywer':4.3,'Politician': 8.2,'Law Professor': 3.3}, 'Hillary':{},....}
# def Predict_from_wordsDict(wordDict_path, kb_path, nameSentence_path):
# 	with open(wordDict_path) as data_file:
# 		wordDitc = json.load(data_file)
	
# 	NameJob_pair = Read_NameJob_pair_from_kb(kb_path)
# 	result = {}
# 	for idx,row in NameJob_pair.iterrows():
# 		Name = row['name']
# 		Job  = row['occupation']
# 		if not Name in result.keys():
# 			jobScore_pair = {}
# 			jobScore_pair[Job] = Calculate_weight(Name,Job,wordDitc,nameSentence_path)
# 			result[Name] = jobScore_pair
# 		else:
# 			result[Name][Job]  = Calculate_weight(Name,Job,wordDitc,nameSentence_path)	

# 	return result

# def MapAll(wordDict_path, kb_path, nameSentence_path):
# 	res = Predict_from_wordsDict(wordDict_path, kb_path, nameSentence_path)
# 	for name,job_scores in res:
# 		res[name] = MapLinear(job_scores)

	








path = "/Users/Zhuangyiwei/Desktop/412project/prof_sentence_dict.txt"
#result = Predict_Output_Structure_kb("/Users/Zhuangyiwei/Desktop/triple-scoring/professiontest.kb")
#print result
#read_data_write_file(path)
read_data_write_file(path)
#write_tfidf_all_words(path)

