import json
from statistics import mean, stdev

def df_from_listofdicts(listofdifcs: list):
    refdict = listofdifcs[0]
    keys = list(refdict.keys())
    newdict = {
        key: [listofdifcs[i][key] for i in range(len(listofdifcs))] for key in keys
    }
    return newdict

jsonf = open("data/resistance.jsonl", "r")
dictionnaires = []
for line in jsonf:
    dictionnaires.append(json.loads(line))
jsonf.close()
df = df_from_listofdicts(dictionnaires)
classes = list(df["label"])
labeledsequences = {label: [] for label in classes}
for label in list(labeledsequences.keys()):
    for i in dictionnaires:
        if i["label"] == label:
            labeledsequences[label].append(len(i["text"]))
labeledsequences = {label: (mean(labeledsequences[label]), stdev(labeledsequences[label]))for label in list(labeledsequences.keys())}
print(f"{len(set(classes))} classes, total number of transcripts: {len(classes)}; classes are: {','.join(list(set(classes)))}")
classcount = {classific: classes.count(classific) for classific in list(set(classes))}
classcountfromzero = {classific: 0 for classific in list(set(classes))}
prots = list(df["text"])
lengths = [len(prot) for prot in prots]
print(f"Longest sequence is {max(lengths)} aa")
jsonfl = open("data/resistance_reduced.jsonl", "w")
for i in range(len(prots)):
    if classcount[classes[i]] > 200:
        if classcountfromzero[classes[i]] < 200 and labeledsequences[classes[i]][0]-3*labeledsequences[classes[i]][1] <= len(prots[i]) <= labeledsequences[classes[i]][0]+3*labeledsequences[classes[i]][1]:
            jsonobj = json.dumps({"label": classes[i], "text": " ".join([char for char in prots[i]])})
            jsonfl.write(jsonobj+"\n")
            classcountfromzero[classes[i]]+=1
        else:
            continue
    else:
        jsonobj = json.dumps({"label": classes[i], "text": " ".join([char for char in prots[i]])})
        jsonfl.write(jsonobj+"\n")
jsonfl.close()