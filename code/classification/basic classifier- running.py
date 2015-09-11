# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 22:53:16 2014

@author: ananya
"""
import re
import csv
import pandas as pd
import numpy as np

from sklearn import cross_validation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB 
from sklearn import metrics


#train data
df= pd.read_csv('/Users/ananya/Desktop/dbms project/data/train.csv', 
                sep=',',header=None,usecols=[1,2,3,6,12,13], encoding='utf8')
X_train=np.array(df[1])
y_train=np.array(df[2])

#test data
df= pd.read_csv('/Users/ananya/Desktop/dbms project/data/test copy.csv', 
                sep=',',header=None,usecols=[1,2,3,6,12,13], encoding='utf8')   
X_test=np.array(df[1])
y_test=np.loadtxt(df[2]) # labels on which the target will be classified



from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

           

classifier = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),  
    ('ch2', SelectKBest(chi2, k=100)),
    ('clf', MultinomialNB())])
    
                       
classifier.fit(X_train, y_train)
predicted = classifier.predict(X_test)

for item, labels in zip(X_test, predicted):
    print '%s => %s' % (item, labels)
    
#print np.mean(predicted==y_test)
    
