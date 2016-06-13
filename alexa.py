from getUrls import get_clean_urls
from scrape import extract_top_sites
# get urls from memento and save to urls.txt
# get_clean_urls()
# scrape first url 
f = open('urls.txt')
urls = f.readlines()
print("this is the url %s", urls[0][0:-1])
print(extract_top_sites(urls[0][0:-1], 40))
print(extract_top_sites(urls[1][0:-1], 40))