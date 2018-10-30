import numpy as np
import pandas as pd
import re, nltk, gensim
from os.path import join
from os import listdir
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words(['english', 'french','danish', 'russian', 'spanish']))

import pickle
from gensim import matutils
# from gensim.models.ldamodel import LdaModel
from gensim.models.ldamulticore import LdaMulticore
from gensim.corpora import Dictionary
# Plotting tools
# import pyLDAvis
# import pyLDAvis.sklearn
# import matplotlib.pyplot as plt

##################################################################
### preprocessing 
def preprocessing (doc) :
    doc = doc.split(' ')
    new_doc = []
    for w in doc :
        word = re.sub(u'[^a-zA-Z]+', '', w).lower()
        # word = lemmatizer.lemmatize(word)
        if len(word) < 12 and word not in stop_words :
            new_doc.append(word)
    return new_doc



def fit_lda(X, num_topics=5, passes=20):
    """ Fit LDA from a scipy CSR matrix (X). """
    print ('fitting lda...')
    return LdaMulticore(corpus, num_topics = num_topics,
                                id2word = dictionary, 
                                passes = passes,
                                eval_every=5, 
                                workers=5)


def print_topics(lda):
    """ Print the top words for each topic. """
    topics = lda.show_topics(num_topics=-1)
    print (topics)

### load data
data = []
PATH = "content"
file_names = [join(PATH, f) for f in listdir(PATH)]
counter = 0
for f in  file_names :
    try :
        content = preprocessing(open(f).read())
        counter += 1
    except :
        continue
    data.append(content)
    
# data = data[:30]
# now 'data' is our dataset 
print ("Data size :", counter, len(data))

### Vectorize
dictionary = Dictionary(data)
dictionary.filter_extremes(no_below=10, no_above=0.6)
dictionary.save("ldamodel/dictionary.dict")
corpus = [dictionary.doc2bow(doc) for doc in data]

### LDA 
lda = fit_lda(corpus, num_topics=50)
print_topics(lda)

### save model
lda.save("ldamodel/lda.model")



