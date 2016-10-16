#coding: utf-8
import numpy
import pandas
from pandas import DataFrame
from pandas import Series
import math
import gzip
import json
import sys

coding="utf-8"
#read all names from profession.train
#input: path of profession.trains r 
#output: a Series of names 
def Read_name_from_profession(path):
	s1 = pandas.read_csv(path, names = ['name' , 'occupation' , 'score'] , sep = '\t', encoding = 'utf-8')
	train_names = s1.name
	train_names.drop_duplicates(inplace = True)
	return train_names

#read all occupation from profession.train
#input: path of profession.trains r 
#output: a Series of jobs
def Read_occupation_from_profession(path):
	s1 = pandas.read_csv(path, names = ['name' , 'occupation' , 'score'] , sep = '\t', encoding = 'utf-8')
	job_names = s1.occupation
	job_names.drop_duplicates(inplace = True)
	return job_names

def Read_nation_from_nationality(path):
	s1 = pd.read_csv(path, names = ['name' , 'nation' , 'score'] , sep = '\t', encoding = 'utf-8')
	nation_names = s1.nation
	nation_names.drop_duplicates(inplace = True)
	return nation_names

def read_word_vectors(filename):    
	word_vecs = {}
	if filename.endswith('.gz'): file_object = gzip.open(filename, 'r')
	else: file_object = open(filename, 'r')

	for line_num, line in enumerate(file_object):
		line = line.strip().lower()
		word = line.split()[0]
		word_vecs[word] = numpy.zeros(len(line.split())-1, dtype=float)
		for index, vec_val in enumerate(line.split()[1:]):
			word_vecs[word][index] = float(vec_val)      
	sys.stderr.write("Vectors read from: "+filename+" \n")
	return word_vecs

dict_vectors = read_word_vectors("vectors-enwikitext_vivek200.txt")
name_vector_pair={}
profession_vector_pair={}
nationality_vector_pair={}
for name in Read_name_from_profession("profession.train") :
	name=name.replace(" ","")
	name=name.lower()
	name_vector_pair[name] = dict_vectors[name]
fo1 = open("name_vector.text", 'w')
json.dump(name_vector_pair, fo1)

# for profession in Read_occupation_from_profession("profession.train"):
# 	profession=profession.replace(" ","")
# 	profession=profession.lower()
# 	profession_vector_pair[profession] = dict_vectors[profession]
# fo2 = open("profession_vector.text", 'w')
# json.dump(profession_vector_pair, fo2)

# for nationality in Read_nation_from_nationality("nationality.train"):
# 	nationality=nationality.replace(" ","")
# 	nationality=nationality.lower()
# 	nationality_vector_pair[nationality] = dict_vectors[nationality]
# fo3 = open("nationality_vector.text", 'w')
# json.dump(nationality_vector_pair, fo3)