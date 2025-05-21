import pathlib
import conllu


conditions = {"UD_English-GENTLE": (lambda meta: "meta::speakerCount" in meta,
									lambda meta: int(meta["meta::speakerCount"])>0 )
			}


for treebank in conditions:
	print(f"Reading treebank {treebank}...")
	source_path = f"source/{treebank}/"
	destination_path = f"destination/{treebank}"
	pathlib.Path(destination_path).mkdir(parents=True, exist_ok=True)


	for filename in pathlib.Path(source_path).glob("*.conllu"):

		print(f"Reading file {filename}...")

		file_stem = filename.stem

		with open(filename) as fin, open(pathlib.Path(destination_path).joinpath(f"{file_stem}.selected.conllu"), "w") as fout:

			fun1, fun2 = conditions[treebank]
			sentences = conllu.parse_incr(fin)

			condition = False

			for sentence in sentences:
				metadata = sentence.metadata

				if fun1(metadata):
					if fun2(metadata):
						condition = True
						print(sentence.serialize().strip(), file=fout)
					else:
						condition = False
				else:
					if condition:
						print(sentence.serialize().strip(), file=fout)

		if condition:
			print(sentence.serialize().strip(), file=fout)