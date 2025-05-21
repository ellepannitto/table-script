from conllu import parse


with open("source/UD_English-GENTLE/en_gentle-ud-test.conllu") as fin:
	data = fin.read()
	sentences = parse(data)

	for sentence in sentences:
		print(sentence.TokenList)
		input()