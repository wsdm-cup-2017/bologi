#coding: utf-8
import numpy
import pandas
from pandas import DataFrame
from pandas import Series
import math
import gzip
import json
import sys
import pickle

coding="utf-8"
#read all names from profession.train
#input: path of profession.trains r 
#output: a Series of names 
def Read_name_from_profession(path):
	s1 = pandas.read_csv(path, names = ['name' , 'occupation' , 'score'] , sep = '\t', encoding = 'utf-8')
	train_names = s1.name
	train_names.drop_duplicates(inplace = True)
	return train_names

def Read_name_from_nationality(path):
	s1 = pandas.read_csv(path, names = ['name' , 'nationality' , 'score'] , sep = '\t', encoding = 'utf-8')
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
	s1 = pandas.read_csv(path, names = ['name' , 'nation' , 'score'] , sep = '\t', encoding = 'utf-8')
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

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

dict_vectors = read_word_vectors("vectors-enwikitext_vivek200.txt")
name_vector_pair={}
profession_vector_pair={}
nationality_vector_pair={}
namefromNation_vector_pair={}
namefromNation_notfound={}
name_notfound={}
profession_notfound={}
nationality_notfound={}
for name in Read_name_from_profession("profession.train") :
	name_origin=name
	name=name.replace(" ","")
	name=name.lower()
	if dict_vectors.has_key(name):
		name_vector_pair[name] = dict_vectors[name]
	else:
		name_notfound[name_origin] = name
save_obj(name_vector_pair, "name_vector")
save_obj(name_notfound, "name_notfound")

for profession in Read_occupation_from_profession("profession.train"):
	profession_origin=profession
	profession=profession.replace(" ","")
	profession=profession.lower()
	if dict_vectors.has_key(profession):
		profession_vector_pair[profession] = dict_vectors[profession]
	else:
		profession_notfound[profession_origin] = profession
save_obj(profession_vector_pair, "profession_vector")
save_obj(profession_notfound, "profession_notfound")

for nationality in Read_nation_from_nationality("nationality.train"):
	nationality_origin=nationality
	nationality=nationality.replace(" ","")
	nationality=nationality.lower()
	if dict_vectors.has_key(nationality):
		nationality_vector_pair[nationality] = dict_vectors[nationality]
	else:
		nationality_notfound[nationality_origin] = nationality
save_obj(nationality_vector_pair, "nationality_vector")
save_obj(nationality_notfound, "nationality_notfound")

for name in Read_name_from_nationality("nationality.train"):
	name_origin=name
	name=name.replace(" ","")
	name=name.lower()
	if dict_vectors.has_key(name):
		namefromNation_vector_pair[name] = dict_vectors[name]
	else:
		namefromNation_notfound[name_origin] = name
save_obj(namefromNation_vector_pair, "namefromNation_vector")
save_obj(namefromNation_notfound, "namefromNation_notfound")