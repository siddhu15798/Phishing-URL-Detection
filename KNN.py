import joblib
import pandas as pd
import matplotlib.pyplot as plt
from warnings import simplefilter
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report

simplefilter(action='ignore', category=FutureWarning)

URLS = pd.read_csv("data.csv")

URLS = URLS.drop(URLS.columns[[0]], axis=1)

URLS = URLS.sample(frac=1).reset_index(drop=True)

URLS_Without_Labels = URLS.drop('Result', axis=1)

Labels = URLS['Result']

Training_Data, Testing_Data = train_test_split(URLS_Without_Labels, test_size=0.25, random_state=150)

Training_Labels, Testing_Labels = train_test_split(Labels, test_size=0.25, random_state=150)

KNN = KNeighborsClassifier(n_neighbors=5)

KNN.fit(Training_Data, Training_Labels) 

Prediction_Labels = KNN.predict(Testing_Data)

Confusion_Matrix = confusion_matrix(Testing_Labels, Prediction_Labels)

print("\nTraining Accuracy Score Obtained is: {0:.2f}%".format(accuracy_score(Training_Labels, KNN.predict(Training_Data))*100.))
print("Testing Accuracy Score Obtained is: {0:.2f}%\n".format(accuracy_score(Testing_Labels, Prediction_Labels)*100.))
print("Classification Report: \n",classification_report(Testing_Labels, Prediction_Labels, target_names=['Phishing Websites', 'Normal Websites']))
print("Confusion Matrix: \n", Confusion_Matrix)
print("\n")

joblib.dump(KNN, 'KNN.pkl')