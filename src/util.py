import json

# output in json format
def output_as_json(obj, filename):
	fo = open(filename, "wb")
	json.dump(obj,fo, indent=4, sort_keys=True)
