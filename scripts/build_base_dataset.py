import gzip
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio.Seq import Seq
import json
import pandas as pd


def hidrophobicity(protein_sequence):
    protein_sequence = protein_sequence.replace("*", "").replace("X","").replace("Z", "").replace("B","")
    hydrophobicity_score = ProteinAnalysis(protein_sequence).gravy()
    return hydrophobicity_score


def isoelectric_pt(protein_sequence):
    protein_sequence = protein_sequence.replace("*", "").replace("X","").replace("Z", "").replace("B","")
    isoelectric = ProteinAnalysis(protein_sequence).isoelectric_point()
    return isoelectric


def aromatic(protein_sequence):
    protein_sequence = protein_sequence.replace("*", "").replace("X","").replace("Z", "").replace("B","")
    arom = ProteinAnalysis(protein_sequence).aromaticity()
    return arom


def instable(protein_sequence):
    protein_sequence = protein_sequence.replace("*", "").replace("X","").replace("Z", "").replace("B","")
    inst = ProteinAnalysis(protein_sequence).instability_index()
    return inst


def weight(protein_sequence):
    protein_sequence = protein_sequence.replace("*", "").replace("X","").replace("Z", "").replace("B","")
    wgt = ProteinAnalysis(protein_sequence).molecular_weight()
    return wgt


def sec_struct(protein_sequence):
    protein_sequence = protein_sequence.replace("*", "").replace("X","").replace("Z", "").replace("B","")
    second_struct = ProteinAnalysis(protein_sequence).secondary_structure_fraction()
    return ",".join([str(s) for s in second_struct])


def mol_ext(protein_sequence):
    protein_sequence = protein_sequence.replace("*", "").replace("X","").replace("Z", "").replace("B","")
    molar_ext = ProteinAnalysis(protein_sequence).molar_extinction_coefficient()
    return ",".join([str(s) for s in molar_ext])


def load_data(infile):
    """Load data from infile if it is in fasta format (after having unzipped it, if it is zipped)"""
    if infile.endswith(".gz"):  # If file is gzipped, unzip it
        y = gzip.open(infile, "rt", encoding="latin-1")
        # Read file as fasta if it is fasta
        if (
            infile.endswith(".fasta.gz")
            or infile.endswith(".fna.gz")
            or infile.endswith(".fas.gz")
            or infile.endswith(".fa.gz")
        ):
            records = SeqIO.parse(y, "fasta")
            sequences = {}
            for record in records:
                sequences.update({str(record.id): str(record.seq)})
            y.close()
            return sequences
        else:
            y.close()
            raise ValueError("File is the wrong format")
    # Read file directly as fasta if it is a not zipped fasta: handle also more uncommon extensions :-)
    elif (
        infile.endswith(".fasta")
        or infile.endswith(".fna")
        or infile.endswith(".fas")
        or infile.endswith(".fa")
    ):
        with open(infile, "r") as y:
            records = SeqIO.parse(y, "fasta")
            sequences = {}
            for record in records:
                sequences.update({str(record.id): str(record.seq)})
            y.close()
            return sequences
    else:
        raise ValueError("File is the wrong format")

def read_multiplefasta(multiple_fasta):
    genomes = []
    with open(multiple_fasta) as file:
        single_genomes = []
        counter = 0
        for line in file:
            if ">" not in line:
                seq = []
                for char in line:
                    if char != '\n':
                        seq.append(char)
                dnar = ""
                dnadef = dnar.join(seq)
                single_genomes.append(dnadef)
                counter += 1
                comp_gen = ""
                complete_genome = comp_gen.join(single_genomes)
            if ">" in line and counter == 0:
                continue
            if ">" in line and counter != 0:
                genomes.append(complete_genome) 
                single_genomes = []
        genomes.append(complete_genome)           
    
    return genomes


def check_if_in_header(classesdict: dict, header: str) -> str:
    for key in list(classesdict.keys()):
        if header.split("|")[1] in classesdict[key]:
            return key
    return ""

def map_classes_to_aro_indices(aro_indices: str, classes: list):
    tsv = pd.read_csv(aro_indices, sep="\t")
    classesdict = {cla: [] for cla in classes}
    accessions = list(tsv["Protein Accession"])
    classesexp = list(tsv["AMR Gene Family"])
    for cla in classes:
        for i in range(len(classesexp)):
            if cla == classesexp[i]:
                classesdict[cla].append(accessions[i])
    return classesdict

fln = pd.read_csv("data/most_common_classes.csv")
classes = list(fln["CLASS"])
print(classes)
aro_indices = "data/aro_categories_index.tsv"
classesdict = map_classes_to_aro_indices(aro_indices, classes)
fasta = open("data/protein_fasta_protein_homolog_model.fasta", "r")
fastalines = fasta.readlines()
fasta.close()
headers = [line.replace("\n","") for line in fastalines if line.startswith(">")]
seqs = read_multiplefasta("data/protein_fasta_protein_homolog_model.fasta")
csv = open("data/proteinstats.csv", "w")
csv.write("ENZYME_TYPE,HIDROPHOBICITY,ISOELECTRIC,AROMATIC,INSTABLE,MW,HELIX,TURN,SHEET,MOL_EXT_RED,MOL_EXT_OX\n")
jsonf = open("data/resistance.jsonl", "w")
counter = 0
for j in range(len(headers)):
    counter+=1
    cl = check_if_in_header(classesdict, headers[j])
    if cl != "":
        jsonobj = json.dumps({"text": seqs[j], "label": cl})
        jsonf.write(jsonobj+"\n")
        hydr = hidrophobicity(seqs[j])
        isl = isoelectric_pt(seqs[j])
        arm = aromatic(seqs[j])
        inst = instable(seqs[j])
        mw = weight(seqs[j])
        se_st = sec_struct(seqs[j])
        me = mol_ext(seqs[j])
        csv.write(
            f'{cl.replace(",",":")},{hydr},{isl},{arm},{inst},{mw},{se_st},{me}\n'
        )
    if counter % 500 == 0:
        print(f"Processed {counter} reads")
jsonf.close()
csv.close()