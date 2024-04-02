import joblib
from argparse import ArgumentParser
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

argparse = ArgumentParser()
argparse.add_argument(
    "-i",
    "--input_file",
    help="Path to the input file where all the raw reads are stored (must be fasta)",
    required=True,
)

argparse.add_argument(
    "-c",
    "--classifier",
    help="Path to the joblib file where the classifier is stored",
    required=True,
)

args = argparse.parse_args()


inf = args.input_file
clf = args.classifier


if __name__=="__main__":
    import json
    jsonf = open("id2label.json", "r")
    dictionnaire = json.load(jsonf)
    jsonf.close()
    classifier = joblib.load(clf)
    # Features
    data = pd.read_csv(inf)
    X = data.iloc[:, 1:]
    # Labels
    y_true = data["ENZYME_TYPE"]
    y_pred = classifier.predict(X)
    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score([dictionnaire[yt] for yt in y_true], [dictionnaire[yp] for yp in y_pred],  labels=list(set([dictionnaire[yt] for yt in y_true])), average='weighted')
    precision = precision_score([dictionnaire[yt] for yt in y_true], [dictionnaire[yp] for yp in y_pred],  labels=list(set([dictionnaire[yt] for yt in y_true])), average='weighted')
    recall = recall_score([dictionnaire[yt] for yt in y_true], [dictionnaire[yp] for yp in y_pred],  labels=list(set([dictionnaire[yt] for yt in y_true])), average='weighted')
    print(f"TEST ON {inf}\n-Accuracy: {accuracy:.4f}\n-f1 score: {f1:.4f}\n-Precision: {precision:.4f}\n-Recall: {recall:.4f}")

