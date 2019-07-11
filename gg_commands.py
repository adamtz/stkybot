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
	post_params = { "bot_id" : os.getenv('GROUPME_BOT_ID'), "text": text, "attachments" : [{ "type": "mentions", "user_ids": [str(mention_id)], "loci": [[start,end]] }]}
	headers = {'Content-Type': "application/json"}
	response = requests.post('https://api.groupme.com/v3/bots/post', headers = headers, data = json.dumps(post_params))
	print (response)

def runCommands(message):
	if (message['text'] == '!help'):
		to_send = 'List of Commands:\n!mfl:get mfl commands\n!random:get a random number\n!woat:find out who the worst is'
		sendText(to_send)
	elif (message['text'] == '!mfl'):
		to_send = 'MFL Stuff::\n!otc:See who is OTC(not working)\n!draft:Get draft info\n!bylaws:Get Link for Bylaws'
		sendText(to_send)
	elif (message['text'] == '!otc'):
		to_send = 'Whoever is on the clock better pick...or else'
		sendText(to_send)
	elif (message['text'] == '!draft'):
		#draft_info = getDraftInfo()
		sendText("Draft Has Not Started Yet")
	elif (message['text'] == '!bylaws'):
		to_send = 'https://docs.google.com/document/d/1kH6CBfGpBkCsiWCzGh5D-iri7cXKwzGIapIXdaMUyNw/edit?usp=sharing'
		sendText(to_send)
	elif (message['text'] == '!drew'):
		to_send = 'Drew, Start the draft please'
		sendText(to_send)
	elif (message['text'] == '!wakeup'):
		to_send = "Bleeep Bloop.....I'm up!"
		sendText(to_send)
	elif (message['text'] == '!random'):
		to_send = str(random.randint(1,100))
		sendText(to_send)
	elif (message['text'] == '!woat'):
		mention_id = message['user_id']
		mention_name = message['name']
			#build message to send with the user to mention
		to_send = 'you are the worst @' + mention_name
		sendText_mention(to_send, mention_id, mention_name)

def parseMessage(message):
	#check if someone is abusing the bot, if they have an entry in the cache then they hit too many times
	status = cache.get(message['name'])
	if status == "used":
		print ("banning: " + message['name'])
		#delete from cache first so we can update the timeout via set
		cache.delete(message['name'])
		cache.set(message['name'], "banned", timeout = 30)
		sendText_mention("@" + message['name']+ " ,you are using the bot too much, no bot for you for 30 seconds", message['user_id'], message['name'])
	elif status == "banned":
		print ("ignoring commands from: " + message['name'])
		return None
	else:
		#add all users to this cache so they cant overwhelm the bot
		cache.delete(message['name'])
		cache.set(message['name'], "used", timeout = 6)
		#run the commands
		runCommands(message)
