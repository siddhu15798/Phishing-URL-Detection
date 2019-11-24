import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from warnings import simplefilter
from sklearn import model_selection
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

simplefilter(action='ignore', category=FutureWarning)

URLS = pd.read_csv("data.csv")

url = URLS.values

X = url[:,1:31]

Y = url[:,31]

Seed = 5
Names = []
Models = []
Results = []
Scoring = 'accuracy'

Models.append(('SVM', SVC()))
Models.append(('NB', BernoulliNB()))
Models.append(('LR', LogisticRegression()))
Models.append(('KNN', KNeighborsClassifier()))
Models.append(('RF', RandomForestClassifier()))
Models.append(('DTC', DecisionTreeClassifier()))

for Name, Model in Models:
    
    K_Fold = model_selection.KFold(n_splits = 10, random_state = Seed)
    CV_Results = model_selection.cross_val_score(Model, X, Y, cv = K_Fold, scoring = Scoring)
    
    Names.append(Name)
    Results.append(CV_Results)
    
    Msg = "%s: %f (%f)" % (Name, CV_Results.mean(), CV_Results.std())
    print(Msg)

fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(Results)
ax.set_xticklabels(Names)
plt.show()