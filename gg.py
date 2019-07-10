import requests
import time
from gg_commands import *

request_params = {'token': 'wxWNTxmaK2OeSbcyLJNxchFnfQJWe09897S3kyJ6'}
while True:
	response = requests.get('https://api.groupme.com/v3/groups/51526137/messages', params = request_params)
	if (response.status_code == 200):
		response_messages = response.json()['response']['messages']
		for message in response_messages:
			#first ignore messages from the bot_id
			if (message['name'] == 'StickyBot'):
				break
			#parse messages for responses
			parseMessage(message)
			request_params['since_id'] = message['id']
	print 'looping'
	time.sleep(3)