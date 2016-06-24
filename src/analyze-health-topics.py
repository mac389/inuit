import json, os

from itertools import izip
from awesome_print import ap 

#-- Facebook

health_topics = json.load(open(os.path.join('..','data','health-topics.json'),'rb'))
words = json.load(open(os.path.join('..','data','word-frequencies.json')))

data = {topic:None for topic in health_topics}

for topic in data:
	data[topic] = sum([freq for word,freq in words.iteritems() if word in health_topics[topic]])

json.dump(data,open(os.path.join('..','data','health-topic-prevalence-fb'),'wb'))
ap(data)

#For blood pressure, really should analyze bigrams

#-- Twitter
DIRECTORY = os.path.join('..','data')
READ = 'rb'

paths = {'case':os.path.join(DIRECTORY,'case'),
   		'control':os.path.join(DIRECTORY,'control')}

data = {"case":{topic:None for topic in health_topics},"control":{topic:None for topic in health_topics}}

for condition in ['case','control']:
	unigrams = json.load(open(os.path.join(DIRECTORY,'1-gram-frequencies-%s.json'%(condition)),READ))
	bigrams = json.load(open(os.path.join(DIRECTORY,'2-gram-frequencies-%s.json'%(condition)),READ))

	for topic in health_topics:
		topic_sum = 0

		for unigram,freq_uni in unigrams.iteritems():
			if unigram in health_topics[topic]:
			 	topic_sum += freq_uni

		for bigram, freq_bi in bigrams.iteritems():
			if bigram in health_topics[topic]:
				topic_sum += freq_bi


		data[condition][topic] = topic_sum

		del topic_sum

ap(data)