# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 18:11:41 2014

@author: ananya/ deepti
"""

import re
import csv
import numpy as np
import pandas as pd
#import time

from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB 
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.lda import LDA
from nltk.corpus import stopwords
import nltk.stem.porter as stemming
import string
import nltk

from sklearn import metrics
from sklearn.feature_extraction import text 
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.feature_extraction.text import CountVectorizer

import cPickle as pickle
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import Pipeline


my_words=[]
def validateUrl(tweet):
    regExp = "(?P<url>https?://[a-zA-Z0-9\./-]+)"
    url_li = re.findall(regExp, tweet)     
    #incase of multiple url, even if one url is valid, return true.
    for url in url_li:
        i = url.rfind("/") 
        p=url[i+1:]
        if i+1 < len(url) and len(p) >= 10:
            l=re.compile("[\W]").split(url.lower())
            my_words.extend(l)
            return True    
    return False
    
    
def clean_rawtext(in_raw, out_parsed):
    with open(in_raw, 'r') as fin, \
        open (out_parsed, 'w') as fout:        
        writer=csv.writer(fout, delimiter=',')
        #consider only english tweets and tweets with valid url 
        for row in csv.reader(fin, delimiter=','):
            if row[6]=='en'and validateUrl(row[1]):
                writer.writerow(row)

                        
def train_model(Xtrain,ytrain,binmodel, model): 
    if(model == 'MultinomialNB'):
        clf=MultinomialNB(alpha=0.1)
    elif(model=='LinearSVC'):
        clf=LinearSVC()
    elif(model=='SVC'):
        clf=SVC()
    else:
       clf=MultinomialNB(alpha=0.1) 
    print "---------------------------- Model selected : ", model
    clf.fit(Xtrain,ytrain)
    pickle.dump(clf, open(binmodel, 'wb')) 
 
   
def test_model(Xtest,ytest, binmodel):
  clf = pickle.load(open(binmodel, 'rb'))
  if ytest is not None:
    # reports
    ypred = clf.predict(Xtest)
    print Xtest
    print "Confusion Matrix (Test)"
    print confusion_matrix(ytest, ypred)
    print "Classification Report (Test)"
    print classification_report(ytest, ypred)
    

def extract_Url(pred_output, url_file):
    regExp = "(?P<url>https?://[a-zA-Z0-9\./-]+)"
    with open(pred_output, 'r') as fin, \
        open (url_file, 'w') as fout: 
        #consider only english tweets and tweets with valid url 
        for row in csv.reader(fin, delimiter=','):  
            if row[1]=='1.0':
                url_li = re.findall(regExp, row[0]) 
                for url in url_li:
                    if validateUrl(url):
                        fout.write("%s\n" % url)

            
    
def main():
# path= sys.argv[1]  
    in_raw='/Users/ananya/Desktop/dbms project/data/11_26/train.csv' 
    out_parsed = '/Users/ananya/Desktop/dbms project/data/11_26/train-out.csv'\

# remove noise from raw text
    clean_rawtext(in_raw,out_parsed)
    with open('/Users/ananya/Desktop/dbms project/org/complete/stop_words.txt' ,'wb') as f:
        pickle.dump(my_words,f)

    my_stop_words = text.ENGLISH_STOP_WORDS.union(my_words)
                                 
##    manual train test split
    #train data
    df= pd.read_csv('/Users/ananya/Desktop/dbms project/data/11_26/train-out.csv', 
                    sep=',',header=None,usecols=[1,2,3,6,12,13], encoding='utf8')
    
    text1=np.array(df[1]) 

    vectorizer = TfidfVectorizer(analyzer=u'word',ngram_range=(1,3),norm='l2',lowercase = True,max_df=0.95,stop_words=my_stop_words, max_features=15000)
    X= vectorizer.fit_transform(text1)
                    
    y=np.loadtxt(df[2])

    ch2=SelectKBest(score_func=chi2, k=1500)
    ch2.fit_transform(X,y)

    top_ranked_features = sorted(enumerate(ch2.scores_),key=lambda x:x[1], reverse=True)[:2000]    
    top_ranked_features_indices = map(list,zip(*top_ranked_features))[0]
    sel_kfeatures = (np.array(vectorizer.get_feature_names())[top_ranked_features_indices]).tolist()

    custom_features =[u'@TIMEWorld',u'@RT_com', u'@UN agency', u'@WHO', u'@UN_News_Centre', 
              u'@KGeorgievaEU',u'@hlthnews', u'@SABreakingNews', u'@NewsWireNGR',
              u'@VOA_News', u'[VOA]', u'@eNCAnews', u'@BBCNews', u'@japantimes',
                u'@abc', u'@nprnews', u'@reuters', '@TheWorldPost', u'@IBNMoney_com',
                u'#Deadly',u'\#Virus',u'\#Guinea', u'\#epidemic',  u'\#virus', u'\#SierraLeone',
                u'\#EVD', u'\#AskEbola', u'\#UN',u'\#WHO',u'Retweet this in ',
                u'\#guardian',u'\#RedCross',u'\#Ebola outbreak',u'\#Ebola', u'\#Liberia',
                u'\#ebolavirus',u'#Africa',u'#panic',u'#crisismanagement',u'@guardian',u'@Independent',
                u'@sharethis',u'RT',u'CTV NewsAlert',u'@ReutersAfrica',u'@Federation',u'@IDS_uk',u'@NatGeo',
                u'@BBCWorld',u'Red Cross',u'Deadly',u'West Africa',u'Central Africa',
                u'Ghana',u'Liberia',u'SierraLeone',u'Deaths',u'Reuters', u'#Ebola #virus',
                u'\#Ghana', u'Guinea', u'BBCNews', u'Emergency Plan of Action', u'#Foxnews']
    
    sel_kfeatures.extend(custom_features)
    

    Xtrain = np.array(df[1])
    ytrain = y
        
#    #test data
    in_raw='/Users/ananya/Desktop/dbms project/data/11_26/Unknown.csv'
    out_parsed='/Users/ananya/Desktop/dbms project/data/11_26/Unknown-out.csv'
    clean_rawtext(in_raw,out_parsed)
    df= pd.read_csv(out_parsed, 
                    sep=',',header=None,usecols=[1,2,3,6,12,13], encoding='utf8')   
    Xtest=np.array(df[1])
#    ytest=np.loadtxt(df[2]) # labels on which the target will be classified  
    
    
    classifier = Pipeline([
        ('tfidf', TfidfVectorizer(vocabulary=sel_kfeatures)),  
        ('clf', MultinomialNB())])
        
                           
    classifier.fit(Xtrain, ytrain)
#    print Xtrain
    predicted = classifier.predict(Xtest)
    
    pred = '/Users/ananya/Desktop/dbms project/data/11_26/predicted.csv'
    out = '/Users/ananya/Desktop/dbms project/data/11_26/url.txt'
#    print Xtest
    with open(pred, 'wb') as fout:
        output=csv.writer(fout, delimiter=',')
        for item, labels in zip(Xtest, predicted):
            output.writerow([item, labels])

    
    extract_Url(pred,out)
        
#    print "Confusion Matrix (Test)"
#    print confusion_matrix(ytest, predicted)
#    print "Classification Report (Test)"
#    print classification_report(ytest, predicted)
        
   
#                                     
#    train_model(Xtrain, ytrain, "/Users/ananya/Desktop/dbms project/data/model.bin", 'Multinomial')
#    test_model(Xtest, ytest, "/Users/ananya/Desktop/dbms project/data/model.bin")  
#   
#    train_model(Xtrain, ytrain, "/Users/ananya/Desktop/dbms project/data/model.bin", 'LinearSVC')
#    test_model(Xtest, ytest, "/Users/ananya/Desktop/dbms project/data/model.bin") 
    

    
if __name__== "__main__":
    main()