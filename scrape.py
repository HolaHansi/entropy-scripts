from bs4 import BeautifulSoup 
import re
import requests


# def extract_top_sites(limit=500):
# 	int i = 0
# 	f = open('urls.txt', 'r')
# 	urls = f.readlines()


counter = 0
sites = []
limit = 500
elem_on_page = 0

def extract_top_sites(url,limit=500): 
	global counter
	global sites
	global elem_on_page

	# check to see if hard limit is respected
	if (limit > 500):
		print("limit max is 500\n")
		return 0

	r = requests.get(url)
	if (r.status_code != 200):
		print("status not 200 for url: %s", url)
		return 0
	else:
		html = r.text
		print("status 200 for url %s", url)

	soup = BeautifulSoup(html, 'html.parser')

	# get all site-listings
	site_listings = soup.find_all(class_="site-listing")

	elem_on_page = len(site_listings)
	print(elem_on_page)
	
	# now update sites and counter
	if (1 == get_sites_from_page(site_listings, limit)):
		# open next page of rankings
		next_page = soup.find('a', class_="next")['href']
		print(next_page)
		str_index = url.find("topsites")
		new_url = url[0:str_index - 1] + next_page

		# recursive call
		extract_top_sites(new_url, (limit-elem_on_page))
	else:
		print("counter value " + str(counter))
		print(sites)
		return sites


	
def get_sites_from_page(site_listings, limit):
	"""
	takes bs4 object site_listings and append the top_sites with corresponding rankings as tuples
	to the global list variable sites. Returns 0 if limit was reached, and 1 otherwise. 
	"""
	global counter
	global sites

	for site in site_listings:
		if (counter < limit):
			link_node = site.find('a')
			# split for >
			link = re.split('>', str(link_node))[0]
			# get end of link 
			link = re.split('/', link)[-1]
			# remove double quotes
			link = link[0:-1]

			# increment counter and create tuple s.t. site_tup = (rank, url)
			counter += 1
			site_tup = (counter, link)

			#append to list of sites
			sites.append(site_tup)
		else:
			# limit is reached...
			return 0
    # limit not reached yet
	return 1







	

