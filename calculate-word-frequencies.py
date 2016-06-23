import nltk, os, re, itertools, json, random

from collections import Counter
from awesome_print import ap 
from progress.bar import Bar
from string import punctuation
from nltk.stem.wordnet import WordNetLemmatizer

DIRECTORY = os.path.join(os.getcwd(),'data')
CASE = os.path.join(DIRECTORY,'case')
CONTROL = os.path.join(DIRECTORY,'control')

paths = {'case':os.path.join(DIRECTORY,'case'),
   		'control':os.path.join(DIRECTORY,'control')}

READ = 'rb'
WRITE = 'wb'

lmtzr = WordNetLemmatizer()
stopwords = open("stopwords",READ).read().splitlines()
fields = ['hashtags','mentions','tokens']
def camel_case_split(identifier):
    matches = re.finditer('(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', identifier)
    split_string = []
    # index of beginning of slice
    previous = 0
    for match in matches:
        # get slice
        split_string.append(identifier[previous:match.start()])
        # advance index
        previous = match.start()
    # get remaining string
    split_string.append(identifier[previous:])
    return split_string

def getHashtags(tokens):
	return [token for token in tokens if token.startswith('#') and len(token)>1]

def getMentions(tokens):
	return [token for token in tokens if token.startswith('@') and len(token)>1]

def clean(words):
	words = [word.lower() for word in itertools.chain.from_iterable(map(camel_case_split,words))]
	words = [word for word in nltk.word_tokenize(' '.join(words))
				if not any([word in nltk.corpus.stopwords.words('english'), word in stopwords,
						  't.co' in word, word in punctuation])]

	words = [re.sub(r'^https:\/\/.*[\r\n]*', '', word, flags=re.MULTILINE) for word in words]
	return [lmtzr.lemmatize(word) for word in words if all([word != '',len(word)>2,word.isalpha()])]

def process(string,isbar=False):
	string = string.encode('utf-8').decode('ascii','ignore')
	words = string.split()

	ans = {}
	ans['hashtags'] = getHashtags(words)
	ans['mentions'] = getMentions([word for word in words if word not in ans['hashtags']])
	ans['tokens'] = clean([word for word in words if word not in ans['mentions']])
	
	if bar:
		bar.next()

	return ans

def bigrams(text):
	return [' '.join(bigram) for bigram in nltk.bigrams(text)]

for name,path in paths.iteritems():
	if name == 'control':
		filenames = random.sample(os.listdir(path),30*len(os.listdir(paths['case'])))
		bar = Bar('Processing tweets', max=len(filenames))
		#There are 1404 files in the "case" files as of 4/24/2016
		tweets = [process(json.load(open(os.path.join(path,filename),READ))['text'])
									for filename in filenames]
	elif name == 'case':
		bar = Bar('Processing tweets', max=20*len(os.listdir(path)))
		tweets = [process(line.split(' | ')[0],isbar=True) for filename in os.listdir(path)
				for line in open(os.path.join(path,filename),READ).read().splitlines()]

	bar.finish()

	ap('Calculating 1-grams')
	#-- Calculate 1 grams
	json.dump({field:Counter(itertools.chain.from_iterable([tweet[field] for tweet in tweets]))
					for field in fields},
				open('1-gram-frequencies-%s.json'%name,WRITE))

	ap('Calculating 2-grams')
	#-- Calculate 2-grams
	json.dump({field:Counter(itertools.chain.from_iterable([bigrams(tweet[field]) for tweet in tweets]))
					for field in fields},
				open('2-gram-frequencies-%s.json'%name,WRITE))