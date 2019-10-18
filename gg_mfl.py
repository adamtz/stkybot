import requests
import json
import os
from datetime import datetime, timedelta, date

LeagueID = os.getenv('LEAGUEID')

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

def getLiveScoring_MFL():
	mflJar = loginHELPER("stickyz", os.getenv('USER_PASS'))
	week = weekHelper()
	try:
		url = "http://www67.myfantasyleague.com/2019/export?TYPE=liveScoring&L=" + LeagueID + "&APIKEY=&W="+ week + "&DETAILS=&JSON=1"		#UPDATE TO CORRECT WEEK AND URL FOR LEAGUE
		response = requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			if "matchup" in data["liveScoring"].keys():
				franchise_list = getFranchiseInfo_MFL()
				matchups = data["liveScoring"]["matchup"]
				lineup_info = ""
				for matchup in matchups:
					franchises = matchup["franchise"]
					score1 = float(franchises[0]["score"])
					team1 = list(filter(lambda team: team['id'] == franchises[0]["id"], franchise_list))[0]["name"]
					score2 = float(franchises[1]["score"])
					team2 = list(filter(lambda team: team['id'] == franchises[1]["id"], franchise_list))[0]["name"]
					lineup_info= "{}{} vs {} : {} to {}\n".format(lineup_info, team1, team2, score1, score2)
			else:
				lineup_info = "No matchups"
			return lineup_info
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting getting live scoring info: " + str(e))

def getStandings_MFL():
	mflJar = loginHELPER("stickyz", os.getenv('USER_PASS'))
	week = weekHelper()
	try:
		url = "http://www67.myfantasyleague.com/2019/export?TYPE=leagueStandings&L=" + LeagueID + "&APIKEY=&W="+ week + "&DETAILS=&JSON=1"		#UPDATE TO CORRECT WEEK AND URL FOR LEAGUE
		response = requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			standings_list = data["leagueStandings"]["franchise"]
			standings_info = "League Standings:\n"
			franchise_list = getFranchiseInfo_MFL()
			for franchise in standings_list:
				teamName = list(filter(lambda team: team['id'] == franchise["id"], franchise_list))[0]["name"]
				wins = franchise["h2hw"]
				losses = franchise["h2hl"]
				pf = franchise["pf"]
				power = franchise["pwr"]
				standings_info = "{}{}: {}-{} PF:{} PWR:{}\n".format(standings_info, teamName, wins, losses, pf, power)
			return standings_info
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting getting standings info: " + str(e))

def getPicks_MFL():
	mflJar = loginHELPER("stickyz", os.getenv('USER_PASS'))
	try:
		url = "http://www67.myfantasyleague.com/2019/export?TYPE=futureDraftPicks&L=" + LeagueID + "&APIKEY=&JSON=1"
		response = requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			data= json.loads(response.text)
			picks_list = data["futureDraftPicks"]["franchise"]
			picks_info = "League Picks:\n"
			franchise_list = getFranchiseInfo_MFL()
			for franchise in picks_list:
				teamName = list(filter(lambda team: team['id'] == franchise["id"], franchise_list))[0]["name"]
				future_picks_list = franchise["futureDraftPick"]
				future_pick_info = ""
				#handle 1 pick or no picks
				if type(future_picks_list) == list:
					for future_pick in future_picks_list:
						future_pick_info = "{}Rd{},".format(future_pick_info,future_pick["round"])
					future_pick_info = future_pick_info[:-1]
				elif type(future_picks_list) == dict:
						future_pick_info = "{}Rd{},".format(future_pick_info,future_picks_list["round"])
						future_pick_info = future_pick_info[:-1]
				else:
					#no picks
					future_pick_info = "{}:Do Not Pass Go".format(future_pick_info,"0")
				
				picks_info = "{}{}: {}\n".format(picks_info,teamName, future_pick_info)
			return picks_info
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting getting picks info: " + str(e))

def getSurvivor_MFL():
	mflJar = loginHELPER("stickyz", os.getenv('USER_PASS'))
	#week has to be an int here for getting the right week on the array of weeks from mfl
	week = int(weekHelper())
	print ("week is: " + str(week))
	try:
		url = "http://www67.myfantasyleague.com/2019/export?TYPE=survivorPool&L=" + LeagueID + "&APIKEY=&JSON=1"
		response = requests.get(url,cookies=mflJar)
		if response.status_code == 200:
			franchise_list = getFranchiseInfo_MFL()
			data= json.loads(response.text)
			survivor_list = data["survivorPool"]["franchise"]
			survivor_info = ""
			for franchise in survivor_list:
				teamName = list(filter(lambda team: team['id'] == franchise["id"], franchise_list))[0]["name"]
				franchise_info = franchise["week"]
				this_week = franchise_info[week-1]
				if "pick" in this_week.keys() and this_week["pick"] != "" :
					pick = this_week["pick"]
				else:
					pick = "Dead"
				survivor_info = "{}{}: {}\n".format(survivor_info,teamName, pick)
			return survivor_info
		else:
			print ("request to mfl failed")
	except Exception as e:
		print ("Error in getting getting survivor info: " + str(e))
		return ("No Survivor")

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

def doBBall():
	week = weekHelper()
	print ("doing the thing for week: " + week)
	url = "https://stickypi.herokuapp.com/run/" + week + "/"
	try:
		response = requests.get(url, timeout=3)
	except:
		return "Doing the thing, might take us a second"

def do4YP():
	url = "https://stickypi.herokuapp.com/4yp/standings/"
	try:
		response = requests.get(url)
		print (response.text)
		return response.text
	except:
		return "Error Getting Standings"

def weekHelper():
	d1 = date(2019, 9, 3)
	d2 = date.today()
	wk1tue = (d1 - timedelta(days=d1.weekday()))
	thiswktue = d2 - timedelta(days=(d2.weekday())+1)
	week = ((thiswktue - wk1tue).days / 7)
	today = date.today().weekday()
	#if today is sunday/monday/tuesday/wednesday keep on previous week stuff else do the current week
	if today <= 2:
		week = week + 1
	else:
		week = week + 2
	return str(int(float(week)))
