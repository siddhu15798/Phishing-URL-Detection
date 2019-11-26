import joblib
import pandas as pd


url = input("Enter URL you want to test")
#iske baad yeh url feature extraction main jaayega

URL = pd.read_csv("Check.csv")

knn_from_joblib = joblib.load('RFE_Decision_Tree.pkl')

if (knn_from_joblib.predict(URL)) == -1 :
    print("Legitimate URL")
    
else :
    print("Phishing URL")