import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.feature_selection import RFE
from warnings import simplefilter
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

simplefilter(action='ignore', category=FutureWarning)

URLS = pd.read_csv("data.csv")

URLS = URLS.drop(URLS.columns[[0]], axis=1)

URLS = URLS.sample(frac=1).reset_index(drop=True)

URLS_Without_Labels = URLS.drop('Result', axis=1)

Labels = URLS['Result']

Training_Data, Testing_Data = train_test_split(URLS_Without_Labels, test_size = 0.25, random_state = 150)

Training_Labels, Testing_Labels = train_test_split(Labels, test_size = 0.25, random_state = 150)

# parameters = [{'C':[1, 10, 100, 1000], 'gamma': [ 0.1, 0.2, 0.3, 0.5]}]
# grid_search = GridSearchCV(SVC(kernel='rbf' ),  parameters,cv =5, n_jobs= -1)
# grid_search.fit(Training_Data, Training_Labels)
# print("Best Accurancy =" +str( grid_search.best_score_))
# print("Best Parameters =" + str(grid_search.best_params_)) 

Model = SVC(C=10, gamma=0.2, random_state=0, kernel='linear')

Rfe = RFE(Model,15)

Fit = Rfe.fit(Training_Data, Training_Labels)

Prediction_Labels = Rfe.predict(Testing_Data)

Confusion_Matrix = confusion_matrix(Testing_Labels, Prediction_Labels)

New_Data = Rfe.transform(URLS_Without_Labels)

# print(label.shape)
df = pd.DataFrame(New_Data)
df.to_csv('RFEsvm.csv')

print("\nNumber Of Features: %d\n" % Fit.n_features_)
print("Selected Features: \n%s\n" % Fit.support_)
print("Feature Ranking: \n%s\n" % Fit.ranking_)
print("Training Accuracy Score Obtained is: {0:.2f}%".format(Fit.score(Training_Data, Training_Labels)*100.))
print("Testing Accuracy Score Obtained is: {0:.2f}%\n".format(accuracy_score(Testing_Labels, Prediction_Labels)*100.))
print("Classification Report: \n",classification_report(Testing_Labels, Prediction_Labels, target_names=['Phishing Websites', 'Normal Websites']))
print("Confusion Matrix: \n", Confusion_Matrix)
print('\n')

joblib.dump(Rfe, 'RFE_SVM.pkl')