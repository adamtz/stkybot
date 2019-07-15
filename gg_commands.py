import requests
import json
import random
import os
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

def getOTC():
	print ("otc")
	otc_info = getOTCInfo_MFL()
	#match franchiseid to team name
	otc_franchise = franchiseMatch(otc_info["franchise"])
	members_list = getMembers()
	matchMembers(members_list, otc_franchise)

def franchiseMatch(franchiseId):
	try:
		#attempt to get the list of franchise names from the cache, its not cached go and get it from MFL
		franchise_list = cache.get("franchises")
		if franchise_list is None:
			franchise_list = getFranchiseInfo_MFL()
			cache.set("franchises", franchise_list)
		for franchise in franchise_list:
			if (str(franchise["id"]) == str(franchiseId)):
				return franchise["name"]
	except Exception as e:
		print ("Error in doing franchise match: " + str(e))

def getFranchiseInfo_MFL():
	mflJar = loginHELPER("stickyz", os.getenv('USER_PASS'))
	try:
		url = "http://www65.myfantasyleague.com/2019/export?TYPE=league&" + os.getenv'LEAGUEID' + "&JSON=1"
		#UPDATE TO CORRECT WEEK AND URL FOR LEAGUE
		response = requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			results = data["league"]["franchises"]["franchise"]
			franchise_list = []
			for franchise in results:
				franchise_info = {"id" : franchise["id"], "name" : franchise["name"]}
				franchise_list.append(franchise_info)
			return franchise_list
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting getting franchise info from mfl: " + str(e))

def getOTCInfo_MFL():
	mflJar = loginHELPER("stickyz", os.getenv('USER_PASS'))
	try:
		url = "http://www65.myfantasyleague.com/2019/export?TYPE=draftResults&" + os.getenv'LEAGUEID' + "&JSON=1"
		#UPDATE TO CORRECT WEEK AND URL FOR LEAGUE
		response = requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			results = data["draftResults"]["draftUnit"]["draftPick"]
			otc_info = next((item for item in results if item["player"] == ""), False)
			return otc_info
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting getting OTC: " + str(e))

def getDraftInfo_MFL():
	mflJar = loginHELPER("stickyz", os.getenv('USER_PASS'))
	try:
		url = "http://www65.myfantasyleague.com/2019/export?TYPE=draftResults&" + os.getenv'LEAGUEID' + "&JSON=1"
		#UPDATE TO CORRECT WEEK AND URL FOR LEAGUE
		response = requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			#get otc info first
			results = data["draftResults"]["draftUnit"]["draftPick"]
			draft_info = next((item for item in results if item["player"] == ""), False)
			otc_team = franchiseMatch(draft_info["franchise"])
			#get current pick and round
			draft_info_str = "Draft is in round: " + draft_info["round"] + ", pick: " + draft_info["pick"] + ". Waiting for: " + otc_team
			return draft_info_str
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting draft info: " + str(e))

def loginHELPER(username, password):
	response = requests.get("https://api.myfantasyleague.com/2019/login?USERNAME=" + username + "&PASSWORD=" + password + "&XML=1")
	#data= json.loads(response.text)
	jar = response.cookies
	mfl_id = jar.get("MFL_USER_ID")
	return  jar

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
		if franchise in member["nickname"]:
			text = "@" + franchise + " is OTC"
			sendText_mention(text,member["user_id"],member["nickname"])
			return True
		else:
			text = franchise + " is OTC but a mention match was not found, franchise names and groupme names need to match"
	sendText(text)

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
		to_send = 'MFL Stuff::\n!otc:See who is OTC\n!draft:Get draft info\n!bylaws:Get Link for Bylaws'
		sendText(to_send)
	elif (message['text'] == '!otc'):
		getOTC()
		#sendText("whoever is otc better be picking!")
	elif (message['text'] == '!draft'):
		draft_info = getDraftInfo_MFL()
		sendText(draft_info)
	elif (message['text'] == '!bylaws'):
		to_send = 'https://docs.google.com/document/d/1kH6CBfGpBkCsiWCzGh5D-iri7cXKwzGIapIXdaMUyNw/edit?usp=sharing'
		sendText("On the MFL Site")
	elif (message['text'] == '!drew'):
		to_send = 'Drew, Start the draft please'
		sendText(to_send)
	elif (message['text'] == '!wakeup'):
		to_send = "Bleeep Bloop.....I'm up!"
		sendText(to_send)
	elif (message['text'] == '!sticky'):
		to_send = "Sticky is the man, he is a god among men"
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
