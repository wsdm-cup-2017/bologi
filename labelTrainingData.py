# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series
from nameSentenceGenerator import read_name_from_profession
from nameSentenceGenerator import read_occupation_from_profession
from nameSentenceGenerator import read_NameJob_pair_from_profession
from util import output_as_json

# Author: Zhuang,Yiwei
# Date created:   2016.Oct.05

# Label the training data in a DataFrame  row index is name column index is occupation
# input: path of file
# output: a table DataFrame with names * jobs
# eg .if A has job B and C, then table.loc[A][B] = 1 table.loc[A][C] = 1 other cells in A is 0

def Label_TrainingData(path):
    train_names = read_name_from_profession(path)
    job_names = read_occupation_from_profession(path)
    people_job_pairs = read_NameJob_pair_from_profession(path)
    job_len = len(job_names)
    name_len = len(train_names)
    inital_val = np.zeros((name_len, job_len))
    Label_results = pd.DataFrame(data=inital_val, index=train_names,
                                 columns=job_names)

    # print(Label_results[:3][:3])
    for i in range(len(people_job_pairs)):
        # print(i)
        people_name = people_job_pairs.get_value(i, 'name')
        people_job = people_job_pairs.get_value(i, 'occupation')

        # print(people_name + "'s job is " + people_job)
        Label_results.set_value(people_name, people_job, 1)

    return Label_results

ret = Label_TrainingData('./data/raw_data/profession.train')
ret.to_json('./data/td_labeled.json', orient="index")

# still have some minor error regard to encoding of file

