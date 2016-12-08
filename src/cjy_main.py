#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import argparse
import sys
import math
import numpy as np
import pandas as pd
import numpy as np
import pandas as pd
from cjy_predict import predice_train_file_job_using_dict
from cjy_predict import predice_train_file_nation_using_dict
# from Predict import Predice_train_file_nation
# from Predict import write_test_sentences_to_file


if __name__=='__main__':
    # Parse command line arguments.
    parser = argparse.ArgumentParser()
    r = parser.add_argument_group("required arguments")
    r.add_argument("-i", help="input file to be predicted",
                   action='append', nargs=1, metavar=('inputfile'), required=True)
    r.add_argument("-o", help="predicted results.", required=True)
    args = vars(parser.parse_args())
    infiles = args["i"]
    outpath = args["o"]
    for inf in infiles:
        path = inf[0]
        names=path.split('/')
        type_name = names[-1].split('.')[0]
        if(outpath[-1]=='/'):
            outpath=outpath[:len(outpath)-1]
        opath  = outpath +'/' + names[-1]
#        write_test_sentences_to_file(path)
        if type_name=="profession":
            print "predict profession"
            predice_train_file_job_using_dict(path, opath)
        else:
        # if type_name== "nationality":
            print "predict nationality"
            predice_train_file_nation_using_dict(path, opath)

