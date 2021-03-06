import requests
import time
import os
import json
import datetime
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
	if status == "used" and message['user_id'] != "27293802":
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
	elif (message['text'] == '!scoring' or message['text'] == '!live'):
		scoring()
	elif (message['text'] == '!standings' or message['text'] == '!ranks'):
		standings()
	elif (message['text'] == '!picks' or message['text'] == '!draftpicks'):
		picks()
	elif (message['text'] == '!days'):
		days()
	elif (message['text'] == '!faab' or message['text'] == '!bucks' or message['text'] == '!DLBucks' or message['text'] == '!dlBucks' or message['text'] == '!dlBucks' or message['text'] == '!dlbucks'):
		dlBucks()
	elif (message['text'] == '!dice' or message['text'] == '!rolls' or message['text'] == '!getrolls'):
		dl3_dice()
	elif (message['text'] == '!dobucks' or message['text'] == '!DL3'):
		if message['user_id'] == "6739678":
			to_send = "Running Bucks Update"
			sendText(to_send)
			dl3_run()
	elif (message['text'] == '!dothething' or message['text'] == '!bestball'):
		if message['user_id'] == "6739678" or message['user_id'] == "27293802":
			bball()
		else:
			to_send = "No BestBall for you!"
			sendText(to_send)
			to_send = "https://thumbs.gfycat.com/UnknownAdorableBuzzard-size_restricted.gif"
			sendText(to_send)
	elif (message['text'] == '!survivor'):
		today = date.today().weekday()
		print (today)
		if today != 1 and today != 2:
			survivor()
		else:
			to_send = "Check back later in the week"
			sendText(to_send)
	elif (message['text'] == '!wakeup'):
		to_send = "Bleeep Bloop.....I'm up!"
		sendText(to_send)
	elif (message['text'] == '!sticky'):
		to_send = "Sticky is the man, he is a god among men"
		sendText(to_send)
	elif (message['text'] == '!keeperinfo' or message['text'] == '!keepershit' ):
		to_send = "Players dropped: Top 10 QBs, Top 20 RBs, Top 30 WRs, Top 10 TEs, Top 10 IDLs, Top 20 EDGE, Top 20 LBs, Top 10 CBs, Top 20 S"
		sendText(to_send)
	elif (message['text'] == '!4yp' or message['text'] == '!yp'):
		fourYP()
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
	elif (message['text'] == '!goose'):
		to_send = "The Goose is loose"
		sendText(to_send)
	elif (message['text'] == '!brent'):
		to_send = "Again?"
		sendText(to_send)
	elif (message['text'] == '!badbot'):
		to_send = "I remember"
		sendText(to_send)
	elif (message['text'] == '!santi'):
		to_send = "Staten Island Proud"
		sendText(to_send)
	elif (message['text'] == '!luke'):
		to_send = "From Canada, With Love."
		sendText(to_send)
	elif (message['text'] == '!drew'):
		to_send = "Go Broncos!"
		sendText(to_send)
	elif (message['text'] == '!knotts'):
		to_send = "I may be 99% code but I know that Knotts is the real worst"
		sendText(to_send)
	elif (message['text'] == '!wife'):
		to_send = "No Pants, No Problem"
		sendText(to_send)
	elif (message['text'] == '!donotpassgo'):
		to_send = "DO NOT PASS GO, DO NOT COLLECT 200 DOLLARS: https://www.youtube.com/watch?v=Cj1wcs7SZj0"
		sendText(to_send)
	elif (message['text'] == '!rip'):
		to_send = "Rest In Pepperoni"
		sendText(to_send)