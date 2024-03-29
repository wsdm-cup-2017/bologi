#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import pandas as pd
from pandas import DataFrame

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
# import pprint

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

# linear mapping frequency count to score [0-7]
# input a dictionary, score as val
def normalize(s):
    maxv=max(s.itervalues())

    for k in s:
      try:
        s[k] = float(s[k]) / maxv * 7
      except:
        print "type(maxv) ", maxv
    return s


def maxto7(attr_score_dic):
    maxi = 0
    maxs = 0
    for i in range(len(attr_score_dic)):
      score = attr_score_dic.values()[i]
      if score >= maxs:
        maxs = score
        maxi = i

    i = 0
    for attr, _ in attr_score_dic.iteritems():
      if i == maxi:
        attr_score_dic[attr] = 7
        # print "MAX  ", attr
        break
      else:
        i += 1
    return


def match_name_attr(s, attr, baseline):
  content_in_bracket = s[s.find("(")+1:s.find(")")].lower()

  if content_in_bracket is None:
    return baseline
  else:
    if content_in_bracket == attr.lower():
      return 7.0

    # print content_in_bracket.encode('utf-8'), type(content_in_bracket)
    tokens_bracket = content_in_bracket.encode('utf-8').split()
    tokens_attr = attr.lower().split()

    match_ct = 0
    for t_bracket in tokens_bracket:
      if t_bracket in tokens_attr:
        match_ct += 1

    init_score = max(baseline, float(match_ct)/len(t_bracket)*7)
  return init_score

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
        stemmed_word = stemmer.stem(word) # will throw error for some unicode
      except:
        tmp = 1
        # print "Cannot stem: ", word

      for i in range(n):
        relevant_words = relevant_words_pool[i]
        if relevant_words is None:
          continue
        try:
          if word in relevant_words or stemmed_word in relevant_words: #/home/bologi/bologi/src/cjy_predict.py:99:
            # UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
            attr = attr_score.items()[i][0]
            attr_score[attr] += 1.0
        except:
          print "[word not in relevant] word: ", word

  attr_score = normalize(attr_score)


# new add 12.8
def cal_score_from_dict_and_table(in_path, name2sentences, table_path, dict_triple):
  attr_table = load_json(table_path)

  for name, attr_score in dict_triple.iteritems():
      triple_ct = len(attr_score)
      name_key = name#!!No need can pass.encode("utf-8") # because stored as unicode string before by pandas

      if name_key not in name2sentences:
          # print "=> Not Found: [", name,"]"
          continue
      sentences = name2sentences[name_key]

      count_score_from_table_for_one_person(attr_score, attr_table, sentences)
  return


def predice_triple_using_dict(input_path, output_path, table_path, baseline):
    # dict to store prediction result, while keeping original order w/ input
    dict_triple = OrderedDefaultDict(OrderedDefaultDict)
    df_out = pd.DataFrame(columns = ['name','job', 'score'])

    # read in pair file, init guess to be 1
    s1 = pd.read_csv(input_path, names = ['name' , 'attribute' , 'score'] , sep = '\t', encoding = 'utf-8')
    df_in = DataFrame(s1)
    for index, row in df_in.iterrows():
        # check if name contains (specifier as hint to answer)
        init_score = match_name_attr(row['name'], row['attribute'], baseline)
        dict_triple[row['name']][row['attribute']] = init_score

    # load sub-dictionary one by one, used to look up for wiki-sentences
    name2sentences = None
    intervals = [ord('a'), ord('d'), ord('g'), ord('j'), ord('n'), ord('r'), ord('u')]
    for i in range(len(intervals)):
      print "[predice_triple_using_dict]: Round", i, "/", len(intervals), "..."
      is_last_interval = i + 1 == len(intervals)
      lowb = intervals[0] if is_last_interval else intervals[i]
      highb = intervals[i] if is_last_interval else intervals[i+1]

      prefix = "../data/intermediate_data/name2sentence/name2sentence_"
      if is_last_interval:
        prefix += "NOT_"
      del name2sentences
      name2sentences = load_dict(prefix, chr(lowb), chr(highb))
      # predict
      cal_score_from_dict_and_table(input_path, name2sentences, table_path, dict_triple)

    # store result to file
    for _, job_score_pair in dict_triple.iteritems():
        # round the highest score to 7 for each person
        maxto7(job_score_pair)

    i = 0
    for name, job_score_pair in dict_triple.iteritems():
        for job, score in job_score_pair.iteritems():
            df_out.loc[i] = [name, job, round(score)]
            i += 1

    df_out[['score']] = df_out[['score']].astype(int)
    df_out.set_index(keys = ['name'] , inplace = True)
    df_out.to_csv(output_path, header=None, sep = '\t', encoding='utf-8')