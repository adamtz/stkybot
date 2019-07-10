import requests
import json
import random
import os
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

def sendText(text):
	post_params = { "bot_id" : os.getenv('GROUPME_BOT_ID'), "text": text}
	response = requests.post('https://api.groupme.com/v3/bots/post', data = json.dumps(post_params))
	print (response)

def sendText_mention(text, mention_id, mention_name):
	#get info needed for loci
	start = text.find('@')
	end = len(mention_name)+1
	post_params = { "bot_id" : "da00dc41a88e078a5a0c31c6cf", "text": text, "attachments" : [{ "type": "mentions", "user_ids": [str(mention_id)], "loci": [[start,end]] }]}
	headers = {'Content-Type': "application/json"}
	response = requests.post('https://api.groupme.com/v3/bots/post', headers = headers, data = json.dumps(post_params))
	print (response)

def parseMessage(message):
	#check if someone is abusing the bot, if they have an entry in the cache then they hit too many times
	findUser = cache.get(message['name'])
	if findUser is not None:
		sendText_mention("You are using the bot too much, wait 5 seconds", message['user_id'], message['name'])
	else #add all users to this cache so they cant overwhelm the bot
		cache.set(message['name'], timeout = 5)
	if (message['text'] == '!help'):
		to_send = 'List of Commands:\n!mfl:get mfl commands\n!random:get a random number'
		sendText(to_send)
	elif (message['text'] == '!mfl'):
		to_send = 'MFL Stuff: work in progress'
		sendText(to_send)
	elif (message['text'] == '!random'):
		to_send = str(random.randint(1,100))
		print (to_send)
		sendText(to_send)
	elif (message['text'] == 'who is the worst?'):
		mention_id = message['user_id']
		mention_name = message['name']
		#build message to send with the user to mention
		to_send = 'you are @' + mention_name
		sendText_mention(to_send, mention_id, mention_name)
