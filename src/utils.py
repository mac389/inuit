import operator

def sort(dictionary,reverse=True):
	return sorted(dictionary.items(),key=operator.itemgetter(1),reverse=reverse)