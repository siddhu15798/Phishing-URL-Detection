import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from warnings import simplefilter
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

simplefilter(action='ignore', category=FutureWarning)

URLS = pd.read_csv("data.csv")

# Phishing_URLS = pd.read_csv("Phishing-URLS.csv")

# Legitimate_URLS = pd.read_csv("Legitimate-URLS.csv")

# URLS = Legitimate_URLS.append(Phishing_URLS)

URLS = URLS.drop(URLS.columns[[0]], axis=1)

URLS = URLS.sample(frac=1).reset_index(drop=True)

URLS_Without_Labels = URLS.drop('Result', axis=1)

Labels = URLS['Result']

Training_Data, Testing_Data = train_test_split(URLS_Without_Labels, test_size = 0.25, random_state = 110)

Training_Labels, Testing_Labels = train_test_split(Labels, test_size = 0.25, random_state = 110)

# parameters = [{'C':[1, 10, 100, 1000], 'gamma': [ 0.1, 0.2, 0.3, 0.5]}]

# grid_search = GridSearchCV(SVC(kernel='rbf' ),  parameters,cv =5, n_jobs= -1)

# grid_search.fit(Training_Data, Training_Labels)

# print("Best Accurancy =" +str( grid_search.best_score_))

# print("Best Parameters =" + str(grid_search.best_params_)) 

classifier = SVC(C = 10, kernel = 'rbf', gamma = 0.2 , random_state = 0)

classifier.fit(Training_Data, Training_Labels)

Prediction_Labels = classifier.predict(Testing_Data)

# Confusion_Matrix = confusion_matrix(Training_Labels, Prediction_Labels)

# print(Confusion_Matrix)

print("\nAccuracy Score obtained is : ",accuracy_score(Testing_Labels, Prediction_Labels))