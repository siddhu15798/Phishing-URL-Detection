import joblib
import pandas as pd
from warnings import simplefilter
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report

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

Model = LogisticRegression(random_state=0)

Rfe = RFE(Model, 15)

Fit = Rfe.fit(Training_Data, Training_Labels)

Prediction_Labels = Rfe.predict(Testing_Data)

New_Data = Rfe.transform(URLS_Without_Labels)

# print(label.shape)
df = pd.DataFrame(New_Data)
df.to_csv('RFElogreg.csv')

Confusion_Matrix = confusion_matrix(Testing_Labels, Prediction_Labels)

print("\nNumber Of Features: %d\n" % Fit.n_features_)
print("Selected Features: \n%s\n" % Fit.support_)
print("Feature Ranking: \n%s\n" % Fit.ranking_)
print("Training Accuracy Score Obtained is: {0:.2f}%".format(Fit.score(Training_Data, Training_Labels)*100.))
print("Testing Accuracy Score Obtained is: {0:.2f}%\n".format(accuracy_score(Testing_Labels, Prediction_Labels)*100.))
print("Classification Report: \n",classification_report(Testing_Labels, Prediction_Labels, target_names=['Phishing Websites', 'Normal Websites']))
print("Confusion Matrix: \n", Confusion_Matrix)
print('\n')

joblib.dump(Rfe, 'RFE_Logistic_Regression.pkl')
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