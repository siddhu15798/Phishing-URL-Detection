import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from warnings import simplefilter
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score

simplefilter(action='ignore', category=FutureWarning)

URLS = pd.read_csv("data.csv")

# Phishing_URLS = pd.read_csv("Phishing-URLS.csv")

# Legitimate_URLS = pd.read_csv("Legitimate-URLS.csv")

# URLS = Legitimate_URLS.append(Phishing_URLS)

URLS = URLS.drop(URLS.columns[[0]], axis=1)

URLS = URLS.sample(frac=1).reset_index(drop=True)

URLS_Without_Labels = URLS.drop('Result', axis=1)

Labels = URLS['Result']

Training_Data, Testing_Data = train_test_split(URLS_Without_Labels, test_size = 0.25, random_state = 150)

Training_Labels, Testing_Labels = train_test_split(Labels, test_size = 0.25, random_state = 150)

classifier = LogisticRegression(random_state = 0)

classifier.fit(Training_Data, Training_Labels)

Prediction_Labels = classifier.predict(Testing_Data)

# Confusion_Matrix = confusion_matrix(Training_Labels, Prediction_Labels)

# print(Confusion_Matrix)

print("\nAccuracy Score obtained is : ",accuracy_score(Testing_Labels, Prediction_Labels),"\n")

