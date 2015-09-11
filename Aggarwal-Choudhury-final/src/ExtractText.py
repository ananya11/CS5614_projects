# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup,Comment
import urllib2
from cookielib import CookieJar
import requests
import re
import socket
import errno 
import csv
from urllib2 import urlopen
import httplib
import sys
import os



webpages=[]

def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head']:
		return False
	return True


def extractText(url_file):
     count=1021
     with open(url_file, 'rb') as fin:
        
        #cj = CookieJar()
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        #h = fin.readlines()
        for row in csv.reader(fin, delimiter='\t'):
            html=row[0]
            count+=1 
            req = urllib2.Request(html)
            try:
                #r = requests.head(html)
                urllib2.urlopen(req)
                #url=html
#                soup=extract_url_text(html)
#                if soup!= False:
                
                   # continue
                #print r.status_code
                cj = CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                url = opener.open(html)
                #trackerURLformat = url + 'jobtasks.jsp?jobid=%s&type=%s&pagenum=1'
                soup=BeautifulSoup(url.read())
                taskURLs = [h.get('href') for h in soup.find_all(href=re.compile('taskdetails'))]
                #soup = BeautifulSoup(url)                
                print "step3"
                # Now that we know where all the tasks are, go find their logs
                logURLs = []
                for taskURL in taskURLs:
                    taskHTML =  opener.open(url + taskURL).read()
                    soup = BeautifulSoup(taskHTML)
                    allLogURL = soup.find(href=re.compile('all=true')).get('href')
                    print "step1"
                    logURLs.append(allLogURL)

            # Now fetch the stdout log from each
                for logURL in logURLs:
                    logHTML = opener.open(logURL).read()
                    soup = BeautifulSoup(logHTML)
                    soup=soup
               
                text=''.join(url.text for url in soup.select('article#story p.story-content'))
    				#print(soup.get_text())
    				#text = soup.get_text()
                lines = (line.strip().replace('((','').replace(',)','').replace("'",'').replace('\t','').replace('#','').replace('@','').trim() for line in text.splitlines())
    		# break multi-headlines into a line each
                chunks = (phrase.strip().replace('((','').replace(',)','').replace("'",'').replace('\t','').replace('\t','').replace('#','').replace('@','').trim() for line in lines for phrase in line.split("  "))
                chunks=('\t!@#$%^&*()[]{};:,./<>?\|`~-=_+\t#123456789}{' if x == '' else x for x in chunks)
    		# drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)
    				
    				#print soup;
    			   # soup=BeautifulSoup("http://www.nytimes.com/2014/10/21/us/cdc-issues-new-guidelines-for-ebola-care.html?partner=rss&emc=rss" )
    
                title = ""
    				#text = ""
                if soup.title:
                    if soup.title.string:
                        title = soup.title.string
    			
                comments = soup.findAll(text=lambda text:isinstance(text,Comment))
                [comment.extract() for comment in comments]
                text_nodes = soup.findAll(text=True)
    
                visible_text = filter(visible, text_nodes)
                text = ''.join('\t!@#$%^&*()[]{};:,./<>?\|`~-=_+\t#123456789}{' if x == '' else x for x in visible_text)
                #text = title + " " + text
                webpages.append((url,title, text))
                for webpage in webpages:
                   
                        number=sys.getsizeof(webpage[2].replace('!@#$%^&*()[]{};:,./<>?\|`~-=_+\t#123456789}{', '').replace('\n',' '))
                        print number
                        if(number>8000):
                            with open('D:\\webpages\\webpage'+repr(count)+'.txt', 'wb') as fout:
                                fout.write(html)
        #                        fout.write('\n')
        #                        fout.write(title)
                                fout.write('\n\n')
                                #tuple('\t' if x == '' else x for x in webpage[2])
                                
                                fout.write(webpage[2].encode('utf-8'))
#                b= os.path.getsize('D:\\webpages\\webpage'+str(count)+'.txt')
#                if b<1500:
#                    os.remove('D:\\webpages\\webpage'+str(count)+'.txt')
#                if b>3:
#                    os.remove('D:\\webpages\\webpage'+str(count)+'.txt')
#                        #fout.write(tuple.encode('utf-8'))
 
                            #print ('***************************************************************************')
            except  urllib2.HTTPError as e:
			print ""
            except (ValueError, urllib2.URLError) as e1:
			print ""
            except httplib.BadStatusLine as e:
                    print ""
                    
            except httplib.IncompleteRead as e3:
                
                print ""
            
                
            
        
            except socket.error as error:
                if error.errno == 10054:
                    print""
                   
        

#            with open('C:\\Users\\Deepti\\Downloads\\FAll_2014\\Database\\Project\\Scripts\\webpage.txt', 'wb') as fout:
#                fout.write(webpage)				
		#
		#                fout.write('***************************************************************************')

        
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
    url_file='C:\\Users\\Deepti\\Documents\\MATLAB\\DBMS\\trialrun\\out.txt'
    extractText(url_file)
    index_to_Solr()

if __name__== "__main__":
    main()     
    
