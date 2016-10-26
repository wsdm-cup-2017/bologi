#!/usr/bin/env python3
__author__ = "Jiayu Chen"

import argparse
import os
import sys
import string
import re
from re import split

# Specify and parse cmd line arguments
def parse_cmd_args():
    parser = argparse.ArgumentParser(description='Process command line arguments.')

    parser.add_argument('synfilename', help='file name for synonums')
    parser.add_argument('filename1', help='filename of the first target file')
    parser.add_argument('filename2', help='filename of the second target file')
    parser.add_argument('--tuple-size', dest='tuple_size', default=3, type=int,
                        help='length of each tuple')
    parser.add_argument('--max-dict-len', dest='dict_max_len', default=10000, type=int,
                        help='maximum length of dictionary allowed')

    args = parser.parse_args()
    return args

# Lowercase letters, remove puctuations, replace all synonyms with the same word,
# output as a single-line file
def preprocess_file(filename, dict_synonyms, synonym_marker):
    out_filename = filename + ".cp"
    translator = str.maketrans({key: None for key in string.punctuation})

    with open(filename, 'r') as f_in, open(out_filename, "wt") as f_out:
        for line in f_in:
            if not line:
                continue
            line = line.translate(translator).lower() # removed strip
            wordList = line.split()
            for i in range(len(wordList)):
                if wordList[i] in dict_synonyms:
                    wordList[i] = synonym_marker
                f_out.write(wordList[i] + " ")

    return out_filename

# Store word count in a dictionary
def map_file_to_dict(filename, tuple_size):
    dict = {}

    with open(filename, 'r') as f:
        for line in f:
            if not line:
                continue
            line = line.strip().lower()
            wordList = line.split()
            for i in range(len(wordList)):
                if i + tuple_size > len(wordList):
                    break
                word_tuple = " ".join(wordList[i:i + tuple_size])
                if word_tuple in dict:
                    dict[word_tuple] += 1
                else:
                    dict[word_tuple] = 1

    return dict

# word generator, used to avoid reading long chunk of file into memory
def words(file, buffer_size=2048):
    buffer = ''

    for chunk in iter(lambda: file.read(buffer_size), ''):
        words = re.split("\W+", buffer + chunk)
        buffer = words.pop()
        yield from (word.lower() for word in words if word)

    if buffer:
        yield buffer

# Map file to dictionary while using a word generator to avoid using too much memory at once
def map_file_to_dict_word_gen(word_gen, tuple_size, tuple_window, DICT_MAX_SIZE):
    dict = {}
    tuple_ct = 0

    while len(dict) <= DICT_MAX_SIZE:
        try:
            if len(tuple_window) == tuple_size:
                tuple_ct += 1
                word_tuple = " ".join(tuple_window)
                if word_tuple in dict:
                    dict[word_tuple] += 1
                else:
                    dict[word_tuple] = 1
                tuple_window.pop(0)
            tuple_window.append(next(word_gen))
        except StopIteration:
            break

    return dict, tuple_ct, word_gen, tuple_window


# Count # tuples in file1 that occurred in file2.
# Store file1 as a dictionary then use it to to sum over the count while scanning through file2
# Follow DICT_MAX_SIZE when creating dictionary, scan file1 in reasonable chunk size
def count_overlapped_tuples(filename2, filename1, tuple_size, DICT_MAX_SIZE):

    f1 = open(filename1, 'r')
    word_gen_1 = words(f1)

    overlap_tuple_ct = 0
    file1_tuple_ct = 0
    tuple_window_1 = []

    while True:
        # reset file2's word generator
        f2 = open(filename2, 'r')
        word_gen_2 = words(f2)
        tuple_window_2 = []

        # process chunk of file1
        dict_file1, tuple_ct, word_gen_1, tuple_window_1 = map_file_to_dict_word_gen(word_gen_1,
                                                           tuple_size, tuple_window_1, DICT_MAX_SIZE)
        file1_tuple_ct += tuple_ct
        if not dict_file1:
            break

        # scan through file2 to accumulate overlapped tuple counts
        while True:
            try:
                if len(tuple_window_2) == tuple_size:
                    word_tuple = " ".join(tuple_window_2)
                    if word_tuple in dict_file1:
                        overlap_tuple_ct += dict_file1[word_tuple]
                        del dict_file1[word_tuple]
                    tuple_window_2.pop(0)
                tuple_window_2.append(next(word_gen_2))
            except StopIteration:
                break

    f1.close()
    f2.close()
    return overlap_tuple_ct, file1_tuple_ct


