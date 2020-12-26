#!/usr/bin/python3
#
# This script pulls the data from the meter inputs of the Burk to Google Firestore. 

import requests
from datetime import datetime
import configparser
import os.path
import hashlib
import re
from google.cloud import firestore

# Grab our configuration for the Burk
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

URL_base = config.get('global', 'URL_base')
username = config.get('global', 'username')
password = config.get('global', 'password')

main_page = URL_base + '/index.htm'
logon_page = URL_base + '/login.htm'
# Channeldump is the thing that makes the json data once we login
channel_page = URL_base + '/ChannelDump.cgi'

def grabdata(inputdata):
	with requests.Session() as s:
		# Scrape the nounce from the login page
		nounce = re.findall('var nounce   = (.+)[,;]{1}', s.get(logon_page).text)[0]

		# The below is the 'p' value submitted in the HTTP POST. It's a md5 hash of the nounce + username + password
		pM = hashlib.md5()
		pM.update((nounce + username + password).encode('utf-8'))
		p = pM.hexdigest()

		# Set up our parameters for POSTing to the burk
		login_params = {'login': '', 'u': username, 'p': p}

		# Login to burk itself
		s.post(main_page, data=login_params)
		# Grab the json channels data
		resp2 = s.get(channel_page)

		# Set data to json
		data = resp2.json()

		# Current time needs to be grabbed
		timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		db = firestore.Client()

		# Index 1 is the label, 2 is the numerical value, 3 is units. 
		for item in data['Meters']:
			doc_ref = db.collection(u'meters').document()
			doc_ref.set({
				u'timestamp': timestamp, # TODO: Maybe a better type for this
				u'label': item[1],
				u'value': float(item[2]),
				u'units': item[3]
			})