import requests
import time
import os
import json
from flask import Flask
from gg_commands import *

gg = Flask(__name__)

@gg.route('/', methods=['POST'])
def webhook():
	data = requests.get_json()

	# We don't want to reply to ourselves!
	if data['name'] != os.getenv('BOT_NAME'):
		msg = '{}, you sent "{}".'.format(data['name'], data['text'])
		sendText(msg)

	return "ok", 200
# request_params = {'token': 'wxWNTxmaK2OeSbcyLJNxchFnfQJWe09897S3kyJ6'}
# while True:
	# response = requests.get('https://api.groupme.com/v3/groups/51526137/messages', params = request_params)
	# if (response.status_code == 200):
		# response_messages = response.json()['response']['messages']
		# for message in response_messages:
			#first ignore messages from the bot_id
			# if (message['name'] == 'StickyBot'):
				# break
			#parse messages for responses
			# parseMessage(message)
			# request_params['since_id'] = message['id']
	# print 'looping'
	# time.sleep(2)