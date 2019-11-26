import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report

URLS = pd.read_csv("data.csv")

URLS = URLS.drop(URLS.columns[[0]], axis=1)

URLS = URLS.sample(frac=1).reset_index(drop=True)

URLS_Without_Labels = URLS.drop('Result', axis=1)

Labels = URLS['Result']

Training_Data, Testing_Data = train_test_split(URLS_Without_Labels, test_size=0.3, random_state=110)

Training_Labels, Testing_Labels = train_test_split(Labels, test_size=0.3, random_state=110)

Model = DecisionTreeClassifier(random_state=0)

Rfe = RFE(Model, 15)

Fit = Rfe.fit(Training_Data, Training_Labels)

Prediction_Labels = Rfe.predict(Testing_Data)

Confusion_Matrix = confusion_matrix(Testing_Labels, Prediction_Labels)

New_Data = Rfe.transform(URLS_Without_Labels)

# print(label.shape)
df = pd.DataFrame(New_Data)
df.to_csv('RFEdectree.csv')

print("\nNumber Of Features: %d\n" % Fit.n_features_)
print("Selected Features: \n%s\n" % Fit.support_)
print("Feature Ranking: \n%s\n" % Fit.ranking_)
print("Training Accuracy Score Obtained is: {0:.2f}%".format(Fit.score(Training_Data, Training_Labels)*100.))
print("Testing Accuracy Score Obtained is: {0:.2f}%\n".format(accuracy_score(Testing_Labels, Prediction_Labels)*100.))
print("Classification Report: \n",classification_report(Testing_Labels, Prediction_Labels, target_names=['Phishing Websites', 'Normal Websites']))
print("Confusion Matrix: \n", Confusion_Matrix)
print('\n')

joblib.dump(Rfe, 'RFE_Decision_Tree.pkl')

# print(URLS.columns)
# print(URLS.shape)
# print(URLS.head(5))
# print(len(Training_Data),len(Testing_Data))
# print(len(Training_Labels),len(Testing_Labels))
# print(Training_Labels.value_counts())
# print(Testing_Labels.value_counts())
