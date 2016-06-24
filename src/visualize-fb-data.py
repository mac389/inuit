import json, os 

import matplotlib.pyplot as plt
import Graphics as artist 

from textblob import Word
from awesome_print import ap
from string import punctuation 
from nltk.corpus import stopwords as stopz

data = json.load(open(os.path.join('..','data','word-frequencies.json'),'rb'))
stopwords = open(os.path.join('..','data','stopwords')).read().splitlines()
stp = stopz.words('english')

#Further clean up
for word,frequency in data.items():
	if "u'" in word or '\\n' in word:
		new_word = word.replace("u'","").replace('\\n',"").lower().replace(punctuation,"")
		if new_word.isalpha() and new_word not in stopwords and new_word not in stp:
			new_word = Word(new_word).lemmatize()
			if new_word in data: #Different forms of word in DB. Combine the associated frequencies. 
				freqs = data[new_word]
				data[new_word] = freqs + data[word]
				del data[word]
			else:
				data[new_word] = data[word]
				del data[word]
		else:
			del data[word]
	if word.isupper():
		if word.lower() in data:
			freq = data[word.lower()]
			data[word.lower()] = freq + data[word]
			del data[word]
	if word in stopwords or word in stp:
		del data[word]

ap(data)
json.dump(data,open(os.path.join('..','data','word-frequencies.json'),'wb'))

cutoff = 20


fig = plt.figure()
ax = fig.add_subplot(111)
labels,freqs = zip(*sorted(data.items(),key=lambda x:x[1],reverse=True)[:cutoff])
ax.plot(freqs,'k--',linewidth=2)
artist.adjust_spines(ax)

ax.set_xticks(range(len(labels)))

ax.set_xticklabels(map(artist.format,[label.replace('#','\#').replace('@','\@').replace('_',' ') for label in labels]),rotation='vertical')

#ax.set_title(artist.format('%d-gram of %s, %s'%(ngram,field,condition)))
plt.tight_layout()
plt.savefig('../imgs/words-on-facebook.png')
