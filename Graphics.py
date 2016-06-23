import nltk, string, json, os

from nltk import word_tokenize

import numpy as np

import matplotlib.pyplot as plt

from matplotlib import rcParams

rcParams['text.usetex'] = True

exclude = set(string.punctuation)
READ = 'rb'
#directory = json.load(open('/Volumes/My Book/Dropbox/Toxic/dictionary.json',READ))

#stopwords = [word.rstrip('\r\n').strip() for word in open(directory['stopwords'],READ).readlines()]
#emoticons = [word.rstrip('\r\n').strip() for word in open(directory['emoticons'],READ).readlines()]

def format(text):
    return lambda text:r'\Large \textbf{\textsc{%s}}'%text


def my_boxplot(ax, positions, values, width=None, color=None, label=None):
    """Custom box plot to work around some of matplotlib's quirks.
 
    Parameters
    ----------
    ax : matplotlib axis
        Target axis.
    positions : (M,) ndarray of float
        Where to positions boxes on the x-axis.
    values : (M, N) ndarray of float
        The percentiles of each row of ``values`` is box-plotted. 
    width : float
        Width of the boxes.
    color : str
        Matplotlib color code.
 
    """
    if width is None:
        width = 1
    if color is None:
        color = 'r'
    
    x = np.column_stack((positions, positions))
    p25, p75 = np.percentile(values, [25, 75], axis=1)
    whisker_lower = np.column_stack((np.min(values, axis=1), p25))
    whisker_upper = np.column_stack((p75, np.max(values, axis=1)))
    plt.plot(x.T, whisker_lower.T, '%s-_' % color)
    plt.plot(x.T, whisker_upper.T, '%s-_' % color)
 
    zero_mid_percentile, = np.where(p25 == p75)
    w = width / 2. 
    for ix in zero_mid_percentile:
        pos = positions[ix]
        med = np.median(values[ix])
        plt.plot([pos - w, pos + w], [med, med], color, linewidth=6)
 
    bp = ax.boxplot(values.T, positions=positions, sym='', widths=width, whis=0)
    plt.setp(bp['boxes'], linewidth=1, color=color)
    plt.setp(bp['medians'], linewidth=2, color=color)
    plt.setp(bp['caps'], visible=False)
    plt.setp(bp['fliers'], visible=False)
    
    ax.plot(positions, np.median(values, axis=1), color, linewidth=2, label=label)

def adjust_spines(ax,spines=['bottom','left']):
	for loc, spine in ax.spines.iteritems():
		if loc in spines:
			spine.set_position(('outward',10))
			#spine.set_smart_bounds(True) #Doesn't work for log log plots
			spine.set_linewidth(1)
		else:
			spine.set_color('none') 
	if 'left' in spines:
		ax.yaxis.set_ticks_position('left')
	else:
		ax.yaxis.set_ticks([])

	if 'bottom' in spines:
		ax.xaxis.set_ticks_position('bottom')
	else:
		ax.xaxis.set_ticks([])

format = lambda text: r'\Large \textbf{\textsc{%s}}'%text

def frequencies(words, ax=None, cutoff=30, savename=None,base='../data'):
    words = [word.lower() for word in words]
    words = [word for word in words if word not in stopwords 
                                    and word not in emoticons
                                    and all(ord(letter)<128 for letter in word) 
                                    and word  not in ['rt','amp']
                                    and not any(ch in word for ch in exclude)
                                    and len(word)>3]
    fdist = nltk.FreqDist(words)
    freqs = fdist.items()[:cutoff]
    word,f =zip(*freqs)
    if savename:
        with open(os.path.join(base,savename),'wb') as fid:
            for w,ff in zip(word,f):
                print '%s \t %d'%(w,ff)        

    f = np.array(f).astype(float)
    f /= float(f.sum())
    if not ax:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    ax.plot(f,'k',linewidth=2)
    adjust_spines(ax)
    ax.yaxis.grid()
    ax.xaxis.grid()
    ax.set_xticks(range(len(word)))
    ax.set_xticklabels(map(format,word),range(len(word)), rotation=90)
    ax.set_ylabel(r'\Large $\log \left(\mathbf{Frequency}\right)$')
    plt.tight_layout()
    plt.show()