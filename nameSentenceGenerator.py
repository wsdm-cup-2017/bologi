import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series
from sets import Set
from util import output_as_json

#Author: Zhuang,Yiwei
#Date created:   2016.Oct.05

#read all names from profession.train
#input: path of profession.trains r
#output: a Series of names
def read_name_from_profession(path):
	s1 = pd.read_csv(path, names = ['name' , 'occupation' , 'score'] , sep = '\t', encoding = 'utf-8')
	train_names = s1.name
	train_names.drop_duplicates(inplace = True)
	# print(train_names)
	return train_names

#read all occupation from profession.train
#input: path of profession.trains r
#output: a Series of jobs
def read_occupation_from_profession(path):
	s1 = pd.read_csv(path, names = ['name' , 'occupation' , 'score'] , sep = '\t', encoding = 'utf-8')
	job_names = s1.occupation
	job_names.drop_duplicates(inplace = True)
	return job_names

#read all name job pairs from profession.train
#input: path of profession.trains r
#output: a DataFrame of name job pairs
def read_NameJob_pair_from_profession(path):
	s1 = pd.read_csv(path, names = ['name' , 'occupation' , 'score'] , sep = '\t', encoding = 'utf-8')
	pairs = DataFrame(s1)
	pairs = pairs.drop('score',1)
	#print(pairs)
	return pairs

#Find all the names in a sentence
#input:  be a sentence from wiki
#output: a list of raw names eg. [[Brack_Obama|Obama], [Lady_Gaga|gaga]]
def find_names_in_One_Sentence(sentence):
	start_idx 			= 0
	end_idx	  			= 0

	result 				= []
	for i in range(len(sentence)):
		if sentence[i] =='[' :
			start_idx = i+1
		elif sentence[i] == ']':
			end_idx = i
			result.append(sentence[start_idx : end_idx])
			start_idx = 0
			end_idx   = 0

	return result

#Parse a list of names
#input: a list of raw names eg. ["Brack_Obama|Obama" , "Lebron_James|James"
#output: clean names ['Brack Obama' , 'Lebron James']
def parse_names(raw_names):
	names = []
	for raw_name in raw_names:
		vertical_idx = 0
		for i in range(len(raw_name)):
			if raw_name[i] == '|':
				vertical_idx =  i
		name = raw_name[0:vertical_idx]
		name = name.replace("_"," ")
		names.append(name)

	return names


#Find related sentence for a sepcific person
#input:None
#output: A dictionary eg. {'Obama': [sentence1, sentence2] , 'Lebron James': [s3,s4]}
def find_related_sentence_from_wiki():
	profession_path = "./data/raw_data/profession.train"
	wiki_path		= "./data/sample"

	train_names = read_name_from_profession(profession_path)
	s1 = pd.read_csv(wiki_path, names = ['sentences'] , sep = '.\n',engine='python')
	Sentences = s1.sentences
	result_dict = {}

	for sentence in Sentences:
		names_in_sentence = find_names_in_One_Sentence(sentence)
		clean_names 	  = parse_names(names_in_sentence)
		for c_name in clean_names:
			if 1:#train_names.str.contains(c_name).any():
				print(c_name)
				if not c_name in result_dict.keys():
					result_dict[c_name] = [sentence]
				else:
					result_dict[c_name].append(sentence)
	return result_dict

#call function
output_as_json(find_related_sentence_from_wiki(), "./data/nameToSentences.json")