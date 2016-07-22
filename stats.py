from pymongo import MongoClient
import os

client = MongoClient()
db = client.alexaDB
colSites = db.sites
colHandlers = db.handlers



# create DIR if not present
try:
    os.mkdir("stats")
except OSError:
    pass

# change to this dir
os.chdir("stats")

print("=== getting handlerNumIps.json ==== \n")
# get the number of ips for each handlers
f = open("handlerNumIps.json", "w")
pipeline = [
{'$project': {'name': 1, '_id': 0, "countIps": {"$size": "$ips"}, "handle": 1}},
{"$sort": {"countIps": -1}}
]
cur = colHandlers.aggregate(pipeline)

for line in cur:
    f.write(str(line) + "\n")
f.close()

print("=== getting ipsPrDate.json === \n")
# group snapshots by date and get all IPs for each date.
f = open("ipsPrDate.json", "w")
pipeline = [
    {"$unwind": "$snapshots"},
    {"$unwind": "$snapshots.ips"},
    {"$group": {
        "_id": "$snapshots.date",
        "ips": {"$addToSet": "$snapshots.ips"}
    }},
]
cur = colSites.aggregate(pipeline)
for line in cur:
    f.write(str(line) + "\n")
f.close()

print("=== getting snapshotHandlers.json ==== \n")
# for each snapshot, get corresponding handlers with counts
f = open("snapshotHandlers.json", "w")
pipeline = [
    {"$unwind": "$snapshots"},
    {"$unwind": "$snapshots.ips"},
    {"$group": {
        "_id": "$snapshots.date",
        "ips": {"$addToSet": "$snapshots.ips"}
    }},
    {"$unwind": "$ips"},
    {"$lookup":
        {
        "from": "handlers",
        "localField": "ips",
        "foreignField": "ips",
        "as": "handler"
        }
    },
    {"$unwind": "$handler"},
    {"$group": {
            "_id": {"_id": "$_id", "handlerName": "$handler.name"},
            "count": {"$sum": 1},
        }
    },
    {"$group": {
        "_id": "$_id._id",
        "handlers": {"$addToSet": {"handlerName": "$_id.handlerName", "countIps": "$count"}}
    }}
]

cur = colSites.aggregate(pipeline)
for x in cur:
    f.write(str(x) + "\n")
f.close()

print("succesfully created statfiles in directory: stats")
