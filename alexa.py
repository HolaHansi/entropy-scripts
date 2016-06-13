from getUrls import get_clean_urls
from scrape import extract_top_sites
# get urls from memento and save to urls.txt
# get_clean_urls()
# scrape first url 
f = open('urls.txt')
url = f.readline()[0:-1]
print("this is the url %s", url)
print(extract_top_sites(url, 40))