import os
import requests
from secrets import ARIN_API_KEYY
from time import sleep
import xml.etree.ElementTree as ET

from pymongo import MongoClient


class ArinWhoWas:
    BASE = "https://www.arin.net/rest"
    KEY = ARIN_API_KEYY

    def __init__(self):
        WORK_DIR = os.path.dirname(os.path.realpath(__file__))

        self.WHOWAS_REPORTS = WORK_DIR + "/whowas_reports"

        # create DIR if not present
        try:
            os.mkdir(self.WHOWAS_REPORTS)
        except OSError:
            pass

        # change to this dir
        os.chdir(self.WHOWAS_REPORTS)


    def file_ticket(self, ip):
        url = self.BASE + "/report/whoWas/net/%s?apikey=%s" % (ip, self.KEY)
        r = requests.get(url)

        if r.status_code == 200:
            root = ET.fromstring(r.text)
            for elem in root.findall('.//'):
                # tags are not clean, hence this iteration...
                if 'ticketNo' in elem.tag:
                    self.TICKET_NO = elem.text
                    break
            print(self.TICKET_NO)
        else:
            print('request failed!')
            print(r.text)

    def get_message_id(self):
        url = self.BASE + "/ticket/%s?apikey=%s" % (self.TICKET_NO, self.KEY)
        r = requests.get(url)
        print(r.status_code)
        print(r.text)

# # testing
# x = Arin()
# x.file_ticket("172-31-62-169")
# print("about to look up message")
# sleep(10)
# x.get_message_id()



class handlerWhois:
    url = "https://whois.arin.net/rest/ip/%s/"
    ips = []
    numStartAdd = 0
    numEndAdd = -1

    @staticmethod
    def numValue(ip):
        ipList = ip.split('.')
        nums = map(lambda x : int(x), ipList)
        ipVal = 0
        i = 3
        # msb from left to right
        for num in nums:
            ipVal += (256 ** i) * num
            i -= 1
        return ipVal

    def inRange(self, ip):
        thisIp = self.numValue(ip)
        # TODO: find out if intervals are inclusive or not
        return self.numStartAdd <= thisIp <= self.numEndAdd

    def lookup_ip(self, ip):
        # obj already has ips - only add if IP is not already in IPs and in range.
        if self.ips:
            if self.inRange(ip) and ip not in self.ips:
                self.ips.append(ip)
                print('ip was in range, appended to ips')
                return 1
            else:
                print("ip out of range")
                return 0

        # obj doesn't already have ips - look up ip with ARIN whois
        else:
            # this should probably be done in initialization!
            r = requests.get(self.url % ip)
            print(r.text)
            if r.status_code == 200:
                root = ET.fromstring(r.text)
                # run through elements and update class fields
                for elem in root.findall(".//"):
                    # initiate info on handle
                    if "registrationDate" in elem.tag:
                        self.regDate = elem.text
                    elif "ref" in elem.tag:
                        self.ref = elem.text
                    elif "handle" in elem.tag:
                        self.handle = elem.text
                    elif "name" in elem.tag:
                        self.name = elem.text
                    elif "description" in elem.tag:
                        self.description = elem.text
                    elif "orgRef" in elem.tag:
                        self.orgRef = elem.text

                    # get start and end address, and the respective numerical values
                    elif "endAddress" in elem.tag:
                        self.endAdd = elem.text
                        self.numEndAdd = self.numValue(self.endAdd)
                    elif "startAddress" in elem.tag:
                        self.startAdd = elem.text
                        self.numStartAdd = self.numValue(self.startAdd)
                # append this ip
                self.ips.append(ip)
                print("initiated handler for ip %s, handle: %s" % (ip, self.handle))
                return 1


# I have list of IPs
# for each IP if first one, make a obj and call lookup ip
# if not first, for each obj in list of objects,
# run lookup_ip, if every obj returns 0, then create new object and loopup_ip.

# flush all the object to mongodb. Bad idea, as script might stop, and we'll lose
# all objects in memory.
# idea: have objects in memory and in db.


url = "https://whois.arin.net/rest/ip/%s/"

