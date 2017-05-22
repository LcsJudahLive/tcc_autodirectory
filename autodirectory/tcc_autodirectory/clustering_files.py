from __future__ import print_function
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
import newpdf
from sklearn import feature_extraction
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import mpld3

pdf_path = '/new'
path = '/home/lucas/files'
#newpdf.main(pdf_path, path)
file_titles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
text = ''
documents_text = []


for file in file_titles:
	open_file = codecs.open(path + '/' + file,'rb',encoding="utf-8")
	for line in open_file.read().encode('ascii',"ignore"):
		#line = unicode(line,encoding='utf-8')
		text += line
	open_file.close()
	documents_text.append(text)
	text = ''

stopwords = nltk.corpus.stopwords.words('english')
stemmer = SnowballStemmer("english") 

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

#not super pythonic, no, not at all.
#use extend so it's a big flat list of vocab
totalvocab_stemmed = []
totalvocab_tokenized = []
for i in documents_text:
    allwords_stemmed = tokenize_and_stem(i) #for each item in 'synopses', tokenize/stem
    totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
    
    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
#print 'there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame'

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(documents_text) #fit the vectorizer to synopses

print(tfidf_matrix.shape)

terms = tfidf_vectorizer.get_feature_names()

from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)
print
print

from sklearn.cluster import KMeans

num_clusters = 20
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

from sklearn.externals import joblib
#uncomment the below to save your model 
#since I've already run my model I am loading from the pickle

joblib.dump(km,  'doc_cluster.pkl')

km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()

documents = {'title': file_titles, 'text': documents_text, 'cluster':clusters }
frame = pd.DataFrame(documents, index = [clusters] , columns = ['title', 'text', 'cluster'])

frame['cluster'].value_counts()


print("Top terms per cluster:")
print()
#sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')
    
    for ind in order_centroids[i, :6]: #replace 6 with n words per cluster
        print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
    print() #add whitespace
    print() #add whitespace
    
    print("Cluster %d titles:" % i, end='')
    if type(frame.ix[i]['title']) is str:
    	values = frame.ix[i]['title']
    	string = True
    else:
    	values = frame.ix[i]['title'].values.tolist()
    	string = False
    
    if string == False:
    	print(", ".join(values))
    else:
		print(' %s,' % values, end='')
    
    print() #add whitespace
    print() #add whitespace