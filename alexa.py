from getUrls import get_clean_urls
import os
import re
from scrape import extract_top_sites

# make a dir for the data files
os.makedirs("ranking_files")


# get urls from memento and save to urls.txt
#get_clean_urls()
# scrape first url 
f = open('urls.txt')
urls = f.readlines()
f.close()

# change working dir to save results in right folder
os.chdir("ranking_files")

for url in urls:
	# the name of a result file is the date of the snapshot .txt
	date = re.search('[0-9]+', url).group()
	to_save = extract_top_sites(url[0:-1], 500)

	q = open(str(date)+".txt", 'w')
	for tup  in to_save:
		# write tuples in CSV format to file
		q.write(str(tup[0]) + "," + tup[1] + "\n")
	q.close()
	print('wrote another result to file \n')
