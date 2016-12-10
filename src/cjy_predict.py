#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
from pandas import DataFrame
# from pandas import Series
import ast
import json
import re
import sys
import os
import pickle
import random

from collections import OrderedDict, defaultdict
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import SnowballStemmer
import pprint

stemmer = SnowballStemmer("english")
class OrderedDefaultDict(OrderedDict, defaultdict):
    def __init__(self, default_factory=None, *args, **kwargs):
        #in python3 you can omit the args to super
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory


def load_json(path):
    return json.load(open(path))

# load pickle dictionary into memory
# @param: lowb, highb as char
def load_dict(dict_prefix, lowb, highb):
    filename = dict_prefix + lowb + "-" + highb +".p"
    with open(filename, "rb" ) as f:
      restored_dict = pickle.load(f)
    # print "===> Opened ", filename
    return restored_dict

def store_input_file_as_df(path):
    s1 = pd.read_csv(path, names = ['name' , 'attribute' , 'score'] , sep = '\t', encoding = 'utf-8')
    pairs = DataFrame(s1)
    # pairs.drop(pairs[ pairs.score == 0 ].index, inplace=True)
    pairs = pairs.drop('score',1)
    pairs = pairs.reset_index(drop=True)
    return pairs

# map frequency count to score [0-7]
# input a dictionary, score as val
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


def maxto7(df, starti, endi):
    maxi = starti
    maxs = 0
    for i in range(starti, endi):
        score = df.loc[i]['score']
        if score > maxs:
            maxs = score
            maxi = i
    df.loc[maxi,'score'] = 7
    return

def match_name_attr(s, attr):
  content_in_bracket = s[s.find("(")+1:s.find(")")].lower()
  if content_in_bracket is None:
    return False
  else:
    if content_in_bracket == attr.lower():
      return True

    tokens = content_in_bracket
    if attr.lower() in tokens:
      return True
  return False

def count_score_from_table_for_one_person(attr_score, table_dic, sentences):
  n = len(attr_score)
  relevant_words_pool = [] #lower-cased attribute as key
  attr_key2attr = {} # used for lookup in second for loop

  # prepare relavant words pools for attributes-to-predict
  for attr, _ in attr_score.iteritems():
    if attr.lower() not in table_dic:
      print "[count_score_from_table_for_one_person]", attr.lower(), "not in dic"
      relevant_words_pool.append(None)
    else:
      relevant_words_pool.append(table_dic[attr.lower()])

  # one pass to accumulate word frequency
  for sentence in sentences:
    tokens = CountVectorizer(strip_accents='Unicode', lowercase=True).build_tokenizer()(sentence)
    # sentence.lower().split()

    for word in tokens:
      try:
        word = stemmer.stem(word) # will throw error for some unicode
      except:
        tmp = 1
      #   print "Cannot stem: ", word
      for i in range(n):
        relevant_words = relevant_words_pool[i]
        if relevant_words is None:
          continue
        try:
          if word in relevant_words: #/home/bologi/bologi/src/cjy_predict.py:99:
            # UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
            attr = attr_score.items()[i][0]
            attr_score[attr] += 1
        except:
          print "[word not in relevant] word: ", word

  attr_score = normalize(attr_score)


# new add 12.8
def cal_score_from_dict_and_table(in_path, name2sentences, table_path, dict_triple):
  attr_table = load_json(table_path)

  for name, attr_score in dict_triple.iteritems():
      triple_ct = len(attr_score)
      name_key = name#!!No need can pass.encode("utf-8") # because stored as unicode string before by pandas
      # check if name contains (specifier as hint to answer)
      for attr in attr_score.keys():
        if match_name_attr(name, attr) is True:
          attr_score[attr] = 7

      if name_key not in name2sentences:
          # print "=> Not Found: [", name,"]"
          continue
      sentences = name2sentences[name_key]
      # else:
      #     print "==> :)))) Found: ", name
      count_score_from_table_for_one_person(attr_score, attr_table, sentences)
  return


def predice_triple_using_dict(nation_path, nation_result_path, table_path):
    # dict to store prediction result, while keeping original order w/ input
    dict_triple = OrderedDefaultDict(OrderedDefaultDict)
    df_out = pd.DataFrame(columns = ['name','job', 'score'])

    # read in pair file, init guess to be 1
    s1 = pd.read_csv(nation_path, names = ['name' , 'attribute' , 'score'] , sep = '\t', encoding = 'utf-8')
    df_in = DataFrame(s1)
    for index, row in df_in.iterrows():
        dict_triple[row['name']][row['attribute']] = 1

    # load sub-dictionary one by one, used to look up for wiki-sentences
    name2sentences = None
    intervals = [ord('a'), ord('d'), ord('g'), ord('j'), ord('n'), ord('r'), ord('u')]
    for i in range(len(intervals)):
      print "[predice_triple_using_dict]: Round", i, "/", len(intervals),"\n"
      is_last_interval = i + 1 == len(intervals)
      lowb = intervals[0] if is_last_interval else intervals[i]
      highb = intervals[i] if is_last_interval else intervals[i+1]

      prefix = "../data/intermediate_data/name2sentence/name2sentence_"
      if is_last_interval:
        prefix += "NOT_"
      del name2sentences
      name2sentences = load_dict(prefix, chr(lowb), chr(highb))
      # predict
      cal_score_from_dict_and_table(nation_path, name2sentences, table_path, dict_triple)

    # store result to file
    i = 0
    for name, job_score_pair in dict_triple.iteritems():
        for job, score in job_score_pair.iteritems():
            df_out.loc[i] = [name, job, score]
            i += 1
        # round the highest score to 7 for each person
        maxto7(df_out, i-len(job_score_pair), i-1)
    df_out[['score']] = df_out[['score']].astype(int)
    df_out.set_index(keys = ['name'] , inplace = True)
    df_out.to_csv(nation_result_path, header=None, sep = '\t', encoding='utf-8')