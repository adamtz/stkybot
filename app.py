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
	# We don't want to reply to ourselves!
	if data['name'] != os.getenv('BOT_NAME') and "!" in data['text'][0]:
		parseMessage(data)
	return "ok", 200