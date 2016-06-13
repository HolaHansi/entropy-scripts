import re
import requests

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
			# url = url[:index] + "id_" + url[index:]
			# get http status of link
			status = requests.get(url).status_code
			# if ok, append to list of links 
			if status == 200:
				urls.append(url + "\n")
				print("url is fine!")

	q = open('urls.txt', 'w')
	q.writelines(urls)

	# remember to close files (maybe not super important in python :> )
	close(q)
	close(f)

	print("saved %d valid urls to urls.txt ", len(urls))
	return 0


