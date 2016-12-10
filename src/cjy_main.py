#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import argparse
import sys
import math
import numpy as np
import pandas as pd
import numpy as np
import pandas as pd
from cjy_predict import predice_triple_using_dict

if __name__=='__main__':
    # Parse command line arguments.
    parser = argparse.ArgumentParser()
    r = parser.add_argument_group("required arguments")
    r.add_argument("-i", help="input file to be predicted",
                   action='append', nargs=1, metavar=('inputfile'), required=True)
    r.add_argument("-o", help="predicted results.", required=True)
    r.add_argument("--stem", type=int, choices=[0, 1],
                    help="choose which version of table to use")

    args = vars(parser.parse_args())
    if args['stem'] == 0:
        table_path_prefix = "../data/intermediate_data/old_"
    else:
        table_path_prefix = "../data/intermediate_data/"

    print "Use table w/ prefix: ", table_path_prefix
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
            print "=> predicting profession.."
            table_path = table_path_prefix + type_name +"_words_table.txt"
            predice_triple_using_dict(path, opath, table_path)
        elif type_name== "nationality":
            print "=> predicting nationality..."
            table_path = table_path_prefix + type_name +"_words_table.txt"
            predice_triple_using_dict(path, opath, table_path)

