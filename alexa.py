from getUrls import get_clean_urls, elim_urls, get_closest_snapshot, getDate
import datetime
import json
import os
from pymongo import MongoClient
import re
import requests
from scrape import extract_top_sites, get_description
import socket


#
# def add_current_urls():
#	 """
#	 Assumes an open connection to a populated mongo db. Will add a list of current IPS
#	 associated with every domain.
#	 """

def add_ips_and_location():
	"""
	Assumes an open connection to a populated mongo db. Will add a list of current IPS
	associated with every domain.
	"""
	# get all sites
	sites = col.find({})

	for site in sites:
		url = site['url']
		try:
			ips = socket.gethostbyname_ex(url)[-1]
		except socket.error:
			ips = []

		IPLocations = []
		for ip in ips:
			request_url = 'http://freegeoip.net/json/%s' % ip
			print(request_url)
			r = requests.get(request_url)
			print(r.text)
			IPLocation = json.loads(r.text)
			IPLocation['timestamp'] = datetime.datetime.now()
			IPLocations.append(IPLocation)

		print(IPLocations)

		# now add to databse
		result = col.update_one({'url': url},
						{
						'$set': {
							'currentIP_location': IPLocations
							}
						}
						)


		if result.acknowledged:
			print("added %d ips to url: %s" % (len(ips), url))
		else:
			print("didn't add ips to db, something went wrong!")

def set_descriptions():
	"""
	Assumes an open connection to a populated mongo db. Will make calls to wayback api
	and add a description to every snapshot of every site.
	"""
	# get all sites
	sites = col.find({})

	# counting number of seen sites in loop
	numSITES = 0
	for site in sites:
		# counting number of saved snaps
		snapNUM = 0
		# get closest snap show
		for snap in site['snapshots']:
			# get the closest (urlShot, dateShot (datetime obj))
			closest_mem_shot = get_closest_snapshot(site['url'], snap['dateMementoFormat'])

			# check if url was in the arhive at all
			# closest_snap_shot is int if not in arhive
			inArchive = not isinstance(closest_mem_shot, int)

			if inArchive:
				# if closest snap shot is less than 90 days later or prior to alexa snapshot,
				# we save the header meta tag description from the archived snapshot
				# we do nothing if no valid desc is available.
				delta = closest_mem_shot['date'] - snap['date']
				if abs(delta.days) < 90:
					# use try clause, as sometimes get_description fails due to
					# some weird request business to the api.
					try:
						header_description = get_description(closest_mem_shot['url'])
						# update the snapshot in the database with header_description
						result = col.update_one(
						{'url': site['url'], 'snapshots.date': snap['date']},
						{
							"$set": {'snapshots.$.header_description': header_description }
						}
						)
						# print status
						if result.acknowledged:
							snapNUM += 1
							print("Stored %d valid descs out of %d total descriptions" % (snapNUM, len(site['snapshots'])))
						else:
							print("Failed to store a valid description")
					except:
						print("request failed...")
		# counter
		numSITES += 1
		print("stored descriptions for %d sites...\n" % numSITES)


def initiate_urls_with_snaps():
	"""
	Assumes an open connection to mongo. Will make calls to extract_top_sites,
	and populate an assumed empty collection with url, and list of snapshots: rank, date, mementoDate
	"""
	f = open('newUrls.txt')
	urls = f.readlines()
	f.close()

	# counter of urls considered in loop
	numURLS = 0
	for url in urls:
		# the name of a result file is the date of the snapshot .txt
		dateMementoFormat = re.search('[0-9]+', url).group()
		# get datetime object from date
		dateTimeDate = getDate(dateMementoFormat)

		# get list of topsites
		top_sites = extract_top_sites(url[0:-1], 500)

		# counter of stored topsites
		topNUM = 0
		for dic in top_sites:
			result = col.update_one(
			{'url': dic['url']},
			{ "$addToSet":
				{"snapshots":
					{
					 "rank": dic['rank'],
					 "date": dateTimeDate,
					 "dateMementoFormat": dateMementoFormat
					 }
				}
			},
			upsert=True
			)

			if result.acknowledged:
				topNUM += 1
				print("Stored %d out of %d snapshots... \n" % (topNUM, len(top_sites)))
			else:
				print("Failed to store site")
		# counter
		numURLS += 1
		print("Gone through %d out of %d URLS... \n" % (numURLS, len(urls)))


client = MongoClient()
db = client.alexaDB
col = db.sites


# get urls from memento and save to urls.txt
#get_clean_urls()
# decide the min time interval in days between snapshots
# elim_urls(90)
# scrape first url


# print("deleted everything")
# # fresh start
# col.delete_many({})
#
# print("======= GET TOPSITES =======\n")
# # get all topsites and their snapshots
# initiate_urls_with_snaps()

print("==== test print out ====")
cursor = col.find({})

for p in cursor:
	print(p)

print("==== about to add ips ====")
add_ips_and_location()
#
# print("======= GET DESCRIPTIONS =======\n")
# # update snapshots with descriptions (heavy operation)
# set_descriptions()


# col.delete_many({})


# # change working dir to save results in right folder
# os.chdir("ranking_files")


print("now test if can collect from mongo\n\n")

print("calling find({})")
cursor = col.find({})

for p in cursor:
	print(p)

print("looking for google")
cursor = col.find({"url": "google.com"})

for p in cursor:
	print (p)

client.close()

	# # open a file named the date of the alexa snapshot.txt
	# q = open(str(date)+".txt", 'w')
	#
	# # now in each topsite add the historical description from the meta tag
	# for tup in top_sites:
	#	 # get historical description
	#	 histo_header_desc = getDescription(tup)
	#	 print("description!!:::::::::::\n")
	#	 print(histo_header_desc)
	#
	#	 # write tuples in CSV format to file
	#	 toWrite = str(tup[0]) + "," + tup[1] + "," + histo_header_desc + "\n"
	#	 print(toWrite)
	#	 q.write(toWrite)
	#
	# # remember to close file
	# q.close()
	# print('wrote another result to file \n')
