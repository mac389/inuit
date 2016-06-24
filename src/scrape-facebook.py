import facebook, requests, json 



tokens = json.load(open('../tokens.json','rb'))
APP_ID = tokens['id']
APP_SECRET = tokens['secret'] 
ACCESS_TOKEN = tokens['long_access_token']

"""
A simple example script to get all posts on a user's timeline.
Originally created by Mitchell Stewart.
<https://gist.github.com/mylsb/10294040>
"""


def action(post):
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    print(posts)


# You'll need an access token here to do anything.  You can get a temporary one
# here: https://developers.facebook.com/tools/explorer/
# Look at Bill Gates's profile for this example by using his Facebook id.

pages = open('../data/inuit-pages').read().splitlines()
graph = facebook.GraphAPI(ACCESS_TOKEN)

for page in pages:
	profile = graph.get_object(page)
	posts = graph.get_connections(profile['id'],'posts')

	while True:
		with open('../data/%s'%page,'a') as fid:
		    try:
		        # Perform some action on each post in the collection we receive from
		        # Facebook.
		        for post in posts['data']:
		        	print>>fid,post
		        posts = requests.get(posts['paging']['next']).json()
		    except KeyError:
		        # When there are no more pages (['paging']['next']), break from the
		        # loop and end the script.
		        break
