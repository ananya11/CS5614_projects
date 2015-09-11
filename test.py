# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 04:35:35 2014

@author: ananya
"""


import sunburnt
import hashlib

from bs4 import BeautifulSoup,Comment
import urllib2
from cookielib import CookieJar
import requests
import httplib2

webpages=[]


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head']:
        return False
    return True
 
import sys

def extractText(url_file):
     count=0
     with open(url_file, 'rb') as fin:
        count+=1 
#        cj = CookieJar()
#        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urls = fin.readlines()
        for url in urls:
            try:
                r = requests.get(url,timeout=10,verify=False)
            except:
                print sys.exc_info()[0]
                continue
            page = r.content or r.text
            soup = BeautifulSoup(page)
            title = ""
            text = ""
            if soup.title:
                if soup.title.string:
                    title = soup.title.string
#               comments = soup.findAll(text=lambda text:isinstance(text,Comment))
#            [comment.extract() for comment in comments]
            text_nodes = soup.findAll(text=True)    
            visible_text = filter(visible, text_nodes)
            text = ''.join(visible_text)
            #text = title + " " + text
            webpages.append((url,title, text))


def index_to_Solr():
#    solr_url = "http://localhost:8983/solr" 
      
#    solr_instance = sunburnt.SolrInterface(url=solr_url, http_connection=h)
#    count=0
    
    for url, title, webpage in webpages:
        h = hashlib.md5(url).hexdigest() 
        doc = {"id":h, "url":url, "title":title, "content":webpage}
        print doc
        
#        solr_instance.add(**doc)
#
#    try:
#        solr_instance.commit()
#    except:
#          print "Could not Commit Changes to Solr, check the log files."
#    else:
#          print "Successfully committed changes"


              
            
def main():
    url_file='/Users/ananya/Desktop/dbms project/data/11_27/url_unshorten.txt'
    extractText(url_file)
    index_to_Solr()

if __name__== "__main__":
    main()     
    
