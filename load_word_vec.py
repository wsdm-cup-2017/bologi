import pickle
import numpy
import pandas
import scipy
from scipy import spatial
from scipy import stats
from pandas import DataFrame
from pandas import Series

def load_obj(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def read_NameJob_pair_from_profession(path):
	s1 = pandas.read_csv(path, names = ['name' , 'occupation' , 'score'] , sep = '\t')
	s1['name'] = [x.replace(" ", "") for x in s1['name']]
	s1['name'] = [x.lower() for x in s1['name']]
	s1['occupation'] = [x.replace(" ", "") for x in s1['occupation']]
	s1['occupation'] = [x.lower() for x in s1['occupation']]
	pairs = DataFrame(s1)
	return pairs

def read_NameNation_pair_from_profession(path):
	s2 = pandas.read_csv(path, names = ['name' , 'nation' , 'score'] , sep = '\t')
	s2['name'] = [x.replace(" ", "") for x in s2['name']]
	s2['name'] = [x.lower() for x in s2['name']]
	s2['nation'] = [x.replace(" ", "") for x in s2['nation']]
	s2['nation'] = [x.lower() for x in s2['nation']]
	pairs = DataFrame(s2)
	return pairs

def main():
	name_vector = load_obj("name_vector.pkl")
	namefromNation_vector = load_obj("namefromNation_vector.pkl")
	profession_vector = load_obj("profession_vector.pkl")
	nation_vector = load_obj("nationality_vector.pkl")
	document = read_NameJob_pair_from_profession("profession.train")
	doc = read_NameNation_pair_from_profession("nationality.train")

	# find cosine distance between name and occupation
	for key in name_vector.keys():
		currentNameVector = name_vector.get(key)
		currentProfession = document.loc[document['name'] == key,['occupation']].values

		for x in currentProfession:
			if profession_vector.has_key(x[0]):
				print key, x[0], 1-spatial.distance.cosine(currentNameVector,profession_vector.get(x[0]))

	# find cosine distance between name and nationality
	for name in namefromNation_vector.keys():
		currentNameVector = namefromNation_vector.get(name)
		currentNation = doc.loc[document['name'] == name,['nation']].values

		for x in currentNation:
			print name, x[0], 1-spatial.distance.cosine(currentNameVector,nation_vector.get(x[0]))

if __name__ == '__main__':
main()