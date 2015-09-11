# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 04:35:35 2014

@author: ananya
"""


import sunburnt
import solr
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

def extractText(url_file):
     count=0
     with open(url_file, 'rb') as fin:
        count+=1 
        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        h = fin.readlines()
        for html in h:
            try:
                r = requests.head(html)
                if r.status_code == 404:
                    continue
                #print r.status_code
                url = opener.open(html)
                soup=BeautifulSoup(url.read())
    				
                text=''.join(url.text for url in soup.select('article#story p.story-content'))
    				#print(soup.get_text())
    				#text = soup.get_text()
    
    		# break into lines and remove leading and trailing space on each
                lines = (line.strip() for line in text.splitlines())
    		# break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    		# drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)
    				
    				#print soup;
    			   # soup=BeautifulSoup("http://www.nytimes.com/2014/10/21/us/cdc-issues-new-guidelines-for-ebola-care.html?partner=rss&emc=rss" )
    
                title = ""
    				#text = ""
                if soup.title:
                    if soup.title.string:
                        title = soup.title.string
    			
#                comments = soup.findAll(text=lambda text:isinstance(text,Comment))
#                [comment.extract() for comment in comments]
                text_nodes = soup.findAll(text=True)
    
                visible_text = filter(visible, text_nodes)
                text = ''.join(visible_text)
#                print type(text)
                #text = title + " " + text
                webpages.append((html,title, text))
#                for webpage in webpages:
#                    print webpage
#                    print ('***************************************************************************')
            except requests.ConnectionError:
			print ""



def index_to_Solr():
    solr_url = "http://dlib.vt.edu:8080/solr/"      
    numAdded=0  
    solr_instance = sunburnt.SolrInterface(url=solr_url)
#    count=0
    
    with open('/Users/ananya/Desktop/dbms project/data/11_27/test.json','wb') as fout:
        fout.write('[\n')
        for url, ti, webpage in webpages:
            url_md5 = hashlib.md5(url).hexdigest() 
#            solr_instance.add(id=url_md5,url_s=url,text=webpage,title=ti)
            doc = {"id":url_md5, "url":url, "title":ti, "content":webpage}
            solr_instance.add(doc)
            fout.write(repr(doc))
            fout.write('\n,\n\n')
        fout.write(']')
#  
    try: # Try to commit the additions
    	solr_instance.commit()
    except:
    	print "Could not Commit Changes to Solr Instance - check logs"
    else:
    	print "Success. "+str(numAdded)+" documents added to index"  

              
            
def main():
    url_file='/Users/ananya/Desktop/dbms project/data/11_27/url_unshorten.txt'
    extractText(url_file)
    index_to_Solr()

if __name__== "__main__":
    main()     
    
