# -*- coding: utf-8 -*-
"""Pyrocove_firewall.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YiY718RdxDAxkRUuEUAwhM548VTHUYId
"""

pip install dill

"""#Importing the Libraries"""

import pandas as pd
import dill
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

"""#Random Forest Classifier Implementation

#Importing the Dataset
"""

dataset = pd.read_csv("Reduced Dataset CSV.csv")

print(dataset)

"""#Split the Features"""

url_arr = dataset["url"]
y = dataset["type"]

print(url_arr)

"""#Tokenizer Function"""

def makeTokens(f):
  tknsBySlash = str(f.encode("utf-8")).split("/")
  totalTokens = []

  for i in tknsBySlash:
    tokens = str(i).split("-")
    tokensByDot = []

  for j in range(len(tokens)):
    tempTokens = str(tokens[j]).split(".")
    tokensByDot = tokensByDot + tempTokens
    totalTokens = totalTokens + tokens + tokensByDot

  totalTokens = list(set(totalTokens))

  if 'com' in totalTokens:
    totalTokens.remove('com')

  if 'in' in totalTokens:
    totalTokens.remove('in')

  return totalTokens

print(makeTokens("www.google.com/search-query"))

vectorizer = TfidfVectorizer(tokenizer=makeTokens)

X = vectorizer.fit_transform(url_arr)

print(X)

"""##Split Train and Test Set"""

X_Train, X_Test, Y_Train, Y_Test = train_test_split(X,y, random_state=42, test_size=0.2)

"""##Training

##Create an Object for Random Forest Classifier
"""

RF = RandomForestClassifier(n_estimators=200, criterion='entropy', random_state = 42)

"""#Train the Model"""

RF.fit(X_Train,Y_Train)

"""##Dump the Models"""

with open("url_tokenizer", "wb") as fin0:
  dill.dump(makeTokens, fin0)
  print("Make tokens function dumped.")

with open("url_vectorizer", "wb") as fin1:
  dill.dump(makeTokens, fin1)
  print("Vectorizer object dumped")

with open("url_model", "wb") as fin2:
  dill.dump(RF, fin2)
  print("RF model dumped")

"""##Testing"""

RF.predict(X_Test)

query = vectorizer.transform([
    "https://www.google.co.in",
    "http://kickass.to",
])

RF.predict(query)

"""##Calculate for Score"""

print(RF.score(X_Test, Y_Test))

"""##Helper Function"""

def predictUrl(url):
  X_predict = vectorizer.transform([url])
  return RF.predict(X_predict)

print(predictUrl("http://www.harley-davidson-dijon.com/component/adsmanager/1-/737-"))