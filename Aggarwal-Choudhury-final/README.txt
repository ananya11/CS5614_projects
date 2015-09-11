# This is a course project of CS5614: (Big) Data Management Systems developed by 
# Ananya Choudhury and Deepti Aggarwal.


Welcome to the G.R.I.D project!
-------------------------------

G.R.I.D is an end-to-end web archive search engine which provides an efficient information retrieval technic to analyze information related to a disaster.


Getting Started
---------------- 
The code has been written for the G.R.I.D search engine in which the input is the data file and output is the text extract related to tweets in the search engine. The project is divided in four parts and the code for each step is included in this package. The paths mentioned within the code needs to be modified according to the user.

This package contains the following in src folder.

1)Classifier: Classification.py identifies relevant webpages by classifying tweets as relevant and non-relevant based on the tweets. This is written in Python 2.7.0. This outputs a cvs file containing tweets labelled as 0 and 1. This is also outputs a list of URLs extracted from tweets labelled as 1.

2)ExtractUrl: ExtractUrl.java extracts URLs to unshorten URL using MapReduce. IllegalStateException encountered in ExtractUrl class is handled in Precondition.java. The list of short URLs from previous step is the input for this step.

3)Extract URL using MapReduce : ProjectMap1.jar : This is the MapReduce executable of ExtractUrl.java for AWS. This outputs a text file containing actual URLs.

4)TextExtraction: ExtractText.py script uses BeautifulSoup python module to extract text from the webpages. This piece of code takes the list of expanded URLs as input. The output is a tuple of (url, html id, content). This also outputs text files containing the URL and its corresponding extracted  text.

5)Index to Solr: ExtractText.py : This contains a method to index the text extracted from webpage to Solr. This requires a connection to Solr server.

6) Other models used: CrossValidation.py script contains the models we used for classification (LinearSVC). It also contains Cross Validation code that we used to classify data into k folds of test and train.



The Data folder contains: 
- Train.csv : Training data for the classifier
- Test.csv : Test data for the classifier. 
- Unknown.csv: This is the complete unknown dataset used to classify the tweets
- Predicted.csv : This is the output of the classifier.
- Url.txt : This is the input file to Stage 2. This contains the list of unshorten url which is the output for Classification.py Stage 1 mentioned above. 
- out.txt : This is the output file of Stage 2/3. This is the output file of Mapreduce.



The DOC folder contains:
	- Project presentation slides. Project.pptx
	- Final Project report. Aggarwal_Choudhury_Final_Project_Report.pdf

*********************************************************************************************

Classification.py:
--------------------
Implements a Naive Bayes Classifier to output relevant tweets
Train Input: It is a csv file containing tweets in row[1] corresponding labels in row[2] to train the dataset
Tests Input: It is a csv file containing tweets in row[1]
Classifier output: It is a csv file containing tweets in row[1] and the predicted labels in row[2]
Final output: A text file containing the url of the relevant tweets. 



ExtractUrl.java/ProjectMap1.jar:
-----------------
Unshorten the relevant URLs using mapper and reducer
Input: Output of ExtractUrl.java. This is a text file containing the URLS extracted from tweets.
Output: A text file containing the actual URLs.


ExtractText.py: 
-----------------
TextExtraction/Solr: This python script extract texts from the webpages following the parent-child relationship in html source code. 
 	- ExtractText():
		Input: Output of ExtractUrl.java. This is the list of actual URLs.
		Output: The output is the extracted text and title of the webpage
	- index_to_Solr():
		Input: The extracted text and the title of each webpage. 
		Output: The data is indexed to Solr.

***********************************************************************************************

How to run a demo
------------------- 
1. Classifier.py : Update the train.csv, Unknown.csv, Predicted.csv, stop_words.txt file path in the code. Run this. The output will be Predicted.csv and url.txt. 
2. Upload the ProjectMap1.jar file and url.txt file in AWS . Run the code.
3. Take the output from Step2 which is a text file containing actual URLs. This is the input to the next step.
4. This will be input to ExtractText.py. Update the path to the input file in ExtractText().ALso mention the output file path. Running this requires a connection to Solr server. Mention the Solr server URL in index_to_Solr() method.
5. If required, the Solr server can be installed in local machine. Refer to "http://www.apache.org/dyn/closer.cgi/lucene/solr/4.10.2". 
6. The data can be indexed to Solr using SimplePostTool.
7. Velocity interface in Solr needs to be configured as follows:
	- Change solrconfig.xml located at /SOLR_HOME/example/solr/collection1 . 
		- Add <str name="v.template">custom</str>
		- Add <str name="v.layout">cqlayout</str>
		- Replace <requestHandler name="/browse" class="solr.SearchHandler"> with <requestHandler name="/custom" class="solr.SearchHandler">
	- navigate to SOLR_HOME/example/solr/conf/velocity
	- edit VM_global_libray.vm . Replace #macro(url_for_home)#url_for_solr/browse#end  with #macro(url_for_home)#url_for_solr/custom#end  
	- Create cqlayout.vm . Add
<html>
<head>
   #parse("head.vm")  
</head>
  <body>
    <div id="content">
      $content
    </div>
  </body>
</html>
	- Create custom.vm
#*
<div class="navigators">
  #parse("facets.vm")
</div>
*#
	- Modify doc.vm
<div class="result-title"><b>#field('name')</b></div>
<div>Summary: #field('summary')</div>
<div>Release Year: #field('released')</div>
<div>Rank: #field('rank')</div>
<div>Rating: #field('rating')</div>

	- Modify join_doc.vm, query_form.vm, query.vm according to the desired UI layout.

**********************************************************************************************
				
Softwares to be installed:
---------------------------
Python - version 2.7
Python modules : sklearn, nltk, pickle, numpy, pandas, sunburnt, solr, bs4, cookielib
Java - version 1.7
AWS - create an account with Amazon AWS
Solr - version 4.10

***********************************************************************************************

Future Scope:
---------------
- We can enhance the text extraction process to index only the summarized text to Solr- The classification accuracy can be further improved by increasing the training dataset.
- A more sophisticated interface can be built to search the indexed text.
***********************************************************************************************
 
