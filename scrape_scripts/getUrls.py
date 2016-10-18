import re
import requests
from datetime import datetime
import json

def getDate(line):
	"""
	takes string, gets the date embedded in it, returns datetime obj
	"""
	# get the date in url
	m = re.search('[0-9]+',line)
	longInt = m.group()
	year = str(longInt[0:4])
	month = str(longInt[4:6])
	day = str(longInt[6:8])
	date = datetime.strptime(year+ "-" + month+ "-" + day, '%Y-%m-%d')
	return date


def get_closest_snapshot(url, date):
	"""
	Takes a URL and a date (integer arhive format), returns a dict where url is
	the archieved formatted url, and date is the date of the closest snapshot to the given date.
	"""
	# use internet arhieve API
	apiUrl = "http://archive.org/wayback/"


	# create the url to be requested
	apiUrl += "available?url=" + url + "&timestamp=" + date

	# convert to string
	jsonData = requests.get(apiUrl).text

	# convert to python dict
	pythonData = json.loads(jsonData)

	# get date and url
	try:
		dateShot = pythonData["archived_snapshots"]["closest"]["timestamp"]
		urlShot = pythonData["archived_snapshots"]["closest"]["url"]
	except:
		print("URL not available in archive\n")
		return -1
	# turn dateShot into a datetime obj
	try:
		dateShot = getDate(dateShot)
	except:
		# date from wayback API is corrupt, so we choose a really old date
		# to avoid this description from being included
		dateShot = getDate("19931202")

	toReturn = {"url": urlShot, "date": dateShot}

	return toReturn

def get_clean_urls():
	"""
	Assumes that you already has a topsites.txt from memento.
	The function strips the urls from web.archive and saves them to urls.txt
	"""
	#open file of top sites
	f = open('topsites.txt', 'r')
	lines = f.readlines()
	urls = []
	for line in lines:
		# currently, I only care about web.archieve.org
		if ("web.archive.org" in line):
			#strip to url
			url = (re.split(';', line)[0][1:-1])
			#get index before alexa url
			try:
				index = url[1:].index('http://')
			except:
				continue
			#insert id_ string in url to retrieve minimal site
			url = url[:index] + "id_" + url[index:]
			# get http status of link
			status = requests.get(url).status_code
			# if ok, append to list of links
			if status == 200:
				urls.append(url + "\n")
				print("url is fine!")

	q = open('urls.txt', 'w')
	q.writelines(urls)

	# remember to close files (maybe not super important in python :> )
	q.close()
	f.close()

	print("saved %d valid urls to urls.txt " % len(urls))
	return 0

def elim_urls(interVal=30):
	"""
	open urls.txt, clean out urls according to interVal (1 month by default), and save to newUrls.txt
	"""
	f = open('urls.txt')
	lines = f.readlines()

	# associate date object with url
	urlDates = []
	for line in lines:
		# make datetime object out date in url
		date = getDate(line)

		# append this tuple (url, date) to the list
		urlDates.append((line, date))

	# only save url if date difference is greater than 3 months
	urlsToSave = [urlDates[0][0]]

	# The following algorithm only saves a url if
	# its date is at least 3 months (90 days) post the previously saved url
	i = 1
	k = 1
	while (i<len(urlDates)):
		delta = urlDates[i][1] - urlDates[i-k][1]
		if ((delta.days / interVal) >= 1):
			urlsToSave.append(str(urlDates[i][0]))
			k = 1
		else:
			k += 1
		i += 1

	# create new file with these cleaned urls
	q = open('newUrls.txt', 'w')
	q.writelines(urlsToSave)
	q.close()
	f.close()
