import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import VotingClassifier, HistGradientBoostingClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

print("Loading data...")
# Load the data from the CSV file
data = pd.read_csv("data/proteinstats.csv")
print("Loaded data")

print("Generating training and test data...")
# Features
X = data.iloc[:, 1:]

# Labels
y = data["ENZYME_TYPE"]


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Generated training and test data")

print("Building and training the model...")
# Create and train the Random Forest classifier
clf4 = DecisionTreeClassifier()
clf7 = HistGradientBoostingClassifier()
clf8 = ExtraTreesClassifier()
classifier = VotingClassifier([('dt', clf4), ('hgb', clf7), ('etc', clf8)], voting='hard')

model = classifier.fit(X, y)  # Uncomment this line if clf needs training


# Make predictions on the test set
y_pred = model.predict(X)

# Evaluate the accuracy of the model
accuracy = accuracy_score(y, y_pred)
print(f"Accuracy: {accuracy}")

from joblib import dump

print("Saving model...")
dump(model, "./resistML.joblib")
print("Saved")

print("All done")
