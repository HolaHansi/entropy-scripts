from getUrls import get_clean_urls
from scrape import extract_top_sites

# get urls from memento and save to urls.txt
# get_clean_urls()

# scrape first url 
f = open('urls.txt')
url = f.readline() 
print("this is the url %s", url)

print(url[0:-1])

extract_top_sites("http://web.archive.org/web/20100209035039id_/http://www.alexa.com/topsites/") 

