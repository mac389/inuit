import json, os 

import matplotlib.pyplot as plt
import Graphics as artist 

from awesome_print import ap

data = json.load(open(os.path.join('..','data','word-frequencies.json'),'rb'))

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