import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from warnings import simplefilter
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
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

Model = LogisticRegression()

Rfe = RFE(Model, 15)

Fit = Rfe.fit(Training_Data, Training_Labels)

print("Num Features: %d" % Fit.n_features_)
print("Selected Features: %s\n" % Fit.support_)
print("Feature Ranking: %s\n" % Fit.ranking_)
print("\n")
print(Fit.score(Training_Data, Training_Labels))
Prediction_Labels = Rfe.predict(Testing_Data)
New_Data = Rfe.transform(URLS_Without_Labels)

# print(label.shape)
df = pd.DataFrame(New_Data)
df.to_csv('data1.csv')

# print("\nAccuracy Score obtained is : ",accuracy_score(Testing_Labels, Prediction_Labels),"\n")
print('Accuracy score of the Logistic Regression classifier with default hyperparameter values {0:.2f}%'.format(accuracy_score(Testing_Labels, Prediction_Labels)*100.))
print('\n')
print('Classification report of the Logistic Regression classifier with default hyperparameter value')
print('\n')
print(classification_report(Testing_Labels, Prediction_Labels, target_names=['Phishing Websites', 'Normal Websites']))

Confusion_Matrix = confusion_matrix(Testing_Labels, Prediction_Labels)

print(Confusion_Matrix)

# classifier = LogisticRegression(random_state = 0)
# classifier.fit(Training_Data, Training_Labels)
# Prediction_Labels = classifier.predict(Testing_Data)

# clf = GridSearchCV(classifier, hyperparameters, cv=5, verbose=0)
# best_model = clf.fit(Training_Data, Training_Labels)
# print('Best Penalty:', best_model.best_estimator_.get_params()['penalty'])
# print('Best C:', best_model.best_estimator_.get_params()['C'])
# prediction = best_model.predict(Testing_Data)
# Confusion_Matrix = confusion_matrix(Training_Labels, Prediction_Labels)

# print("\nAccuracy Score obtained is : ",accuracy_score(Testing_Labels, Prediction_Labels),"\n")
# print('Accuracy score of the Logistic Regression classifier with default hyperparameter values {0:.2f}%'.format(accuracy_score(Testing_Labels, Prediction_Labels)*100.))
# print('\n')
# print('Classification report of the Logistic Regression classifier with default hyperparameter value')
# print('\n')
# print(classification_report(Testing_Labels, Prediction_Labels, target_names=['Phishing Websites', 'Normal Websites']))