import numpy as np
from gensim import corpora, models
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from gensim import matutils

from os import listdir
from os.path import join
import enchant
import re
import pandas as pd
import pickle
import operator

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt

### path
MODEL_FILE_PATH = "ldamodel/lda.model"
DICTIONARY_PATH = "ldamodel/dictionary.dict"

# #Load Model and File :
ldamodel = LdaModel.load(MODEL_FILE_PATH)
dictionary = Dictionary.load(DICTIONARY_PATH)

# preprocessing
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
# eng = enchant.Dict("en_US")

## load community 
comm_df = pd.read_csv('dat/community.csv')
users = comm_df[comm_df.modularity_class == 1].Label

#####
#####
def preprocessing (doc) :
    doc = doc.split(' ')
    new_doc = []
    for w in doc :
        word = re.sub(u'[^a-zA-Z]+', '', w).lower()
        # word = lemmatizer.lemmatize(word)
        if len(word) < 12 and word not in stop_words :
            new_doc.append(word)
    return ' '.join(new_doc)


def get_lda_topics (doc) :
    new_vec = dictionary.doc2bow(doc.split(" "))
    topics = ldamodel.get_document_topics(new_vec)
    return topics
    
##############################################################

list_topics = {}
doc = ''
for user in users :
    user = user[1:]
    try :
        doc += open(join('content', user)).read() + ' '
    except :
        continue
## now 'doc' is community content
doc = preprocessing(doc)
topics = get_lda_topics(doc)

terms = {}
total_score = 0
for topic, score in topics :
    for word, word_score in ldamodel.get_topic_terms(topic, topn=10):
        word = dictionary.get(word)
        if word not in terms :
            terms[word] = score *word_score
            total_score += score *word_score
        else :
            terms[word] += score *word_score
            total_score += score *word_score

for word in terms :
    terms [word] = terms[word] / total_score

### word cloud
import random 
def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(150, 240)

x, y = np.ogrid[:300, :300]
mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
mask = 255 * mask.astype(int)

wordcloud = WordCloud(width = 500, height = 400, 
                      background_color="black", mask=mask).generate_from_frequencies(terms)
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)#.recolor(color_func=grey_color_func, random_state=3),
        #    interpolation="bilinear")
plt.savefig("example.png")
plt.show()




