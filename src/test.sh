# Dec. 2016, Jiayu Chen
if [ "$#" -le 2 ] #at least 3 params
	then
		echo "Usage: source test.sh [#tuples to test] [profession/nationality] [vm/dev] <0 for unstemmed table>"
		return
fi

declare -i stem=1
if [ "$#" -eq 4 ]; then
	stem=$4
fi

baselines=(0.6 1.2 1.8 2.5)
if [ "$#" -eq 5 ]; then
	baselines=("$5")
fi

for bl in "${baselines[@]}"
do
	echo -e "\nTesting baseline $bl\n"
	if [ "$3" = "vm" ]; then
		echo "Using $1 lines/tuples for testing $2 (profession/nationality), stem table? $stem"
		head -n$1 /media/training-datasets/triple-scoring/wsdmcup17-triple-scoring-training-dataset-2016-09-16/$2.train > \
		     ../data/input_tuple/$2.test.cjy
		head -n$1 /media/training-datasets/triple-scoring/wsdmcup17-triple-scoring-training-dataset-2016-09-16/$2.train > \
		     ../data/raw_data/$2.train.sm
		python2 -W ignore cjy_main.py -i ../data/input_tuple/$2.test.cjy -o ../data/output_data --stem $stem && \
		python3 evaluator.py --run ../data/output_data/$2.test.cjy --truth ../data/raw_data/$2.train.sm --output ../data/output_data/tmp

	elif [ "$3" = "dev" ]; then
		echo "Using $1 lines/tuples for testing $2 (profession/nationality), stem table? $stem"
		head -n$1 ../data/raw_data/$2.train.true > ../data/raw_data/$2.train.cjy
		# head -n$1 ../data/raw_data/$2.train.true > ../data/input_tuple/$2.test.cjy
		cp ../data/raw_data/$2.train.cjy ../data/input_tuple/$2.test.cjy


			python2 cjy_main.py -i ../data/input_tuple/$2.test.cjy -o ../data/output_data --stem $stem --baseline $bl && \
			python3 evaluator.py --run ../data/output_data/$2.test.cjy --truth ../data/raw_data/$2.train.cjy \
			                     --output ../data/output_data/tmp

	fi
done