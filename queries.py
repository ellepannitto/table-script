import sys
import csv
import grewpy as gp

gp.set_config("ud")

folder = sys.argv[1]

corpus_list = ["UD_English-GENTLE",
				"UD_Greek-GDT"]


# INTJ

request_str = "pattern { X[upos=INTJ] }"

request = gp.Request(request_str)

dict = {}

for corpus_id in corpus_list:
	dict[corpus_id] = {"CORPUS": corpus_id}
	corpus = gp.Corpus(f"{folder}/{corpus_id}")
	occurrences = corpus.count(request, clustering_keys=["X.lemma"])

	# print("OCC", occurrences)
	# input()
	if type(occurrences) == int:
		dict[corpus_id]["CLUSTERS"] = 0
	else:
		dict[corpus_id]["TOTAL COUNT"] = sum(occurrences.values())
		dict[corpus_id]["CLUSTERS"] = len(occurrences)
		dict[corpus_id]["VALUES"] = ", ".join(list(occurrences.keys()))

with open('intj.csv', 'w') as csvfile:
	fieldnames = ['CORPUS', 'TOTAL COUNT', "CLUSTERS", "VALUES"]
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval="_")

	writer.writeheader()
	for row in dict:
		writer.writerow(dict[row])


# PUNCT

request_str = "pattern { X[upos=PUNCT] }"

request = gp.Request(request_str)

dict = {}
all_punct = set()

for corpus_id in corpus_list:
	dict[corpus_id] = {"CORPUS": corpus_id}
	corpus = gp.Corpus(f"{folder}/{corpus_id}")
	occurrences = corpus.count(request, clustering_keys=["X.lemma"])

	if type(occurrences) == int:
		dict[corpus_id]["CLUSTERS"] = 0
	else:
		dict[corpus_id]["TOTAL COUNT"] = sum(occurrences.values())
		dict[corpus_id]["CLUSTERS"] = len(occurrences)

		for x in occurrences:
			dict[corpus_id][x] = occurrences[x]
			all_punct.add(x)
		# dict[corpus_id]["VALUES"] = ", ".join(list(occurrences.keys()))

with open('punct.csv', 'w') as csvfile:
	fieldnames = ['CORPUS', 'TOTAL COUNT', "CLUSTERS", "VALUES"] + list(all_punct)
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval="_")

	writer.writeheader()
	for row in dict:
		writer.writerow(dict[row])


# INTERRUPT
request_str = 'pattern { X[form=re".+[-~]"] }'

request = gp.Request(request_str)

dict = {}
all_punct = set()

for corpus_id in corpus_list:
	dict[corpus_id] = {"CORPUS": corpus_id}
	corpus = gp.Corpus(f"{folder}/{corpus_id}")
	occurrences = corpus.count(request, clustering_keys=["X.upos"])

	if type(occurrences) == int:
		dict[corpus_id]["CLUSTERS"] = 0
	else:
		dict[corpus_id]["TOTAL COUNT"] = sum(occurrences.values())
		dict[corpus_id]["CLUSTERS"] = len(occurrences)

		for x in occurrences:
			dict[corpus_id][x] = occurrences[x]
			all_punct.add(x)
		# dict[corpus_id]["VALUES"] = ", ".join(list(occurrences.keys()))

with open('interrupted.csv', 'w') as csvfile:
	fieldnames = ['CORPUS', 'TOTAL COUNT', "CLUSTERS", "VALUES"] + list(all_punct)
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval="_")

	writer.writeheader()
	for row in dict:
		writer.writerow(dict[row])




