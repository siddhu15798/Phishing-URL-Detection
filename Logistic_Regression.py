import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from warnings import simplefilter
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

simplefilter(action='ignore', category=FutureWarning)

# penalty = ['l1', 'l2']
# C = np.logspace(0, 4, 10)
# hyperparameters = dict(C=C, penalty=penalty)

URLS = pd.read_csv("data.csv")

URLS = URLS.drop(URLS.columns[[0]], axis=1)

URLS = URLS.sample(frac=1).reset_index(drop=True)

URLS_Without_Labels = URLS.drop('Result', axis=1)

Labels = URLS['Result']

Training_Data, Testing_Data = train_test_split(URLS_Without_Labels, test_size = 0.25, random_state = 150)

Training_Labels, Testing_Labels = train_test_split(Labels, test_size = 0.25, random_state = 150)

Logistic_Regression = LogisticRegression(random_state = 0)

Logistic_Regression.fit(Training_Data, Training_Labels)

Prediction_Labels = Logistic_Regression.predict(Testing_Data)

# clf = GridSearchCV(Logistic_Regression, hyperparameters, cv=5, verbose=0)
# best_model = clf.fit(Training_Data, Training_Labels)
# print('Best Penalty:', best_model.best_estimator_.get_params()['penalty'])
# print('Best C:', best_model.best_estimator_.get_params()['C'])
# prediction = best_model.predict(Testing_Data)
Confusion_Matrix = confusion_matrix(Testing_Labels, Prediction_Labels)

print("\nTraining Accuracy Score Obtained is: {0:.2f}%".format(accuracy_score(Training_Labels, Logistic_Regression.predict(Training_Data))*100.))
print("Testing Accuracy Score Obtained is: {0:.2f}%\n".format(accuracy_score(Testing_Labels, Prediction_Labels)*100.))
print("Classification Report: \n",classification_report(Testing_Labels, Prediction_Labels, target_names=['Phishing Websites', 'Normal Websites']))
print("Confusion Matrix: \n", Confusion_Matrix)
print("\n")

joblib.dump(Logistic_Regression, 'Logistic_Regression.pkl')