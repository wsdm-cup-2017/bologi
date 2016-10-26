# coding: utf-8
import numpy as np
import pandas
from pandas import DataFrame
from pandas import Series
import math
import gzip
import json
import sys
import pickle
from io import StringIO

def read_triple_file(typename, path):
  df_triple = pandas.read_csv(path, names=['name' , typename , 'score'],
                                    sep='\t', encoding='utf-8')
  return df_triple

def read_word_vectors(filename):
  word_vecs = {}

  with open("newfile", 'r') as f:
    meta_info = f.readline()
    print("Meta info for", filename, ": ", meta_info)
    entry_ct = 200 #f.readline()[1]

    for _, line in enumerate(f):
      if not line:
          continue
      key = line.split()[0].lower()
      word_vecs[key] = np.array(line.split()[1:]) #np.loadtxt(StringIO(line), usecols=range(1,entry_ct+1))

  sys.stderr.write("Finished parsing vectors from: "+filename+" \n")
  return word_vecs

def save_obj(obj, filepath_out):
    with open(filepath_out + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def map_word_to_vector(out_file_prefix, vec_dict, words_col):
  word_to_vec = {}
  word_not_found = {}
  words_col.drop_duplicates(inplace = True)

  for word in words_col:
    word_processed = word.replace(" ","").lower()

    if vec_dict.has_key(word_processed):
      word_to_vec[word_processed] = vec_dict[word_processed]
    else:
      word_not_found[word] = word_processed

  save_obj(word_to_vec, "./data/output_data/" + out_file_prefix + "_vector")
  save_obj(word_not_found, "./data/output_data/" + out_file_prefix + "_notfound")

def main():
  # read in file
  df_profession_train = read_triple_file("profession", "./data/raw_data/profession.train")
  df_nationality_train = read_triple_file("nationality", "./data/raw_data/nationality.train")
  vec_dict = read_word_vectors("vectors-enwikitext_vivek200.txt")

  # map word to vector if available, save unmatched words to another file
  map_word_to_vector("profession", vec_dict, df_profession_train.profession)
  map_word_to_vector("name_Profession", vec_dict, df_profession_train.name)
  map_word_to_vector("nationality", vec_dict, df_nationality_train.nationality)
  map_word_to_vector("name_Nationality", df_nationality_train.name)

if __name__ == '__main__':
    main()
