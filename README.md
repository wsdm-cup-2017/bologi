# bologi
The Bologi Triple Scorer 2017


- for testing, simply run the script to run and eval:
  run 'source ./src/test.sh [#tuples to test] [profession/nationality] [vm/dev]'

# usage:
0. prepare data
- make sure you have wiki file downloaded if you're not running on vm, placed under ./data/raw_data/

- your './data/intermediate_data/' should contain the following:
		name2sentence   nationality_words_table.txt      profession_words_table.txt
  (note name2sentence can be an empty folder, we will store the look-up dictionary here in next step)

1. on first use on your own machine, create name2sentence dictionaries:
   'python2 ./src/cjy_dict_generator.py'
* once have the dictionary, no need to generate it anymore in later uses.

2. run main script to predict tuple
   such as 'python2 cjy_main.py -i ../data/input_tuple/[input filename] -o ../data/output_data'

3. inspect output triples
   'cd ./data/output_data/[input filename]'

4. evaluate score using ./src/evaluator.py
	run 'python3 evaluator.py [-h] --run RUN --truth TRUTH --output OUTPUT'

5. A shell script is provided for quick run and eval on training triples
	run 'cd ./src && source test.sh [#tuples to test] [profession/nationality] [vm/dev] <0 for unstemmed table> <baseline score>", the later two parameters are optional for development purpose

# resrc
- on vm, data already located at
	bologi@tira-ubuntu:/media/training-datasets/triple-scoring/

- download datas as zip:
	'curl http://broccoli.cs.uni-freiburg.de/wsdm-cup-2017/triple-scoring.zip -o <output path such as ./data/war_data/wiki-sentences>'

- wiki data path on vm
"/media/training-datasets/triple-scoring/wsdmcup17-triple-scoring-training-dataset-2016-09-16/wiki-sentences"
