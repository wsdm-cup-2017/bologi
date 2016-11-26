import pandas as pd
import json 
from NameSentenceGenerator import Find_related_sentence_from_wiki


name_sentence = "/Users/Zhuangyiwei/Desktop/triple-scoring/wiki-train.json"
Labeled_profession_path  = "/Users/Zhuangyiwei/Desktop/412project/LabelTrainingData_File_Occupation"

def find_sentence_with_profession( Labeled_profession_path, name_sentence):
    prof=  pd.read_csv(Labeled_profession_path,sep='\t' )

    with open(name_sentence) as json_data:
        name_sent = json.load(json_data)
    
    prof_type= prof.keys()
    prof_type= prof_type[1:]
  
    sent_dict ={}
    
    for pn in prof_type:
        
        data=prof[prof[pn]==1]
        people=data['name'].values
        
        for who in people: 
            if who in name_sent.keys():
                if not pn in sent_dict.keys():
                    sent_dict[pn] = name_sent[who]
                else:
                    sent_dict[pn] += name_sent[who]
            
    return sent_dict 
    
def write_sentences_to_file():
	fo = open("prof_sentence_dict.txt", 'w')
	result = find_sentence_with_profession(Labeled_profession_path, name_sentence)
	json.dump(result, fo)
    
write_sentences_to_file()