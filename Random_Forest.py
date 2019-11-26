import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from warnings import simplefilter
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

Training_Data, Testing_Data = train_test_split(URLS_Without_Labels, test_size=0.25, random_state=150)

Training_Labels, Testing_Labels = train_test_split(Labels, test_size=0.25, random_state=150)

# parameters = [{'n_estimators': [100, 700],
#     'max_features': ['sqrt', 'log2'],
#     'criterion' :['gini', 'entropy']}]
# grid_search = GridSearchCV(RandomForestClassifier(),  parameters,cv =5, n_jobs= -1)
# grid_search.fit(Training_Data, Training_Labels)
# print("Best Accurancy =" +str( grid_search.best_score_))
# print("best parameters =" + str(grid_search.best_params_)) 

Random_Forest_Classifier = RandomForestClassifier(random_state=0)

Random_Forest_Classifier.fit(Training_Data, Training_Labels)

Prediction_Labels = Random_Forest_Classifier.predict(Testing_Data)

Confusion_Matrix = confusion_matrix(Testing_Labels, Prediction_Labels)

# Custom_Random_Forest_Classifier = RandomForestClassifier(n_estimators=700, random_state=0, max_features = 'log2', criterion = "gini", max_depth=100, max_leaf_nodes=20000)
# Custom_Random_Forest_Classifier.fit(Training_Data, Training_Labels)
# Custom_Prediction_Labels = Custom_Random_Forest_Classifier.predict(Testing_Data)
# Confusion_Matrix_2 = confusion_matrix(Testing_Labels, Custom_Prediction_Labels)

#print(URLS.columns)
#print(URLS.shape)
#print(URLS.head(5))
#print(len(Training_Data),len(Testing_Data))
#print(len(Training_Labels),len(Testing_Labels))
#print(Training_Labels.value_counts())
#print(Testing_Labels.value_counts())
print("\nTraining Accuracy Score Obtained is: {0:.2f}%".format(accuracy_score(Training_Labels, Random_Forest_Classifier.predict(Training_Data))*100.))
print("Testing Accuracy Score Obtained is: {0:.2f}%\n".format(accuracy_score(Testing_Labels, Prediction_Labels)*100.))
print("Classification Report: \n",classification_report(Testing_Labels, Prediction_Labels, target_names=['Phishing Websites', 'Normal Websites']))
print("Confusion Matrix: \n", Confusion_Matrix)

joblib.dump(Random_Forest_Classifier, 'Random_Forest.pkl')

Importance = Random_Forest_Classifier.feature_importances_

Indices = np.argsort(Importance)[::-1] 

print("\nIndices of columns : {Indices}")

print("\nFeature ranking: \n")

print("Feature name : Importance\n")

print("The blue bars are the feature importances of the randomforest classifier\n")

for f in range(Training_Data.shape[1]):
    
    print(f"{f+1} {Training_Data.columns[Indices[f]]}   :  {Importance[Indices[f]]} \n")

plt.figure()

plt.title("Feature importances")

plt.barh(range(Training_Data.shape[1]), Importance[Indices], color="b", align="center")   

plt.yticks(range(Training_Data.shape[1]), Training_Data.columns[Indices])

plt.ylim([-1, Training_Data.shape[1]])

plt.rcParams['figure.figsize'] = (35,15)

plt.show()