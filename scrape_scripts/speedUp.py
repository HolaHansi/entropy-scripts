from bs4 import BeautifulSoup
import datetime
import requests
import re
import time


allowed_tlds = ['com', 'net', 'org', 'biz', 'info', 'mobi', 'name']

class ipsObj:
    """
    class for ips and nameservers from dnsTrails.com
    """
    date = None
    ips = None
    ns = None

    def close_in_time(self, date):
        """
        returns true if ipsObj has date greater than date argument,
        but less than 3 months greater.
        """
        toReturn = self.date > date and self.date < (date + datetime.timedelta(days=90))
        return toReturn

def make_request(url):
    requestURL = "http://server9.rscott.org/tools/lookup.htm?domain=" + url
    r = requests.get(requestURL)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_ips_dates(url):
    """
    Attempt to call dnstrails.com at most 3 times.
    or untill it gives more rows than 3
    this is because site doesn't always work on first request.

    When succesfully retrieving DNStrails table, will make a record for every well-formed row. 
    """
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

    # return all the ipObjects from the rows
    return ipObjects_from_rows(rows)


def concat_ns(ns_list):
    """
    given a list known to contain scattered NS name [xxx, ggg, ff.ff, dd.net], produces: "xxx.ggg.ff.ff.dd.net"
    """
    toReturn = ""
    for i in range(len(ns_list)-1):
        toReturn += (ns_list[i] + '.')
    toReturn += ns_list[-1]
    return toReturn


def clean_ns(ns_list):
    """
    NSs are scattered across multiple links in table, so not elements of ns.contents[0] are valid NS names.
    We explot that an NS on DNSTrails always looks like xxx.y where y is in allowed_tlds. 
    Hence, we create a new list of Name servers by concatenating the scattered parts of a ns name into single NSs that 
    end in xxx.y where y is in allowed_tlds. 
    WARNING: we're ignoring all Name servers without a tld in allowed_tlds - but that's a problem of scope in the DNStrails db. 
    """
    if len(ns_list) == 1:
        return ns_list
    else:
        new_ns = []
        # beginning of new ns
        k = 0
        for i in range(len(ns_list)):
            if '.' in ns_list[i] and ns_list[i].split('.')[-1] in allowed_tlds:
                new_ns.append(concat_ns(ns_list[k:i+1]))
                k = i + 1
        return new_ns

def create_ipObject(row):
    """
    Given an a row, will create an ipObject.

    """
    tds = row.findAll('td')
    i=0
    obj = ipsObj()
    for td in tds:
        # for date
        if (i==0):
            # find a date in first column
            date_str = re.search("[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]", str(td)).group()
            date = datetime.datetime.strptime(date_str, "%m/%d/%Y")
            obj.date = date
        # for NS 
        if (i==2):
            name_servers = []
            ns_cursor = td.findAll('a')
            for ns in ns_cursor:
                name_servers.append(ns.contents[0])
            clean_ns(name_servers)    
            obj.ns = name_servers
        # ips
        if (i==3):
            ips = []
            ips_cursor = td.findAll('a')
            for ip in ips_cursor:
                ips.append(ip.contents[0])
            obj.ips = ips
        # increment to consider next column in row..
        i += 1

    if obj.ns:
         obj.ns = clean_ns(obj.ns)
    return obj


def ipObjects_from_rows(rows):
    """
    Given a list of rows in table from DNSTrails.com, will make call to create_ipObject and make an ipobject for each row and return these
    as a list of ipObjects. Will only add ipObject to list if it has a date, and has an IP or a NS. 
    """
    ipObjects = []
    # print(rows)
    for row in rows:
        obj = create_ipObject(row)
        # only if obj has a date, and has ips or ns records, should we save it.. 
        if obj.date is not None and (obj.ips is not None or obj.ns is not None):
            ipObjects.append(obj)
    return ipObjects





def add_historical_ips(col):
    """
    takes a collection, and adds historical ips to respective snapshots of every site
    with a tld in allowed_tlds.
    """
    sites = col.find({})
    number_of_sites = col.find({}).count()
    i = 1
    number_of_site_in_tld = 0
    success_updates = 0
    for site in sites:
        i += 1
        if (i < 731):
            continue
        print("==== request %d out of %d ==== " % (i, number_of_sites))
        url = site['url']
        snapshots = site['snapshots']

        if url.split('.')[-1] not in allowed_tlds:
            print("can't get ips for domain %s" % url.split('.')[1])
            continue

        number_of_site_in_tld += 1


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
                    "$set": {'snapshots.$.ips': ipObj.ips, 'snapshots.$.name_servers': ipObj.ns}
                }
                )
                if result.acknowledged:
                    print("updated ips and NS\n")
                    print(ipObj.ips, ipObj.ns)
                    print("for dates:\n")
                    print(ipObj.date)
                    print(snap_date)
                else:
                    print("something went wrong")
            success_updates += 1

    print("number of successful updates: %d out of number in tld: %d number of sites: %d" % 
        (success_updates, number_of_site_in_tld, number_of_sites))




# for testing
from pymongo import MongoClient
# connect to db
client = MongoClient()
db = client.alexaDB
col = db.sites

add_historical_ips(col)



