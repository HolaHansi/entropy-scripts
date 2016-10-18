import os
import requests
# from secrets import ARIN_API_KEY
from time import sleep
import xml.etree.ElementTree as ET


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
            elif "parentNetRef" in elem.tag:
                whoIs.parentNetRef = elem.text
            elif "updateDate" in elem.tag:
                whoIs.updateDate = elem.text

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


def update_or_create_handler(ip, handlerCol):
    x = whoIsClass()
    numVal = x.numValue(ip)
    handleCur = handlerCol.find({
        "$and": [
            {"numStartAdd": {"$lt": numVal}},
            {"numEndAdd": {"$gt": numVal}}
        ]
        })
    # if this query returns anything, then update ips list with this ip
    print(handleCur.count())
    if handleCur.count():
        print('updating handler for ip: %s' % ip)
        first_handler = handleCur[0]
        result = handlerCol.update_one(
            {"_id":
                first_handler['_id']
            },
            # note that addToSet would never create a duplicate
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
        # if whois request successful - update db
        if handler.requestSuccess:
            # update doc with values from object attributes
            doc = {}
            for key in handler.__dict__.keys():
                doc[key] = handler.__dict__[key]

            result = handlerCol.insert_one(doc)
            if result.acknowledged:
                print("inserted handle: %s into db" % handler.name)
            else:
                print('failed to insert handle: %s into db' % handler.name)
        else:
            print('request to ARIN whois did not return status 200!\n')





def get_handler_on_ips(siteCol, handlerCol):
    # obtain a cursor to a list of all the distinct IPs in the sites collection.
    pipeline = [
        {"$unwind": "$snapshots"},
        {"$unwind": "$snapshots.ips"},
        {"$group": {
            "_id": "$snapshots.ips"
            }
        }
        ]
    IPsCursor = siteCol.aggregate(pipeline)


    # for every IP add or update info on its handler
    k = 1
    for ipDic in IPsCursor:
        ip = ipDic['_id']
        update_or_create_handler(ip, handlerCol)
        print("%d processed ips so far..." % (k))
        k += 1



#FOR HISTORICAL WHOWAS REPORTS - Currently we can't make bulk requests to API..
# class ArinWhoWas:
#     BASE = "https://www.arin.net/rest"
#     KEY = ARIN_API_KEY
#
#     def __init__(self):
#         WORK_DIR = os.path.dirname(os.path.realpath(__file__))
#
#         self.WHOWAS_REPORTS = WORK_DIR + "/whowas_reports"
#
#         # create DIR if not present
#         try:
#             os.mkdir(self.WHOWAS_REPORTS)
#         except OSError:
#             pass
#
#         # change to this dir
#         os.chdir(self.WHOWAS_REPORTS)
#
#
#     def file_ticket(self, ip):
#         url = self.BASE + "/report/whoWas/net/%s?apikey=%s" % (ip, self.KEY)
#         r = requests.get(url)
#
#         if r.status_code == 200:
#             root = ET.fromstring(r.text)
#             for elem in root.findall('.//'):
#                 # tags are not clean, hence this iteration...
#                 if 'ticketNo' in elem.tag:
#                     self.TICKET_NO = elem.text
#                     break
#             print(self.TICKET_NO)
#         else:
#             print('request failed!')
#             print(r.text)
#
#     def get_message_id(self):
#         url = self.BASE + "/ticket/%s?apikey=%s" % (self.TICKET_NO, self.KEY)
#         r = requests.get(url)
#         print(r.status_code)
#         print(r.text)
