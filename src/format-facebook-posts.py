import os, itertools, simplejson, demjson
from awesome_print import ap 
from demjson import decode

names_of_pages = open(os.path.join('..','data','inuit-pages'),'rb').read().splitlines()


data = []

for page in names_of_pages:
	for line in open(os.path.join('..','data',page),'rb').read().splitlines():
		data.append(str(line.split(',')[1].split(':')[1].lower()))

with open(os.path.join('..','data','text-of-facebook-posts'),'a') as fid:
	for line in data:
		print>>fid,line.replace('\n','')