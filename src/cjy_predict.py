#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series
from NameSentenceGenerator import Read_name_from_profession
import ast
import json
import re
import sys
import os
import pickle

def normalize(s):
    minv=min(s.itervalues())
    maxv=max(s.itervalues())

    if minv==maxv :
        score=7
        if minv==0:
            score=0
        for k in s:
            s[k]= score
        return s

    factor =float(7)/(maxv-minv)
    for k in s:
        s[k]=int(round(((s[k])-minv)*factor))

    return s

def read_table(path):
    return json.load(open(path))

def Read_NameJob_pair_from_testfile(path):
    s1 = pd.read_csv(path, names = ['name' , 'occupation' , 'score'] , sep = '\t', encoding = 'utf-8')
    pairs = DataFrame(s1)
    # pairs.drop(pairs[ pairs.score == 0 ].index, inplace=True)
    pairs = pairs.drop('score',1)
    pairs = pairs.reset_index(drop=True)
    return pairs

def Read_NameNation_pair_from_testfile(path):
    s1 = pd.read_csv(path, names = ['name' , 'nation' , 'score'] , sep = '\t', encoding = 'utf-8')
    pairs = DataFrame(s1)
    pairs = pairs.drop('score',1)
    pairs = pairs.reset_index(drop=True)
    return pairs

def Find_test_sentence_from_wiki(testfile):

    wiki_path	= "wiki-sentences"
    train_names = Read_name_from_profession(testfile)
#    print ("train name is", train_names)
    #s1 = pd.read_csv(wiki_path, names = ['sentences'] , sep = '\n',engine='python', encoding = 'utf-8')
    s1 = pd.read_csv(wiki_path, names = ['sentences'] , sep = '\n', encoding = 'utf-8')
    Sentences = s1.sentences
    result_dict = {}

    for sentence in Sentences:
        names_in_sentence = Find_names_in_One_Sentence(sentence)
        clean_names 	  = Parse_names(names_in_sentence)
        for c_name in clean_names:
            if train_names.str.contains(re.escape(c_name)).any():
                if not c_name in result_dict.keys():
                    result_dict[c_name] = [sentence]
                else:
                    result_dict[c_name].append(sentence)
    print ("the len of sentence dict is", len(result_dict), len(train_names))
    return result_dict


def write_test_sentences_to_file(testfile):
    result = Find_test_sentence_from_wiki(testfile)
    with open("name_sentence_dict.json", 'w') as fo:
        json.dump(result, fo)


def Predict_each_job_freq(occupations, table, sentences):
    res   = {}
    for job in occupations:
        res[job] = 0
    for job in occupations:
        if job not  in table.keys():
            res[job] = 0
            continue
        specific_words = table[job]
        for sentence in sentences:
            for word in sentence.split(' '):
                if word in specific_words:
                        res[job] += 1
                # except:
                #     print "error word: ", word

    res = normalize(res)
    return res

def Slice_for_each_person(pairs):
    res = {}
    for index, row in pairs.iterrows():
        res[row['name']] = []

    for index, row in pairs.iterrows():
        res[row['name']].append(row['occupation'])

    return res

def Slice_for_each_person_nation(pairs):
    res = {}
    for index, row in pairs.iterrows():
        res[row['name']] = []

    for index, row in pairs.iterrows():
        res[row['name']].append(row['nation'])

    return res


def read_sentence_train(path):
    return json.load(open(path))


#Modified by Li, add path as arguments of function
def Predice_train_file_job(prof_path, prof_result_path):
    job_Pair =  Read_NameJob_pair_from_testfile(prof_path)
    job_table = read_table("../data/intermediate_data/prof_words_table.txt")
    res = pd.DataFrame(columns = ['name','job', 'score'])
    names_in_job= Read_name_from_profession(prof_path)

    sentences = read_sentence_train("../data/intermediate_data/name_sentence_dict.json")
    slices = Slice_for_each_person(job_Pair)
    i=0
    for index, row in job_Pair.iterrows():
        name = row['name']
        job  = row['occupation']
        if name not in sentences.keys():
            print name
            continue
        job_score_pairs = Predict_each_job_freq(slices[name],job_table,sentences[name])

        res.loc[i] = [name, job, round(job_score_pairs[job])]
        i+=1

    res.set_index(keys = ['name'] , inplace = True)
    res.to_csv(prof_result_path, header=None, sep = '\t')
    return

