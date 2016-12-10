
if [ "$#" -ne 3 ]
	then
		echo "Usage: source test.sh [#tuples to test] [profession/nationality] [vm/dev]"
		return
fi
if [ "$3" = "vm" ]; then
	echo "Using $1 lines/tuples for testing $2 (profession/nationality)"
	head -n$1 /media/training-datasets/triple-scoring/wsdmcup17-triple-scoring-training-dataset-2016-09-16/$2.train > \
	     ../data/input_tuple/$2.test.cjy
	head -n$1 /media/training-datasets/triple-scoring/wsdmcup17-triple-scoring-training-dataset-2016-09-16/$2.train > \
	     ../data/raw_data/$2.train.sm
	python2 cjy_main.py -i ../data/input_tuple/$2.test.cjy -o ../data/output_data && python3 evaluator.py --run ../data/output_data/$2.test.cjy --truth ../data/raw_data/$2.train.sm --output ../data/output_data/tmp
	return
fi

if [ "$3" = "dev" ]; then
	echo "Using $1 lines/tuples for testing $2 (profession/nationality)"
	head -n$1 ../data/raw_data/$2.train.true > ../data/raw_data/$2.train.cjy
	# head -n$1 ../data/raw_data/$2.train.true > ../data/input_tuple/$2.test.cjy
	cp ../data/raw_data/$2.train.cjy ../data/input_tuple/$2.test.cjy
	python2 cjy_main.py -i ../data/input_tuple/$2.test.cjy -o ../data/output_data && \
	python3 evaluator.py --run ../data/output_data/$2.test.cjy --truth ../data/raw_data/$2.train.cjy \
	                     --output ../data/output_data/tmp
	return
fi
