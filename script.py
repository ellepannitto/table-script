import pathlib
import conllu
import sys

if len(sys.argv) < 3:
	print("Please run `python3 script.py [SOURCE_DIR] [DEST_DIR]`")
	sys.exit(1)

source_path = sys.argv[1]
destination_path = sys.argv[2]

spoken_only = ["UD_Abaza-ATB",
	"UD_Beja-Autogramm",
	"UD_Cantonese-HK",
	"UD_Chukchi-HSE",
	"UD_English-ESLSpok",
	"UD_French-ParisStories",
	"UD_French-Rhapsodie",
	"UD_Frisian_Dutch-Fame",
	"UD_Gheg-GPS",
	"UD_Hausa-NorthernAutogramm",
	"UD_Hausa-SouthernAutogramm",
	"UD_Hebrew-IAHLTknesset",
	"UD_Khunsari-AHA",
	"UD_Komi_Zyrian-IKDP",
	"UD_Naija-NSC",
	"UD_Nayini-AHA",
	"UD_Northwest_Gbaya-Autogramm",
	"UD_NynorskLIA",
	"UD_Pesh-ChibErgIS",
	"UD_Slovenian-SST",
	"UD_Soi-AHA",
	"UD_Spanish-COSER",
	"UD_Turkish_German-SAGT",
	"UD_Zaar-Autogramm"]

conditions = {"UD_English-GENTLE": (lambda meta: "meta::speakerCount" in meta,
									lambda meta: int(meta["meta::speakerCount"])>0),
			"UD_English-GUM": (lambda meta: "meta::genre" in meta,
								lambda meta: meta["meta::genre"] in ["conversation", "interview", "speech"]),
			"UD_Greek-GDT": (lambda meta: "sent_id" in meta,
							lambda meta: "ep-session" in meta["sent_id"]),
			"UD_Highland_Puebla_Nahuatl-ITML": (lambda meta: "sent_id" in meta,
												lambda meta: ".eaf" in meta["sent_id"]),
			"UD_Scottish_Gaelic-ARCOSG": (lambda meta: "sent_id" in meta,
										lambda meta: meta["sent_id"].startswith("c") or \
													meta["sent_id"].startswith("n") or \
													meta["sent_id"].startswith("p") or \
													meta["sent_id"].startswith("x")),
			"UD_Western_Sierra_Puebla_Nahuatl-ITML": (lambda meta: "label" in meta,
													lambda meta: "frog-story" in meta["label"])
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