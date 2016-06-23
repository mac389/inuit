import requests, json 


tokens = json.load(open('tokens.json','rb'))
APP_ID = tokens['id']
APP_SECRET = tokens['secret'] 
ACCESS_TOKEN = tokens['long_access_token']

base = 'http://graph.facebook/com'

payload = {''}
r = requsts.get(base,payload)
