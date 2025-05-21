import pathlib
import conllu
import sys

if len(sys.argv) < 3:
	print("Please run `python3 script.py [SOURCE_DIR] [DEST_DIR]`")
	sys.exit(1)

source_path = sys.argv[1]
destination_path = sys.argv[2]

spoken_only = ["UD_Northwest_Gbaya-Autogramm"]

conditions = {"UD_English-GENTLE": (lambda meta: "meta::speakerCount" in meta,
									lambda meta: int(meta["meta::speakerCount"])>0 )
			}

for treebank in spoken_only:
	print(f"Reading treebank {treebank}...")
	source_dir = f"{source_path}/{treebank}/"
	destination_dir = f"{destination_path}/{treebank}"
	try:
		pathlib.Path(destination_dir).symlink_to(source_dir)
	except FileExistsError as e:
		print("Symlink already in place")


for treebank in conditions:
	print(f"Reading treebank {treebank}...")
	source_dir = f"{source_path}/{treebank}/"
	destination_dir = f"{destination_path}/{treebank}"
	pathlib.Path(destination_path).mkdir(parents=True, exist_ok=True)


	for filename in pathlib.Path(source_path).glob("*.conllu"):

		print(f"Reading file {filename}...")

		file_stem = filename.stem
		with open(filename) as fin, \
			open(pathlib.Path(destination_path).joinpath(f"{file_stem}.selected.conllu"), "w") as fout:

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
				print("", file=fout)