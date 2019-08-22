import requests
import json

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
		url = "http://www65.myfantasyleague.com/2019/export?TYPE=league&L="+ LeagueID +"&JSON=1"
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

def getLineupInfo_MFL():
	mflJar = loginHELPER("stickyz", os.getenv('USER_PASS'))
	try:
		url = "http://www65.myfantasyleague.com/2019/export?TYPE=league&L=" + LeagueID + "&JSON=1"
		#UPDATE TO CORRECT WEEK AND URL FOR LEAGUE
		response = requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			results = results = data["league"]["starters"]
			count = results["count"]
			idp_count = results["idp_starters"]
			starters_list  = results["position"]
			if idp_count is None or idp_count == "" or not idp_count:
				lineup_info = "Total Starters: " + count
			else:
				lineup_info = "Total Starters: " + count + ", IDP Total: " + idp_count
			for position in starters_list:
				lineup_info = lineup_info + ", " + position["limit"] + position["name"]
			return lineup_info
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting getting lineup info: " + str(e))

def getOTCInfo_MFL():
	mflJar = loginHELPER("stickyz", os.getenv('USER_PASS'))
	try:
		url = "http://www65.myfantasyleague.com/2019/export?TYPE=draftResults&L=" + LeagueID + "&JSON=1"
		#UPDATE TO CORRECT WEEK AND URL FOR LEAGUE
		response = requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			results = data["draftResults"]["draftUnit"]["draftPick"]
			otc_info = next((item for item in results if item["player"] == ""), False)
			return otc_info
		else:
			print ("request to otc mfl failed")
	except Exception as e:
		print ("Error in getting getting OTC: " + str(e))

def getDraftInfo_MFL():
	mflJar = loginHELPER("stickyz", os.getenv('USER_PASS'))
	try:
		url = "http://www65.myfantasyleague.com/2019/export?TYPE=draftResults&L=" + LeagueID + "&JSON=1"
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
			print ("request to draft mfl failed")
			return ("Draft Not Started or This code is broken")
	except Exception as e:
		print ("Error in getting draft info: " + str(e))

def getDLBucks_MFL():
	mflJar = loginHELPER("stickyz", os.getenv('USER_PASS'))
	try:
		url = "https://www67.myfantasyleague.com/2019/export?TYPE=league&L=" + LeagueID + "&JSON=1"
		response = requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			#loop through teams to get current bb and franchise info
			franchises = data["league"]["franchises"]["franchise"]
			DLBucks_info = ""
			for franchise in franchises:
				DLBucks_info = "{}{} : {}\n".format(DLBucks_info, franchise["name"],franchise["bbidAvailableBalance"])
			return DLBucks_info
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting BB: " + str(e))

def loginHELPER(username, password):
	response = requests.get("https://api.myfantasyleague.com/2019/login?USERNAME=" + username + "&PASSWORD=" + password + "&XML=1")
	#data= json.loads(response.text)
	jar = response.cookies
	mfl_id = jar.get("MFL_USER_ID")
	return  jar

