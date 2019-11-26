import joblib
import pandas as pd


url = input("Enter URL you want to test")
#iske baad yeh url feature extraction main jaayega

URL = pd.read_csv("a.csv")

knn_from_joblib = joblib.load('KNN.pkl')

print(knn_from_joblib.predict(URL))