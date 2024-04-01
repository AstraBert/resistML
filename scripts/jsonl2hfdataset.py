import json
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict, ClassLabel, Value

def create_dataset(dictionary):
    dataset = Dataset.from_dict(dictionary)
    dataset = dataset.cast_column("text", Value("string"))
    dataset = dataset.cast_column("label", ClassLabel(num_classes=12, names=['PDC beta-lactamase', 'CTX-M beta-lactamase', 'SHV beta-lactamase', 'CMY beta-lactamase', 'resistance-nodulation-cell division (RND) antibiotic efflux pump', 'major facilitator superfamily (MFS) antibiotic efflux pump', 'quinolone resistance protein (qnr)', 'IMP beta-lactamase', 'KPC beta-lactamase', 'ACT beta-lactamase', 'MCR phosphoethanolamine transferase', 'VIM beta-lactamase']))
    return dataset

def labels2classes(labels: list, classes: list):
    labels2id = {labels[i]: i for i in range(len(labels))}
    id2lables = {k: labels2id[k] for k in list(labels2id.keys())}
    new_classes = []
    for i in classes:
        new_classes.append(labels2id[i])
    return new_classes, id2lables



def df_from_listofdicts(listofdifcs: list):
    refdict = listofdifcs[0]
    keys = list(refdict.keys())
    newdict = {
        key: [listofdifcs[i][key] for i in range(len(listofdifcs))] for key in keys
    }
    return newdict


fln = open("data/resistance_reduced.jsonl")
ds = []
lines = fln.readlines()
fln.close()
for line in lines:
    ds.append(json.loads(line))
ds_train, ds_test = train_test_split(ds, test_size=0.2, random_state=42)
ds_train = df_from_listofdicts(ds_train)
ds_train["label"], id2label = labels2classes(labels=['PDC beta-lactamase', 'CTX-M beta-lactamase', 'SHV beta-lactamase', 'CMY beta-lactamase', 'resistance-nodulation-cell division (RND) antibiotic efflux pump', 'major facilitator superfamily (MFS) antibiotic efflux pump', 'quinolone resistance protein (qnr)', 'IMP beta-lactamase', 'KPC beta-lactamase', 'ACT beta-lactamase', 'MCR phosphoethanolamine transferase', 'VIM beta-lactamase'], classes=ds_train["label"])
ds_test = df_from_listofdicts(ds_test)
ds_test["label"], id2label = labels2classes(labels=['PDC beta-lactamase', 'CTX-M beta-lactamase', 'SHV beta-lactamase', 'CMY beta-lactamase', 'resistance-nodulation-cell division (RND) antibiotic efflux pump', 'major facilitator superfamily (MFS) antibiotic efflux pump', 'quinolone resistance protein (qnr)', 'IMP beta-lactamase', 'KPC beta-lactamase', 'ACT beta-lactamase', 'MCR phosphoethanolamine transferase', 'VIM beta-lactamase'], classes=ds_test["label"])
settrain = set(list(ds_train["label"]))
settest = set(list(ds_test["label"]))
if settrain==settest:
    print("Yesss!!!", settrain, settest)
    ds_train = create_dataset(ds_train)
    ds_test = create_dataset(ds_test)
    final_ds = {"train": ds_train, "test": ds_test}
    finale = DatasetDict(final_ds)
    print(finale["train"].features)
    print(finale["train"][0])
    print(finale["test"][0])
    with open('id2label.json', 'w') as fp:
        json.dump(id2label, fp)
    fp.close()
    print(finale)
    finale.push_to_hub("as-cle-bert/AMR-Gene-Families")
else:
    print("Nope! Quitting...")