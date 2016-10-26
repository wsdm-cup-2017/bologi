import numpy as np 
import pandas as pd 
from pandas import DataFrame
from pandas import Series
from NameSentenceGenerator import Find_names_in_One_Sentence
from NameSentenceGenerator import Parse_names
from NameSentenceGenerator import Read_NameJob_pair_from_kb



def read_JobWord_table(path):
	with open(path) as data_file:
		data = json.load(data_file)
	return data

def Find_related_sentences_from_wiki_for_each_person(name):
	wiki_path		= "/Users/Zhuangyiwei/Desktop/triple-scoring/wiki-sentences"
	s1 = pd.read_csv(wiki_path, names = ['sentences'] , sep = '\n', encoding = 'utf-8')
	Sentences = s1.sentences
	result_list = []

	for sentence in Sentences:
		names_in_sentence = Find_names_in_One_Sentence(sentence)
		clean_names 	  = Parse_names(names_in_sentence)
		for c_name in clean_names:
			if name == c_name:
				result_list.append(sentence)
	return result_list

def Predict_each_job(occupations, table, sentences):
	res   = {}
	for job in occupations:
		specific_words = table[job]
		for sentence in sentences:
			for word in sentence:
				if word in specific_words:
					res[job] += specific_words[word]

	return res

def Predict_each_person(name, occupations, table):
	sentences = Find_related_sentences_from_wiki_for_each_person(name)
	return Predict_each_job(occupations,table,sentences)

def Slice_for_each_person(pairs):
	res = {}
	for index, row in pairs.iterrows():
		people_name = pairs.get_value(index,'name')
		people_job  = pairs.get_value(index,'occupation')
		if not people_name in res.keys():
			res[people_name] = [people_job]
		else:
			res[people_name].append(people_job)

	return res

def Predict_all(kb_path):
	all_pairs =  Read_NameJob_pair_from_kb(kb_path)
	name_job_dict = Slice_for_each_person(all_pairs)
	table = read_JobWord_table("")
	res = {}
	for name, jobs in name_job_dict:
		res[name] = Predict_each_person(name,jobs,table)