#Modified by Li, add path as arguments of function
def Predice_train_file_nation(nation_path, nation_result_path):
    nation_Pair =  Read_NameNation_pair_from_testfile(nation_path)
    names_in_nation = Read_name_from_profession(nation_path)
    nation_table = read_table("../data/intermediate_data/nation_words_table.txt")
    res = pd.DataFrame(columns = ['name','nation', 'score'])

    sentences = read_sentence_train("name_sentence_dict.json")
    slices = Slice_for_each_person_nation(nation_Pair)
    i=0
    for index, row in nation_Pair.iterrows():
        name = row['name']
        nation  = row['nation']
        if name not in sentences.keys(): continue
        job_score_pairs = Predict_each_job_freq(slices[name],nation_table,sentences[name])

        res.loc[i] = [name, job, round(job_score_pairs[job])]
        i+=1


    res.set_index(keys = ['name'] , inplace = True)
    res.to_csv(nation_result_path, header=None, sep = '\t')
    return


# added by cjy 11/23
def predice_train_file_job_using_dict_helper(prof_path, prof_result_path, name2sentences, df_out):
    print "in predice_train_file_job_using_dict"
    job_Pair =  Read_NameJob_pair_from_testfile(prof_path)
    job_table = read_table("../data/intermediate_data/prof_words_table.txt")
    names_in_job= Read_name_from_profession(prof_path)

    # sentences = read_sentence_train("name_sentence_dict.json")
    print "dict: name2sentences loaded"
    slices = Slice_for_each_person(job_Pair)
    i = df_out.shape[0]
    for index, row in job_Pair.iterrows():
        #!!!SHOULD NOT NEED TO STRIP IF INPUT FORMAT IS CORRECT WITH NO EXTRA SPACE .strip()
        name = row['name']
        name_key = name.encode("utf-8") # because stored as unicode string before by pandas

        job  = row['occupation']
        if name_key not in name2sentences:
            # print "=> Not Found: [", name,"]"
            continue
        # else:
        #     print "==> :)))) Found: ", name
        job_score_pairs = Predict_each_job_freq(slices[name],job_table,name2sentences[name_key])

        df_out.loc[i] = [name, job, round(job_score_pairs[job])]
        i+=1

    return

# load pickle dictionary into memory
# @param: lowb, highb as char
def load_dict(dict_prefix, lowb, highb):
    filename = dict_prefix + lowb + "-" + highb +".p"
    with open(filename, "rb" ) as f:
      restored_dict = pickle.load(f)
    print "===> Opened ", filename
    return restored_dict

def predice_train_file_job_using_dict(prof_path, prof_result_path):
    name2sentences = None
    print "in predice_train_file_job_using_dict"
    df_out = pd.DataFrame(columns = ['name','job', 'score'])

    intervals = [ord('a'), ord('d'), ord('g'), ord('j'), ord('n'), ord('r'), ord('u')]
    for i in range(len(intervals)):
      print i, "==============================>\n"
      is_last_interval = i + 1 == len(intervals)
      lowb = intervals[0] if is_last_interval else intervals[i]
      highb = intervals[i] if is_last_interval else intervals[i+1]

      prefix = "../data/intermediate_data/name2sentence/name2sentence_"
      if is_last_interval:
        prefix += "NOT_"
      del name2sentences
      name2sentences = load_dict(prefix, chr(lowb), chr(highb))
      predice_train_file_job_using_dict_helper(prof_path, prof_result_path, name2sentences, df_out)

    df_out.set_index(keys = ['name'] , inplace = True)
    df_out.to_csv(prof_result_path, header=None, sep = '\t', encoding='utf-8')