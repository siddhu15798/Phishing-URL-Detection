import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from warnings import simplefilter
from sklearn.feature_selection import RFE
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report

simplefilter(action='ignore', category=FutureWarning)

URLS = pd.read_csv("data.csv")

URLS = URLS.drop(URLS.columns[[0]], axis=1)

URLS = URLS.sample(frac=1).reset_index(drop=True)

URLS_Without_Labels = URLS.drop('Result', axis=1)

Labels = URLS['Result']

Training_Data, Testing_Data = train_test_split(URLS_Without_Labels, test_size=0.25, random_state=110)

Training_Labels, Testing_Labels = train_test_split(Labels, test_size=0.25, random_state=110)

Model = RandomForestClassifier(random_state=0)

Rfe = RFE(Model, 15)

Fit = Rfe.fit(Training_Data, Training_Labels)

Prediction_Labels = Rfe.predict(Testing_Data)

Confusion_Matrix = confusion_matrix(Testing_Labels, Prediction_Labels)

New_Data = Rfe.transform(URLS_Without_Labels)

# print(label.shape)
df = pd.DataFrame(New_Data)
df.to_csv('RFErandfor.csv')

print("\nNumber Of Features: %d\n" % Fit.n_features_)
print("Selected Features: \n%s\n" % Fit.support_)
print("Feature Ranking: \n%s\n" % Fit.ranking_)
print("Training Accuracy Score Obtained is: {0:.2f}%".format(Fit.score(Training_Data, Training_Labels)*100.))
print("Testing Accuracy Score Obtained is: {0:.2f}%\n".format(accuracy_score(Testing_Labels, Prediction_Labels)*100.))
print("Classification Report: \n",classification_report(Testing_Labels, Prediction_Labels, target_names=['Phishing Websites', 'Normal Websites']))
print("Confusion Matrix: \n", Confusion_Matrix)
print('\n')

joblib.dump(Rfe, 'RFE_Random_Forest.pkl')
# Model_1 = RandomForestClassifier(n_estimators=700, random_state=0, max_features = 'log2', criterion = "gini", max_depth=100, max_leaf_nodes=20000)

# Rfe_1 = RFE(Model, 15)

# Fit_1 = Rfe_1.fit(Training_Data, Training_Labels)

# Prediction_Labels_1 = Rfe_1.predict(Testing_Data)

# Confusion_Matrix_1 = confusion_matrix(Testing_Labels, Prediction_Labels_1)

# print("Num Features: %d" % Fit_1.n_features_)
# print("Selected Features: %s\n" % Fit_1.support_)
# print("Feature Ranking: %s\n" % Fit_1.ranking_)
# print("\n")
# print(Fit_1.score(Training_Data, Training_Labels))
# print("\n")
# print('Accuracy score obtained is {0:.2f}%'.format(accuracy_score(Testing_Labels, Prediction_Labels_1)*100.))
# print("\n")
# print(Confusion_Matrix_1)

#print(URLS.columns)
#print(URLS.shape)
#print(URLS.head(5))
#print(len(Training_Data),len(Testing_Data))
#print(len(Training_Labels),len(Testing_Labels))
#print(Training_Labels.value_counts())
#print(Testing_Labels.value_counts())
#print(Confusion_Matrix_1)
# print("\nAccuracy Score obtained is : ",accuracy_score(Testing_Labels, Prediction_Labels))
#print(Confusion_Matrix_2)
# print("\nAccuracy Score obtained is : ",accuracy_score(Testing_Labels, Custom_Prediction_Labels))
