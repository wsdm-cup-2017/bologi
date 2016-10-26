from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import operator
from collections import OrderedDict
import pandas as pd
import json 
import re 


#Oct.22 2016 by Li Chen


prof_sentence_path= "./prof_sentence_dict.json"


#convert the prof_sentence_dict to a new dict, which has only one sentence (without names) for each profession.  
#input: dictionary of profession and sentences 
#output: dictionary without the names in [ ]
def Remove_all_names_in_dict_values(prof_sentence_path):
    
    with open(prof_sentence_path) as json_data:
        prof_sent_dict = json.load(json_data)
    
    new_dict={}
    keys = prof_sent_dict.keys() 
    for key  in keys:
        sentence_list  =  prof_sent_dict[key]
        sentence       =  ' '.join(sentence_list)  
        new_dict[key]  =  re.sub("\[.*?\]", "", sentence)
    return new_dict 


#Calculate the tfidf of sentences 
#input: a list of sentences 
#output: 50 words of first sentence with the hightes tfidf value
def Tfidf_for_sentences(sentences):
    vectorizer = TfidfVectorizer(min_df=1, use_idf=True,  sublinear_tf = True)
    X = vectorizer.fit_transform(sentences).toarray() 
    features= vectorizer.get_feature_names()
    tfidf = dict(zip(features, X[0]))
    tfidf_sorted= OrderedDict(sorted(tfidf.items(), key=operator.itemgetter(1), reverse=True))
    return tfidf_sorted.keys()[:50]        # print out 50 words for reference 


# build corpus with short sentences for specificed profession 
#inoput: path and target profession 
#output: corpus 
def Build_corpus(prof_sentence_path, target_prof):
    corpus=[] 
    with open(prof_sentence_path) as json_data:
        prof_sent_dict = json.load(json_data)
        
    prof_list = prof_sent_dict.keys()
    for prof in prof_list[:20]:  # to reduce the running time, only select 20 other professions
        if prof != target_prof:
            corpus  += prof_sent_dict[prof]
    return corpus 


#Find words 
#input: path 
#output: words 

def Find_specific_word_each_occupation(prof_sentence_path):
    result={}
    new_dict = Remove_all_names_in_dict_values(prof_sentence_path)
    
    prof_list = new_dict.keys() 
    print prof_list 
    
    for prof in prof_list:
        print prof 
        corpus          = Build_corpus(prof_sentence_path, prof) 
        target_sentence = new_dict[prof]
        target_corpus   = [target_sentence] + corpus 
        tfidf_words     = Tfidf_for_sentences(target_corpus)
        result[prof]    = tfidf_words 
    
    return result


def read_data_write_file(prof_sentence_path):
    prof_words_dict = Find_specific_word_each_occupation(prof_sentence_path)
    fo = open("prof_words_table.txt", 'w')
    json.dump(job_words_dict, fo)
