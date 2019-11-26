import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from warnings import simplefilter
from sklearn.naive_bayes import GaussianNB, BernoulliNB
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

# Gaussian_NB = GaussianNB()

Bernoulli_NB = BernoulliNB()

# Prediction_Labels = GaussianNB.fit(Training_Data, Training_Labels).predict(Testing_Data)

Prediction_Labels_1 = Bernoulli_NB.fit(Training_Data, Training_Labels).predict(Testing_Data)

# Confusion_Matrix = confusion_matrix(Testing_Labels, Prediction_Labels)

Confusion_Matrix_1 = confusion_matrix(Testing_Labels, Prediction_Labels_1)

# print("\nTraining Accuracy Score Obtained is: {0:.2f}%".format(accuracy_score(Training_Labels, gb.predict(Training_Data))*100.))
# print("Testing Accuracy Score Obtained is: {0:.2f}%\n".format(accuracy_score(Testing_Labels, Prediction_Labels)*100.))
# print("Classification Report: \n",classification_report(Testing_Labels, Prediction_Labels, target_names=['Phishing Websites', 'Normal Websites']))
# print("Confusion Matrix: \n", Confusion_Matrix)
# print("\n")

print("\nTraining Accuracy Score Obtained is: {0:.2f}%".format(accuracy_score(Training_Labels, Bernoulli_NB.predict(Training_Data))*100.))
print("Testing Accuracy Score Obtained is: {0:.2f}%\n".format(accuracy_score(Testing_Labels, Prediction_Labels_1)*100.))
print("Classification Report: \n",classification_report(Testing_Labels, Prediction_Labels_1, target_names=['Phishing Websites', 'Normal Websites']))
print("Confusion Matrix: \n", Confusion_Matrix_1)
print("\n")

joblib.dump(Bernoulli_NB, 'Naive_Bayes.pkl')