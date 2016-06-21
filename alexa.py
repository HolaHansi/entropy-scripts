from getUrls import get_clean_urls, elim_urls, get_closest_snapshot, getDate
import os
import re
from scrape import extract_top_sites, get_description


# make a dir for the data files
os.makedirs("ranking_files")


# get urls from memento and save to urls.txt
#get_clean_urls()
# decide the min time interval in days between snapshots
elim_urls(90)
# scrape first url 
f = open('newUrls.txt')
urls = f.readlines()
f.close()

# change working dir to save results in right folder
os.chdir("ranking_files")

for url in urls:
	# the name of a result file is the date of the snapshot .txt
	date = re.search('[0-9]+', url).group()
	# get datetime object from date
	dateTimeDate = getDate(date)

	# get list of topsites
	top_sites = extract_top_sites(url[0:-1], 500)


	# open a file named the date of the alexa snapshot.txt
	q = open(str(date)+".txt", 'w')

	# now in each topsite add the historical description from the meta tag
	for tup in top_sites:
		# get closest snap show 
		closest_snap_shot = get_closest_snapshot(tup[1], date)

		# check if url was in the arhive at all
		# closest_snap_shot is int if not in arhive
		inArchive = not isinstance( closest_snap_shot, int )


		if (inArchive):
			# if closest snap shot is less than 90 days later or prior to alexa snapshot,
			# we save the description from the archived snapshow
			delta = closest_snap_shot[1] - dateTimeDate
			if (abs(delta.days) < 90):
				histo_header_desc = get_description(closest_snap_shot[0])
				# get rid of commas in description
				histo_header_desc = histo_header_desc.replace(',', '')
			else:
				histo_header_desc = "NO_SNAPSHOT_CLOSE_ENOUGH_IN_TIME"
		else:
			histo_header_desc = "URL_NOT_IN_ARCHIVE"


		# write tuples in CSV format to file
		toWrite = str(tup[0]) + "," + tup[1] + "," + histo_header_desc + "\n"
		print(toWrite)
		q.write(toWrite)


	# remember to close file
	q.close()
	print('wrote another result to file \n')

