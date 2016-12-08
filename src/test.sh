echo "Using $1 lines/tuples for testing $2 (profession/nationality)"
head -n$1 ../data/raw_data/$2.train.true > ../data/input_tuple/$2.test.cjy
head -n$1 ../data/raw_data/$2.train.true > ../data/raw_data/$2.train.sm
python2 cjy_main.py -i ../data/input_tuple/$2.test.cjy -o ../data/output_data && python3 evaluator.py --run ../data/output_data/$2.test.cjy --truth ../data/raw_data/$2.train.sm --output ../data/output_data/tmp

