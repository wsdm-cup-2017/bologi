import numpy as np 
import pandas as pd 
from pandas import DataFrame
from pandas import Series
from NameSentenceGenerator import Read_name_from_profession
from NameSentenceGenerator import Read_occupation_from_profession
from NameSentenceGenerator import Read_NameJob_pair_from_profession
from NameSentenceGenerator import Read_nation_from_nationality
from NameSentenceGenerator import Read_NameNation_pair_from_nationality
import json
#Author: Zhuang,Yiwei
#Date created:   2016.Oct.05

#Label the training data in a DataFrame  row index is name column index is occupation
#input: path of file
#output: a table DataFrame with names * jobs
# eg .if A has job B and C, then table.loc[A][B] = 1 table.loc[A][C] = 1 other cells in A is 0
def Label_TrainingData_Occupation(path):
	train_names 			= Read_name_from_profession(path)
	job_names				= Read_occupation_from_profession(path)
	people_job_pairs 		= Read_NameJob_pair_from_profession(path)
	job_len 				= len(job_names)
	name_len				= len(train_names)
	inital_val       		= np.zeros((name_len, job_len))
	Label_results 			= pd.DataFrame(data = inital_val , index = train_names , columns = job_names)

	for index, row in people_job_pairs.iterrows():
		people_name = people_job_pairs.get_value(index,'name')
		people_job  = people_job_pairs.get_value(index,'occupation')
		Label_results.set_value(people_name, people_job,1) 

	return Label_results


def write_labeled_data_to_file_occupation():
	result = Label_TrainingData_Occupation("/Users/Zhuangyiwei/Desktop/triple-scoring/profession.train")
	result.to_csv("LabelTrainingData_File_Occupation", sep = '\t', encoding = 'utf-8')



def Label_TrainingData_Nation(path):
	train_names 			= Read_name_from_profession(path)
	nation_names			= Read_nation_from_nationality(path)
	people_nation_pairs 	= Read_NameNation_pair_from_nationality(path)
	nation_len 				= len(nation_names)
	name_len				= len(train_names)
	inital_val       		= np.zeros((name_len, nation_len))
	Label_results 			= pd.DataFrame(data = inital_val , index = train_names , columns = nation_names)

	for index,row in people_nation_pairs.iterrows():
		people_name = people_nation_pairs.get_value(index,'name')
		people_nation  = people_nation_pairs.get_value(index,'nation')
		Label_results.set_value(people_name, people_nation,1) 

	return Label_results


def write_labeled_data_to_file_Nation():
	result = Label_TrainingData_Nation("/Users/Zhuangyiwei/Desktop/triple-scoring/nationality.train")
	result.to_csv("LabelTrainingData_File_Nation", sep = '\t', encoding = 'utf-8')

write_labeled_data_to_file_occupation()
write_labeled_data_to_file_Nation()
#still have some minor error regard to encoding of file





