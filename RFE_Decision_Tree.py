import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.model_selection import GridSearchCV

URLS = pd.read_csv("data.csv")

URLS = URLS.drop(URLS.columns[[0]], axis=1)

URLS = URLS.sample(frac=1).reset_index(drop=True)

URLS_Without_Labels = URLS.drop('Result', axis=1)

Labels = URLS['Result']

Training_Data, Testing_Data = train_test_split(URLS_Without_Labels, test_size=0.3, random_state=110)

Training_Labels, Testing_Labels = train_test_split(Labels, test_size=0.3, random_state=110)

Model = DecisionTreeClassifier()

Rfe = RFE(Model, 15)

Fit = Rfe.fit(Training_Data, Training_Labels)

Prediction_Labels = Rfe.predict(Testing_Data)

Confusion_Matrix = confusion_matrix(Testing_Labels, Prediction_Labels)

# print(URLS.columns)
# print(URLS.shape)
# print(URLS.head(5))
# print(len(Training_Data),len(Testing_Data))
# print(len(Training_Labels),len(Testing_Labels))
# print(Training_Labels.value_counts())
# print(Testing_Labels.value_counts())
# print(Confusion_Matrix)
# print("\nAccuracy Score obtained is : ",accuracy_score(Testing_Labels, Prediction_Labels))

print('Accuracy score obtained is {0:.2f}%'.format(accuracy_score(Testing_Labels, Prediction_Labels)*100.))

print(Confusion_Matrix)

# Importance = Rfe.feature_importances_

# Indices = np.argsort(Importance)[::-1] 

# print("\nIndices of columns : {Indices}")

# print("\nFeature ranking: \n")

# print("Feature name : Importance\n")

# print("The blue bars are the feature importances of the randomforest classifier\n")

# for f in range(Training_Data.shape[1]):
    
#     print(f"{f+1} {Training_Data.columns[Indices[f]]}   :  {Importance[Indices[f]]} \n")

# plt.figure()

# plt.title("Feature importances")

# plt.barh(range(Training_Data.shape[1]), Importance[Indices], color="b", align="center")   

# plt.yticks(range(Training_Data.shape[1]), Training_Data.columns[Indices])

# plt.ylim([-1, Training_Data.shape[1]])

# plt.rcParams['figure.figsize'] = (35,15)

# plt.show()