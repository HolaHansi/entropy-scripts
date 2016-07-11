from pymongo import MongoClient
import datetime
import requests
from bs4 import BeautifulSoup
import re
import time

class ipsObj:
    """
    class for ips from dnsTrails.com
    """
    def close_in_time(self, date):
        """
        returns true if ipsObj has date greater than date argument,
        but less than 3 months greater.
        """
        toReturn = self.date > date and self.date < (date + datetime.timedelta(days=90))
        return toReturn

    def __init__(self, date, ips):
        self.date = date
        self.ips = ips

def make_request(url):
    requestURL = "http://server9.rscott.org/tools/lookup.htm?domain=" + url
    r = requests.get(requestURL)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_ips_dates(url):

    # attempt to call dnstrails.com at most 3 times.
    # or untill it gives more rows than 3
    # this is because site doesn't always work on first request.
    i = 1
    while True:
        soup = make_request(url)
        rows = soup.findAll("tr")
        if (len(rows) >= 3):
            break
        if (i >= 3):
            return []
        i += 1
        print("request %d failed" % i)
        time.sleep(5)

    ipObjects = []
    # print(rows)
    for row in rows:
        tds = row.findAll('td')
        i=0
        for td in tds:
            # for date
            if (i==0):
                date_str = re.search("[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]", str(td)).group()
                date = datetime.datetime.strptime(date_str, "%m/%d/%Y")
            # ips
            if (i==3):
                ips = []
                ips_cursor = td.findAll('a')
                for ip in ips_cursor:
                    ips.append(ip.contents[0])
                obj = ipsObj(date, ips)
                ipObjects.append(obj)
            i += 1
    return ipObjects


def add_historical_ips(col):
    """
    takes a collection, and adds historical ips to respective snapshots of every site
    with a tld in allowed_tlds.
    """
    sites = col.find({})
    for site in sites:
        url = site['url']
        snapshots = site['snapshots']

        allowed_tlds = ['com', 'net', 'org', 'biz', 'info', 'mobi', 'name']

        if url.split('.')[-1] not in allowed_tlds:
            print("can't get ips for domain %s" % url.split('.')[1])
            continue

        print("===== Updating IPs for %s ===== \n \n" % url)
        # get ipObjects
        ipObjects = get_ips_dates(url)

        for snapshot in snapshots:
            snap_date = snapshot['date']
            # filter out all the ipObjects not close in time.
            result = filter(lambda x : x.close_in_time(snap_date), ipObjects)
            result_list = list(result)
            # only if result_list is not empty, do we update snapshot with ipObj
            if (len(result_list) > 0):
                ipObj = result_list[0]

                result = col.update_one(
                {'url': url, 'snapshots.date': snap_date},
                {
                    "$set": {'snapshots.$.ips': ipObj.ips }
                }
                )

                if result.acknowledged:
                    print("updated ips:\n")
                    print(ipObj.ips)
                    print("for dates:\n")
                    print(ipObj.date)
                    print(snap_date)
                else:
                    print("something went wrong")
