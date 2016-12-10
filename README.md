# bologi
The Bologi Triple Scorer 2017

# resrc
- on vm, data already located at
	bologi@tira-ubuntu:/media/training-datasets/triple-scoring/wsdmcup17-triple-scoring-training-dataset-2016-09-16$ ls
	nationalities  nationality.kb  nationality.train  persons  profession.kb  professions  profession.train  triple-scoring.zip  wiki-sentences

- download datas as zip:
	'curl http://broccoli.cs.uni-freiburg.de/wsdm-cup-2017/triple-scoring.zip -o <output path such as ./data/war_data/wiki-sentences>'

- for testing, simply run the script to run and eval:
  run 'source ./src/test.sh [#tuples to test] [profession/nationality] [vm/dev]'

# usage:
0. data
- make sure you have wiki file downloaded, placed under ./data/raw_data
- restore'data/intermediate_data/' as following:
		name2sentenc   nationality_words_table.txt      profession_words_table.txt

1. on first use, create name2sentence dictionaries:
'python2 ./src/cjy_dict_generator.py'
* once have the dictionary, no need to generate it anymore in later uses.

2. run main script to predict tuple
such as 'python2 cjy_main.py -i ../data/input_tuple/profession.test.cjy -o ../data/output_data'

3. inspect output triples
'cd ./data/output_data'


# encoding problem w/ unicode
- stored key in semi-unicode like string:
	Vilen K\xc3\xbcnnapu
- vs. actual string read from tuple:
	Vilen KÃ¼nnapu
- >>> "Vilen KÃ¼nnapu".decode("utf-8")
u'Vilen K\xc3\xbcnnapu'

key is 'Vilen K\xc3\x83\xc2\xbcnnapu'

# wiki data path on vm
"/media/training-datasets/triple-scoring/wsdmcup17-triple-scoring-training-dataset-2016-09-16/wiki-sentences"

## word2vec
vectors-enwikitext_vivek200.zip