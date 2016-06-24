import os, nltk, json

from nltk.corpus import wordnet, stopwords
from textblob import TextBlob
from awesome_print import ap 
from collections import Counter

data =  TextBlob(open(os.path.join('..','data','text-of-facebook-posts'),'rb').read())
my_stopwords = open(os.path.join('..','data','stopwords')).read().splitlines()

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

words = data.tags
print len(words)
words = [word.lemmatize(get_wordnet_pos(pos)) for word,pos in data.tags if word not in my_stopwords and word not in stopwords.words('english')]
print len(words)
#ap(data)

json.dump(Counter(words),open(os.path.join('..','data','word-frequencies.json'),'wb'))