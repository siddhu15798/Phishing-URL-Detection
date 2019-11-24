import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from warnings import simplefilter
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score

simplefilter(action='ignore', category=FutureWarning)

URLS = pd.read_csv("data.csv")

URLS = URLS.drop(URLS.columns[[0]], axis=1)

URLS = URLS.sample(frac=1).reset_index(drop=True)

URLS_Without_Labels = URLS.drop('Result', axis=1)

Labels = URLS['Result']

Training_Data, Testing_Data = train_test_split(URLS_Without_Labels, test_size=0.25, random_state=110)

Training_Labels, Testing_Labels = train_test_split(Labels, test_size=0.25, random_state=110)

gb = GaussianNB()

bn = BernoulliNB()

Prediction_Labels = gb.fit(Training_Data, Training_Labels).predict(Testing_Data)

Prediction_Labels_1 = bn.fit(Training_Data, Training_Labels).predict(Testing_Data)

print("\nAccuracy Score obtained is : ",accuracy_score(Testing_Labels, Prediction_Labels))

print("\nAccuracy Score obtained is : ",accuracy_score(Testing_Labels, Prediction_Labels_1))

Confusion_Matrix = confusion_matrix(Testing_Labels, Prediction_Labels)

Confusion_Matrix_1 = confusion_matrix(Testing_Labels, Prediction_Labels_1)

print(Confusion_Matrix)

print(Confusion_Matrix_1)
