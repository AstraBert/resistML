import json
import random as r
from build_base_dataset import *


def generate_random_test(familiesnumber: int, fileslist: list, sampledim: int, filesprotdict: dict, outcsv: str, outjson: str, testnumber: int): 
    randomfiles = []
    n = 0
    while n < familiesnumber:
        m = r.randint(0, len(fileslist)-1)
        if fileslist[m] not in randomfiles:
            randomfiles.append(fileslist[m])
            n+=1
            if n == familiesnumber:
                break
        else:
            continue
    finaltest = {rndfl: {} for rndfl in randomfiles}
    for i in randomfiles:
        seqsdict = load_data(i)
        headers = list(seqsdict.keys())
        to_test = {}
        j = 0
        while j < sampledim:
            m = r.randint(0, len(headers)-1)
            if headers[m] not in list(to_test.keys()):
                to_test.update({headers[m]: seqsdict[headers[m]]})
                j+=1
            else:
                continue
        finaltest[i] = to_test
    csv = open(outcsv, "w")
    csv.write("ENZYME_TYPE,HIDROPHOBICITY,ISOELECTRIC,AROMATIC,INSTABLE,MW,HELIX,TURN,SHEET,MOL_EXT_RED,MOL_EXT_OX\n")
    jsonf = open(outjson, "w")
    for f in list(finaltest.keys()):
        cl = filesprotdict[f]
        counter = 0
        headers = list(finaltest[f].keys())
        for j in headers:
            counter+=1
            if cl != "":
                jsonobj = json.dumps({"text": finaltest[f][j], "label": cl})
                jsonf.write(jsonobj+"\n")
                hydr = hidrophobicity(finaltest[f][j])
                isl = isoelectric_pt(finaltest[f][j])
                arm = aromatic(finaltest[f][j])
                inst = instable(finaltest[f][j])
                mw = weight(finaltest[f][j])
                se_st = sec_struct(finaltest[f][j])
                me = mol_ext(finaltest[f][j])
                csv.write(
                    f'{cl.replace(",",":")},{hydr},{isl},{arm},{inst},{mw},{se_st},{me}\n'
                )
    jsonf.close()
    csv.close()
    print(f'Metadata for test {testnumber}:\n-Protein statistics for resistML were saved in {outcsv}\n-Sequences and labels for resistBERT were saved in {outjson}\n-{sampledim} protein sequences were taken into account for {familiesnumber} families\n-Families taken into account were:\n{",".join([filesprotdict[p] for p in randomfiles])}')
    


import sys
f = open("id2label.json", "r")
to_download = json.load(f)
f.close()
protein_families = list(to_download.keys())
proteinfilesdict = {f"test/reads/{p.replace(' ', '_')}.fasta": p for p in protein_families}
filelist = list(proteinfilesdict.keys())
for i in range(0,6):
    familiesnumber = r.randint(2, 3)
    sampledim = r.randint(10,15)
    outcsv = f"test/testfiles/test_{i}.csv"
    outjson = f"test/testfiles/test_{i}.jsonl"
    generate_random_test(familiesnumber=familiesnumber, fileslist=filelist, filesprotdict=proteinfilesdict, outcsv=outcsv, outjson=outjson, testnumber=i, sampledim=sampledim)