def main():
    # Parse arguments, 2 input files to check against required,
    # continue even if failed to open synonyms file
    args = parse_cmd_args()
    if os.path.exists(args.filename1) == False:
        print("Err: file doesn't exist:", args.filename1,
              "please correct the file path to continue.")
        sys.exit(1)

    if os.path.exists(args.filename2) == False:
        print("Err: file doesn't exist:", args.filename1,
              "please correct the file path to continue.")
        sys.exit(1)

    if os.path.exists(args.synfilename) == False:
        print("Warning: file doesn't exist:", args.synfilename,
              "Continue without synonyms supplied.")

    print("===== Using files: =====\n",
          args.filename1, "and", args.filename2, "...")

    # store synonyms into dictionary,
    # record synonym marker to replace other synonyms during preprocessing
    # dict_synonyms = map_file_to_dict(args.synfilename, 1)
    # if not dict_synonyms:
    #     synonym_marker = ""
    # else:
    #     synonym_marker = list(dict_synonyms.keys())[0]
    dict_synonyms = {}
    synonym_marker = ""
    # Pre-process files: replace synonyms, lowercase words and remove punctuations,
    # output as one line to another file
    filen1_processed_name = preprocess_file(args.filename1, dict_synonyms, synonym_marker)
    # filen2_processed_name = preprocess_file(args.filename2, dict_synonyms, synonym_marker)
    tuple_size = 1

    dict_arr = []

    translator = str.maketrans({key: None for key in string.punctuation})

    with open(args.filename2, 'r') as f_in:
        for line in f_in:
            if not line:
                continue
            line = line.translate(translator).strip().lower()
            wordList = line.split()
            while (len(wordList)-1 >= len(dict_arr)):
                dict_arr.append({})
                # print("len(wordList) ", len(wordList), " vs. len(dict_arr): ", len(dict_arr))
            dict = dict_arr[len(wordList)-1]
            dict[line] = 1

    # print("=====", dict_arr[1])
    f_out = open(filen1_processed_name+"_out", 'w')
    for i in range(len(dict_arr)-1, -1,-1):
        tuple_size = i+1
        dict_target_words = dict_arr[i]


        with open(filen1_processed_name, 'r') as f_1:
            word_gen_1 = words(f_1)
            tuple_window = []
            while True:
                # process chunk of file1
                # checking against dict2, output edited file
                try:
                    if len(tuple_window) == tuple_size:
                        word_tuple = " ".join(tuple_window)
                        if word_tuple in dict_target_words:
                            if tuple_size==2:
                                print ("[1"+word_tuple+"2] ")
                            f_out.write("[1"+word_tuple+"2] ")
                        else:
                            f_out.write(word_tuple+" ")
                        tuple_window.pop(0)
                    tuple_window.append(next(word_gen_1))
                except StopIteration:
                    break

    f_out.close()



    # overlap_tuple_ct, file1_tuple_ct = count_overlapped_tuples(filen2_processed_name,
    #                                      filen1_processed_name, args.tuple_size, args.dict_max_len)

    # print("=> Result:", overlap_tuple_ct/file1_tuple_ct*100,"% of tuples in", args.filename1,
    #       "which appear in", args.filename2)


if __name__ == '__main__':
    main()
