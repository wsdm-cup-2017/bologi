#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
__author__ = "Jiayu Chen"
from collections import defaultdict
import pickle
import pprint

def create_name2sentences_dict_from_wiki(wiki_path, c_lowb, c_highb, should_in_outbound):
  '''
  Create name2sentences lookup dictionary for all people, w/ one pass reading wiki
  Due to memory constrain, the entire dictionary is splitted into several sub-dictionaries,
  splitted according to the lowercased first letter of key, i.e. cleaned person name

  :param str wiki_path: path to wiki file
  :param int c_lowb: lower inclusive bound of generated dict keys
  :param int c_highb: higher exclusive bound of generated dict keys
  :param bool should_in_outbound: when true, generated dict has keys in [c_lowb, c_highb); when false, take the negation
  :return dict dict_ret: A dictionary with cleaned name as key, set as value, i.e. no duplicates
                        e.g. {'Brack Obama': [sentence1, sentence2] , 'Lebron James': [s3,s4]}
  '''
  dict_ret = defaultdict(set)
  with open(wiki_path, 'r') as f:
    for sentence in f:
      # => check if should update when scanned '[name]''
      start_idx = 0
      for i in range(len(sentence)):
        if sentence[i] =='[' :
          start_idx = i+1

        elif sentence[i] == ']':
          # take care bracket mismatch, simply ignore for now
          if start_idx >= i:
            continue

          raw_name = sentence[start_idx : i]

          c_first = ord(raw_name[0].lower())
          if (c_lowb <= c_first and c_first < c_highb) !=  should_in_outbound:
            # => parse name into clean string
            for i in range(len(raw_name)):
              if raw_name[i] == '|':
                #got cleaned name, break the loop once updated dict
                c_name = raw_name[0:i].replace("_"," ")
               # print "- Inserted", c_name
                dict_ret[c_name].add(sentence)

                #tmp for tracking progress
                if len(dict_ret) % 15000 == 0:
                  print len(dict_ret)

                break

  return dict_ret


def load_dict(dict_prefix, lowb, highb):
  '''
  Load pickle dictionary into memory
  :param str dict_prefix: prefix for output file name
  :param str/char lowb/highb: bound for dict should be [lowb, highb)
  '''
  with open(dict_prefix + lowb + "-" + highb +".p", "rb" ) as f:
    restored_dict = pickle.load(f)
  return restored_dict

if __name__=='__main__':
  dict_len = 0
  wiki_path = "/media/training-datasets/triple-scoring/wsdmcup17-triple-scoring-training-dataset-2016-09-16/wiki-sentences"#"../data/raw_data/wiki-sentences"

  # [Memo] sub-dict len1: 93897; len2: 63948, len3: 50037, len4: 77394, len5: 83419, len6:24056
  # save dicts into several sub-dicts, split based on lower-cased first letter of key
  # TODO: adjust the number of splits to optimize performance
  intervals = [ord('a'), ord('d'), ord('g'), ord('j'), ord('n'), ord('r'), ord('u')]
  name2sentence = None

  for i in range(4,len(intervals)):
    is_last_interval = i + 1 == len(intervals)
    lowb = intervals[0] if is_last_interval else intervals[i]
    highb = intervals[i] if is_last_interval else intervals[i+1]
    # make partial dict
    del name2sentence
    name2sentence = create_name2sentences_dict_from_wiki(wiki_path, \
                      lowb, highb, is_last_interval)
    # save to disk
    prefix = "../data/intermediate_data/name2sentence/name2sentence_"
    if is_last_interval:
      prefix += "NOT_"
    pickle.dump( name2sentence, open(prefix + chr(lowb) + "-" + chr(highb) +".p", "wb" ))

    print "Generated dict PT", i, "=> name2sentence size", len(name2sentence), ":\n"
    dict_len += len(name2sentence)


  # print "expect total: 385,426; Got total:", dict_len

  '''
  test code for reloading some sub-dictionary,
  please revise params for load_dict accordingly
  '''
  # restored_dict = load_dict("../data/intermediate_data/name2sentence/name2sentence_NOT_", chr(intervals[0]), chr(intervals[5]))
  # print "restored => name2sentence size", len(restored_dict)#, restored_dict.keys()
  # print restored_dict['Vilen KÃ¼nnapu'], "------------------\n"
  # print restored_dict[ 'Vilen KÃ¼nnapu'.decode("utf-8")], "------------------\n"
  # for key, val in restored_dict.iteritems():
  #   print key, "=>", len(val)
  #   pprint.pprint(val)
