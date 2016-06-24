import json 

import matplotlib.pyplot as plt
import Graphics as artist
import seaborn as sns 

data = json.load(open('../data/health-topic-prevalence-fb','rb'))



labels,values = zip(*data.items())
fig = plt.figure()
ax = fig.add_subplot(111)
ax.bar(xrange(len(data)),values,color='k',align='center')
artist.adjust_spines(ax)
ax.set_xticks(xrange(len(data)))
ax.set_xticklabels(map(artist.format,labels))
ax.set_ylabel(artist.format('No. of mentions'))
plt.tight_layout()
plt.savefig('../imgs/health_topic.png')