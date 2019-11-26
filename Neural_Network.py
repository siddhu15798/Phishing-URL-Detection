import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras import callbacks
from keras.optimizers import *
from keras.layers import Dense
from collections import Counter
from warnings import simplefilter
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

simplefilter(action='ignore', category=FutureWarning)

Data = pd.read_csv('data.csv')
# print(data.head(10))
# print(data.head(10).T)
# print(data.shape)
# print(data.columns)

Classes = Counter(Data['Result'].values)
# print(classes)
# print(classes.most_common())
Classes_Distribution = pd.DataFrame(Classes.most_common(), columns=['Class', 'Number_Of_Observations'])
# print(Classes_Distribution)

# %matplotlib inline
# plt.style.use('ggplot')
# subplot = Classes_Distribution.groupby('Class')['Number_Of_Observations'].sum().plot(kind='barh', width=0.2, figsize=(10,8))

# subplot.set_title('Class distribution of the websites', fontsize = 15)
# subplot.set_xlabel('Number of Observations', fontsize = 14)
# subplot.set_ylabel('Class', fontsize = 14)

# for i in subplot.patches:
#     subplot.text(i.get_width()+0.1, i.get_y()+0.1, \
#             str(i.get_width()), fontsize=11)

# print(data.describe().T)
# print(data.info())

# Mapping the -1 values to 0 in the class labels
Data.rename(columns={'Result': 'Class'}, inplace=True)

Data['Class'] = Data['Class'].map({-1:0, 1:1})
# print(data['Class'].unique())

# Inspection of null values in the dataset
# print(data.isna().sum())

# URLS = pd.read_csv("data.csv")

# URLS = URLS.drop(URLS.columns[[0]], axis=1)

# URLS = URLS.sample(frac=1).reset_index(drop=True)

# URLS_Without_Labels = URLS.drop('Result', axis=1)

# Labels = URLS['Result']

# Training_Data, Testing_Data = train_test_split(URLS_Without_Labels, test_size = 0.25, random_state = 150)

# Training_Labels, Testing_Labels = train_test_split(Labels, test_size = 0.25, random_state = 150)

X = Data.iloc[:,1:31].values.astype(int)
Y = Data.iloc[:,31].values.astype(int)

Training_Data, Testing_Data = train_test_split(X, test_size = 0.20, random_state = 150)

Training_Labels, Testing_Labels = train_test_split(Y, test_size = 0.20, random_state = 150)

# print(X_train.shape)
# print(y_train.shape)
# print(X_test.shape)
# print(y_test.shape)
simplefilter(action='ignore', category=FutureWarning)
Model = Sequential()

# Weights are initialized to small uniformly random values between 0 and 0.05.
Model.add(Dense(45, activation='relu', kernel_initializer='uniform',input_dim=Training_Data.shape[1]))
Model.add(Dense(30, activation='relu', kernel_initializer='uniform'))
Model.add(Dense(1,  activation='sigmoid', kernel_initializer='uniform'))
Model.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])
print(Model.summary())

Early_Stopping = callbacks.EarlyStopping(monitor='loss', min_delta=0.001, patience=5)

History = Model.fit(Training_Data, Training_Labels, batch_size=32, epochs=200, verbose=1, callbacks=[Early_Stopping])
Prediction_Labels = Model.predict(Testing_Data)
scores = Model.evaluate(Testing_Data, Testing_Labels)

print('\nAccuracy score of the Neural Network with basic hyperparameter settings {0:.2f}%\n'.format(scores[1]*100))

joblib.dump(Model, 'Neural_Network.pkl')
# Prediction = []
# for i in range(len(Testing_Data)):
#     Prediction.append(Prediction_Labels[i][0])
    
# for i in range(len(Testing_Data)):
#     if Prediction[i] < 0.5:
#         Prediction[i] == 0
#     elif Prediction[i] > 0.5:
#         Prediction[i] == 1
#     else:
#         Prediction[i] == 0
        
# # Prediction_Lables = Prediction_Labels.reshape((-1,1))
# print(Prediction)
# print(Testing_Labels)
# #print("\nAccuracy Score obtained is : ",accuracy_score(Testing_Labels, Prediction_Labels))

# Confusion_Matrix = confusion_matrix(Testing_Labels, Prediction_Labels)

# print(Confusion_Matrix)