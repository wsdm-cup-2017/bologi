# bologi
The Bologi Triple Scorer

# resrc
- download datas as zip:
	'curl http://broccoli.cs.uni-freiburg.de/wsdm-cup-2017/triple-scoring.zip -o <output path such as ./data/war_data/wiki-sentences>'
- to create smaller sample wiki file for testing:
	'head -n[#lines desired] [filepath]'

# usage:
0. data
- make sure you have wiki file downloaded, placed under ./data/raw_data
- restore'data/intermediate_data/' as following:

name2sentence                   nameToSentences.json    td_labeled.json
name_sentence_dict.json         nation_words_table.txt
name_sentence_dict_nation.json  prof_words_table.txt

1. on first use, create name2sentence dictionaries:
'python2 ./src/cjy_dict_generator.py'
* once have the dictionary, no need to generate it anymore in later uses.

2. run main script to predict tuple
such as 'python2 cjy_main.py -i ../data/input_tuple/profession.test.cjy -o ../data/output_data'

3. inspect output triples
'cd ./data/output_data'

## word2vec
vectors-enwikitext_vivek200.zip

# encoding problem w/ unicode
- stored key in semi-unicode like string:
	Vilen K\xc3\xbcnnapu
- vs. actual string read from tuple:
	Vilen KÃ¼nnapu
- >>> "Vilen KÃ¼nnapu".decode("utf-8")
u'Vilen K\xc3\xbcnnapu'
