#coding: utf-8
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series
import json
import sys
import pickle
#Author: Zhuang,Yiwei
#Date created:   2016.Oct.05


coding="utf-8"
#read all names from profession.train
#input: path of profession.trains r
#output: a Series of names
def Read_name_from_profession(path):
  s1 = pd.read_csv(path, names = ['name' , 'occupation' , 'score'] , sep = '\t', encoding = 'utf-8')
  train_names = s1.name
  train_names.drop_duplicates(inplace = True)
  return train_names

def Read_name_from_kb(path):
  s1 = pd.read_csv(path, names = ['name' , 'occupation'] , sep = '\t', encoding = 'utf-8')
  kb_names = s1.name
  kb_names.drop_duplicates(inplace = True)
  return kb_names

#read all occupation from profession.train
#input: path of profession.trains r
#output: a Series of jobs
def Read_occupation_from_profession(path):
  s1 = pd.read_csv(path, names = ['name' , 'occupation' , 'score'] , sep = '\t', encoding = 'utf-8')
  job_names = s1.occupation
  job_names.drop_duplicates(inplace = True)
  return job_names


#read all nations from nationality.train
#input: path of nationality.trains
#output: a Series of jobs
def Read_nation_from_nationality(path):
  s1 = pd.read_csv(path, names = ['name' , 'nation' , 'score'] , sep = '\t', encoding = 'utf-8')
  nation_names = s1.nation
  nation_names.drop_duplicates(inplace = True)
  return nation_names

#read all name nation pairs from nationality.train
#input: path of nationality.trains r
#output: a DataFrame of name  pairs
def Read_NameNation_pair_from_nationality(path):
  s1 = pd.read_csv(path, names = ['name' , 'nation' , 'score'] , sep = '\t', encoding = 'utf-8')
  pairs = DataFrame(s1)
  #pairs = pairs.drop(pairs[ pairs.score == 0 ].index, inplace=True)
  pairs = pairs[pairs.score != 0]
  pairs = pairs.drop('score',1)
  pairs = pairs.reset_index(drop=True)
  return pairs

def Read_NameNation_pair_from_nationality_kb(path):
  s1 = pd.read_csv(path, names = ['name' , 'nation' ] , sep = '\t', encoding = 'utf-8')
  pairs = DataFrame(s1)
  return pairs

#read all name job pairs from profession.train
#input: path of profession.trains r
#output: a DataFrame of name job pairs
def Read_NameJob_pair_from_profession(path):
  s1 = pd.read_csv(path, names = ['name' , 'occupation' , 'score'] , sep = '\t', encoding = 'utf-8')
  pairs = DataFrame(s1)
  # pairs.drop(pairs[ pairs.score == 0 ].index, inplace=True)
  pairs = pairs[pairs.score != 0]
  pairs = pairs.drop('score',1)
  pairs = pairs.reset_index(drop=True)
  return pairs

def Read_NameJob_pair_from_kb(path):
  s1 = pd.read_csv(path, names = ['name' , 'occupation' ] , sep = '\t', encoding = 'utf-8')
  pairs = DataFrame(s1)
  return pairs

#Find all the names in a sentence
#input:  be a sentence from wiki
#output: a list of raw names eg. [[Brack_Obama|Obama], [Lady_Gaga|gaga]]
def Find_names_in_One_Sentence(sentence):
  start_idx       = 0
  end_idx          = 0

  result         = []
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
def Parse_names(raw_names):
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
def Find_related_sentence_from_wiki():
  profession_path = "profession.train"
  wiki_path    = "wiki-sentences"

  train_names = Read_name_from_profession(profession_path)
  #s1 = pd.read_csv(wiki_path, names = ['sentences'] , sep = '\n',engine='python', encoding = 'utf-8')
  s1 = pd.read_csv(wiki_path, names = ['sentences'] , sep = '\n', encoding = 'utf-8')
  Sentences = s1.sentences
  result_dict = {}

  for sentence in Sentences:
    names_in_sentence = Find_names_in_One_Sentence(sentence)
    clean_names     = Parse_names(names_in_sentence)
    for c_name in clean_names:
      if train_names.str.contains(c_name).any():
        if not c_name in result_dict.keys():
          result_dict[c_name] = [sentence]
        else:
          result_dict[c_name].append(sentence)
  return result_dict

def write_sentences_to_file():
  fo = open("name_sentence_dict.json", 'w')
  result = Find_related_sentence_from_wiki()
  json.dump(result, fo)

#res = Find_related_sentence_from_wiki()
#write_sentences_to_file()

#res = Read_NameJob_pair_from_profession("/Users/Zhuangyiwei/Desktop/triple-scoring/profession.train")
#print(res.get_value(1,'name'))
#print(res)

# ============== cjy added: 11/22 ==================
# create name2sentences lookup for all people, w/ one pass reading wiki
# input:None
# output: A dictionary eg. {'Obama': [sentence1, sentence2] , 'Lebron James': [s3,s4]}
def create_name2sentences_dict_from_wiki():
  wiki_path    = "./data/sample" #/data/raw_data/wiki-sentences"
  result_dict = {}
  #s1 = pd.read_csv(wiki_path, names = ['sentences'] , sep = '\n',engine='python', encoding = 'utf-8')
  with open(wiki_path, 'r') as f:
    for sentence in f:
      if not sentence:
          continue

      names_in_sentence = Find_names_in_One_Sentence(sentence)
      clean_names     = Parse_names(names_in_sentence)
      for c_name in clean_names:
        # if train_names.str.contains(c_name).any():
        if not c_name in result_dict.keys():
          result_dict[c_name] = [sentence]
          if (len(result_dict) % 5000 == 0):
          	print len(result_dict)
        else:
          result_dict[c_name].append(sentence)
  return result_dict

# name2sentence = create_name2sentences_dict_from_wiki()
# pickle.dump( name2sentence, open( "name2sentence.p", "wb" ) )
# print "name2sentence size", len(name2sentence), ":\n"
# restored_dict = pickle.load( open( "name2sentence.p", "rb" ) )
# print "restored => name2sentence size", len(restored_dict)
