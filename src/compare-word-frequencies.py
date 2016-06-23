import nltk, os, re, itertools, json, random

import Graphics as artist
import matplotlib.pyplot as plt 
import utils as tech

from collections import Counter
from awesome_print import ap 
from progress.bar import Bar
from matplotlib import rcParams

rcParams['text.usetex'] = True

DIRECTORY = os.path.join(os.getcwd(),'data')
CASE = os.path.join(DIRECTORY,'case')
CONTROL = os.path.join(DIRECTORY,'control')
READ = 'rb'

paths = {'case':os.path.join(DIRECTORY,'case'),
   		'control':os.path.join(DIRECTORY,'control')}

ngrams = [1,2]

def broadcast(x):
	print x
	return 1

fields = ['hashtags','mentions','tokens']

cutoff = 20
for ngram in ngrams:
	for condition in ['case','control']:
		data = json.load(open('%d-gram-frequencies-%s.json'%(ngram,condition),READ))
		for field in fields:
			fig = plt.figure()
			ax = fig.add_subplot(111)
			labels,freqs = zip(*sorted(data[field].items(),key=lambda x:x[1],reverse=True)[:cutoff])
			ax.plot(freqs,'k--',linewidth=2)
			artist.adjust_spines(ax)

			ax.set_xticks(range(len(labels)))

			ax.set_xticklabels(map(artist.format,[label.replace('#','\#').replace('@','\@').replace('_',' ') for label in labels]),rotation='vertical')

			ax.set_title(artist.format('%d-gram of %s, %s'%(ngram,field,condition)))
			plt.tight_layout()
			plt.savefig('%d-gram-%s-%s.png'%(ngram,field,condition))

			del fig,ax