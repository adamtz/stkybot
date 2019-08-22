import requests
import time
import os
import json
from flask import Flask, request
from gg_commands import *

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	#we don't want to reply to ourselves!
	if data['name'] != os.getenv('BOT_NAME') and "!" in data['text'][0]:
		parseMessage(data)
	return "ok", 200

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

def runCommands(message):
	if (message['text'] == '!help'):
		help()
	elif (message['text'] == '!mfl'):
		mfl()
	elif (message['text'] == '!otc'):
		otc()
	elif (message['text'] == '!draft'):
		draft()
	elif (message['text'] == '!bylaws' or message['text'] == '!bylaw' ):
		bylaws()
	elif (message['text'] == '!lineups' or message['text'] == '!lineup'):
		lineups()
	elif (message['text'] == '!faab' or message['text'] == '!bucks' or message['text'] == '!DLBucks' or message['text'] == '!dlbucks'):
		dlBucks()
	elif (message['text'] == '!wakeup'):
		to_send = "Bleeep Bloop.....I'm up!"
		sendText(to_send)
	elif (message['text'] == '!sticky'):
		to_send = "Sticky is the man, he is a god among men"
		sendText(to_send)
	elif (message['text'] == '!keeperinfo' or message['text'] == '!keepershit' ):
		to_send = "Players dropped: Top 10 QBs, Top 20 RBs, Top 30 WRs, Top 10 TEs, Top 10 IDLs, Top 20 EDGE, Top 20 LBs, Top 10 CBs, Top 20 S"
		sendText(to_send)
	elif (message['text'] == '!goodbot'):
		mention_id = message['user_id']
		mention_name = message['name']
		#build message to send with the user to mention
		to_send = 'Thank you @'+ mention_name +', you are a good water filled flesh bag...err I mean Human'
		sendText_mention(to_send, mention_id, mention_name)
	elif (message['text'] == '!random'):
		to_send = str(random.randint(1,100))
		sendText(to_send)
	elif (message['text'] == '!woat'):
		woat(message)