class whoIsClass:
    @staticmethod
    def numValue(ip):
        ipList = ip.split('.')
        nums = map(lambda x : int(x), ipList)
        ipVal = 0
        i = 3
        # msb from left to right
        for num in nums:
            ipVal += (256 ** i) * num
            i -= 1
        return ipVal

def request_whois(ip):
    request_url = url % ip
    r = requests.get(request_url)
    whoIs = whoIsClass()
    if r.status_code == 200:
        root = ET.fromstring(r.text)
        # run through elements and update class fields
        for elem in root.findall(".//"):
            # initiate info on handle
            if "registrationDate" in elem.tag:
                whoIs.regDate = elem.text
            elif "ref" in elem.tag:
                whoIs.ref = elem.text
            elif "handle" in elem.tag:
                whoIs.handle = elem.text
            elif "name" in elem.tag:
                whoIs.name = elem.text
            elif "description" in elem.tag:
                whoIs.description = elem.text
            elif "orgRef" in elem.tag:
                whoIs.orgRef = elem.text

            # get start and end address, and the respective numerical values
            elif "endAddress" in elem.tag:
                whoIs.endAdd = elem.text
                whoIs.numEndAdd = whoIs.numValue(whoIs.endAdd)
            elif "startAddress" in elem.tag:
                whoIs.startAdd = elem.text
                whoIs.numStartAdd = whoIs.numValue(whoIs.startAdd)
        whoIs.requestSuccess = True
        whoIs.ips = [ip]
    else:
        whoIs.requestSuccess = False
    return whoIs


def update_or_create_handler(ip):
    x = whoIsClass()
    numVal = x.numValue(ip)
    handleCur = handlerCol.find({
        "$and": [
            {"numStartAdd": {"$lt": numVal}},
            {"numEndAdd": {"$gt": numVal}},
            {'ips': {
                        "$not": {
                        "$in": [ip]
                        }
                    }
            }
        ]
        })
    # if this query returns anything, then update ips list with this ip
    print(handleCur.count())
    if handleCur.count():
        print('updating handler for ip: %s' % ip)
        first_handler = handleCur[0]
        print(first_handler)
        result = handlerCol.update_one(
            {"_id":
                first_handler['_id']
            },
            { "$addToSet":
                {"ips": ip}
            })

        if result.acknowledged:
            print("updated handler: %s with ip: %s" % (first_handler['name'], ip))
        else:
            print("failed to update db!")
    # create new entry for this handle
    else:
        print('creating handler for ip: %s' % ip)
        handler = request_whois(ip)
        if handler.requestSuccess:
            try:
                doc = {
                        'regDate': handler.regDate,
                        'ref': handler.ref,
                        'handle': handler.handle,
                        'name': handler.name,
                        'description': handler.description,
                        'orgRef': handler.orgRef,
                        'endAdd': handler.endAdd,
                        'numEndAdd': handler.numEndAdd,
                        'startAdd': handler.startAdd,
                        'numStartAdd': handler.numStartAdd,
                        'ips': [ip]
                    }
            except:
                print('reference error when creating document!')
                return -1


            result = handlerCol.insert_one(doc)
            if result.acknowledged:
                print("inserted handle: %s into db" % handler.name)
            else:
                print('failed to insert handle: %s into db' % handler.name)
        else:
            print('request to ARIN whois did not return status 200!\n')




client = MongoClient()
db = client.alexaDB
siteCol = db.sites
# make new collection for ip handler
handlerCol = db.handlers

# TODO remove this
db.handlerCol.delete_many({})

pipeline = [
    {"$unwind": "$snapshots"},
    {"$unwind": "$snapshots.ips"},
    {"$group": {
        "_id": "$snapshots.ips"
        }
    }
    ]


# now we have list of all distinct IPs in data
IPsCursor = siteCol.aggregate(pipeline)

for ipDic in IPsCursor:
    ip = ipDic['_id']
    update_or_create_handler(ip)


close()
    # check if in collection (in range of some handler) if empty on look up
    # then look up whois and create entry in collection







# for ip in IPsCursor:
#     print(ip['_id'])



#
# x = handlerWhois()
#
# x.lookup_ip("65.55.255.255")
# x.lookup_ip("65.55.255.253")
