# -*- coding: utf-8 -*-
import requests
import random
import os
import json
from werkzeug.contrib.cache import SimpleCache
from gg_mfl import *

cache = SimpleCache()
LeagueID = os.getenv('LEAGUEID')
mflLeagues = ["55825", "31432", "24928"]

def sendText(text):
	post_params = { "bot_id" : os.getenv('GROUPME_BOT_ID'), "text": text}
	response = requests.post('https://api.groupme.com/v3/bots/post', data = json.dumps(post_params))
	print (response)

def sendText_mention(text, mention_id, mention_name):
	#get info needed for loci. Loci is the starting position and end length of the mention. So it needs to calculate where the @ symbol is and how long the mention is so it can place the tag
	start = text.find('@')
	end = len(mention_name)+1
	post_params = { "bot_id" : os.getenv('GROUPME_BOT_ID'), "text": text, "attachments" : [{ "type": "mentions", "user_ids": [str(mention_id)], "loci": [[start,end]] }]}
	headers = {'Content-Type': "application/json"}
	response = requests.post('https://api.groupme.com/v3/bots/post', headers = headers, data = json.dumps(post_params))
	print (response)

def getOTC():
	try:
		print ("otc")
		otc_info = getOTCInfo_MFL()
		#match franchiseid to team name
		otc_franchise = franchiseMatch(otc_info["franchise"])
		members_list = getMembers()
		matchMembers(members_list, otc_franchise)
	except Exception as e:
		print ("Error in getting OTC: " + str(e))
		return False

def getMembers():
	#get members first by getting member lists
	url = "https://api.groupme.com/v3/groups/"+os.getenv('GROUP_ID')
	headers = {"Content-Type" : "application/json", "X-Access-Token" : os.getenv('BOT_TOKEN')}
	response = requests.get(url, headers = headers)
	data= json.loads(response.text)
	members_list = data["response"]["members"]
	return members_list

def matchMembers(members_list, franchise):
	#match franchise OTC to list of members, if not found just return franchise for printing
	#searches for exact match or name in, may need dirty matching on @symbol or something else like that depending on the league
	for member in members_list:
		if franchise in member["nickname"] or member["nickname"].upper().find(franchise.upper()) >= 0:
			text = "@" + franchise + " is OTC"
			sendText_mention(text,member["user_id"],member["nickname"])
			return True
		else:
			text = franchise + " is OTC but a mention match was not found, franchise names and groupme names need to match"
	sendText(text)

def help():
	if LeagueID == "1":
		to_send = 'List of Commands:\n!mfl:get mfl commands\n!random:get a random number\n!woat:find out who the worst is\n!keepershit:find out keeper info\n!yp:find out YP stuff\n!lineups:find out starting lineups'
	else:
		to_send = 'List of Commands:\n!mfl:get mfl commands\n!random:get a random number\n!woat:find out who the worst is'
	sendText(to_send)

def mfl():
	if LeagueID == "1":
		to_send = 'MFL Stuff::\n!otc:See who is OTC\n!draft:Get draft info\n!bylaws:Get Link for Bylaws\n!lineup:Get Lineup Info'
	elif LeagueID == "55825":
		to_send = 'MFL Stuff::\n!dlBucks:Get Current DL Bucks\n!bylaws:Get Link for Bylaws\n!lineup:Get Lineup Info\n!scoring:Get Current Scoring\n!standings:Get Current Standings\n!picks:Get Current Picks\n!Survivor:Get Current Survivor'
	else:
		to_send = 'MFL Stuff::\n!otc:See who is OTC\n!draft:Get draft info\n!bylaws:Get Link for Bylaws\n!lineup:Get Lineup Info\n!scoring:Get Current Scoring\n!standings:Get Current Standings\n!picks:Get Current Picks'
	sendText(to_send)

def otc():
	bool = getOTC()
	if bool is False:
		sendText("whoever is otc better be picking!")
	else:
		sendText(bool)
	#sendText("whoever is otc better be picking!")

def draft():
	if LeagueID in mflLeagues:
		to_send = getDraftInfo_MFL()
	else:
		to_send = 'Draft Order::\n#1-Drew - Hand That Feeds\n#2-Wife - Always Half-Naked\n#3-Sean - Somebodys Baking Brownies\n#4-Czar - Czarry to Bother You\n#5-Ben - The Other Ben\n#6-Ryan - Team Trash Pandas\n#7-Bill - Trauma Llamas\n#8-Devin - D101 Expert\n#9-Kevin - This Fucking Guy\n#10-StickyZ - Eww… so sticky\n#11-Corey - thēDRÎ₽ćhrøñićłēš\n#12-Alex - Dawkin Donuts\n#13-Fallen - Drew Help\n#14-Luke - Fucking Canadian' 
	sendText(to_send)

def bylaws():
	if LeagueID == "31432":
		to_send = "On the MFL Site"
	elif LeagueID == "55825":
		to_send = "https://docs.google.com/document/d/14hFpzUFHm7VFeNXEQ4NydbYqAoSML2gR-PpYHdo-Qh0/view"
	elif LeagueID == "1":
		to_send = 'https://docs.google.com/document/d/1kH6CBfGpBkCsiWCzGh5D-iri7cXKwzGIapIXdaMUyNw/edit?usp=sharing'
	else:
		to_send = 'Not Found'
	sendText(to_send)

def lineups():
	if LeagueID == "1":
		to_send = '1QB, 2RB, 3WR, 1TE, 1SFLEX, 1FLEX, 2IDL, 3EDGE, 3LB, 3CB, 2S, 1DFLEX'
	elif LeagueID in mflLeagues:
		to_send = getLineupInfo_MFL()
	else:
		to_send	= 'lineup info not found'
	sendText(to_send + ". See !Bylaws For More Info")

def scoring():
	if LeagueID in mflLeagues:
		to_send = getLiveScoring_MFL()
	elif LeagueID == "1":
		to_send = do4YP_Scoring()
	else:
		to_send	= 'scoring info not found'
	sendText(to_send)

def standings():
	if LeagueID in mflLeagues:
		to_send = getStandings_MFL()
	elif LeagueID == "1":
		to_send = do4YP_Standings()
	else:
		to_send	= 'standings info not found'
	sendText(to_send)

def dlBucks():
	to_send = getDLBucks_MFL()
	sendText(to_send)

def picks():
	if LeagueID in mflLeagues:
		to_send = getPicks_MFL()
	else:
		to_send	= 'Picks not found'
	sendText(to_send)

def days():
	to_send = getDays()
	sendText(to_send)

def survivor():
	if LeagueID == "55825":
		to_send = getSurvivor_MFL()
	else:
		to_send	= 'No Survivor'
	sendText(to_send)

def bball():
	if LeagueID == "31432":
		to_send = doBBall()
	else:
		to_send = "Not in use"
	sendText(to_send)

def fourYP():
	if LeagueID == "1":
		to_send = do4YP()
	else:
		to_send = "Not in use"
	sendText(to_send)

def dl3_run():
	if LeagueID == "55825":
		to_send = doDL3_run()
	else:
		to_send = "Not in use"
	sendText(to_send)

def dl3_dice():
	if LeagueID == "55825":
		to_send = doDL3_dice()
	else:
		to_send = "Not in use"
	sendText(to_send)

def woat(message):
	mention_id = message['user_id']
	mention_name = message['name']
	#build message to send with the user to mention
	to_send = 'you are the worst @' + mention_name
	sendText_mention(to_send, mention_id, mention_name)
