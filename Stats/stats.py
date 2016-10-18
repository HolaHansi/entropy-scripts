from pymongo import MongoClient
import os

client = MongoClient()
db = client.alexaDB
colSites = db.sites
colHandlers = db.handlers
# #
# # # create DIR if not present
# # try:
# #     os.mkdir("stats")
# # except OSError:
# #     pass
# #
# # # change to this dir
# # os.chdir("stats")
# #
# print("=== getting handlerNumIps.json ==== \n")
# # get the number of ips for each handlers
# f = open("handlerNumIps.json", "w")
# pipeline = [
# {'$project': {'name': 1, '_id': 0, "countIps": {"$size": "$ips"}, "handle": 1}},
# {"$sort": {"countIps": -1}}
# ]
# cur = colHandlers.aggregate(pipeline)
# f.write("{handlers: [\n")
# for line in cur:
#     f.write(str(line) + ",\n")
# f.write("]}\n")
# f.close()
#
# print("=== getting ipsPrDate.json === \n")
# # group snapshots by date and get all IPs for each date.
# f = open("ipsPrDate.json", "w")
# pipeline = [
#     {"$unwind": "$snapshots"},
#     {"$unwind": "$snapshots.ips"},
#     {"$group": {
#         "_id": "$snapshots.date",
#         "ips": {"$addToSet": "$snapshots.ips"}
#     }},
#     {"$sort": {"_id": 1}}
# ]
# cur = colSites.aggregate(pipeline)
# f.write("{handlers: [\n")
# for line in cur:
#     f.write(str(line) + ",\n")
# f.write("]}\n")
# f.close()
# #
# print("=== getting snapshotHandlers.json ==== \n")
# # for each snapshot, get corresponding handlers with counts of unique ips
# f = open("snapshotHandlers.json", "w")
def getData():
    pipeline = [
        {"$unwind": "$snapshots"},
        {"$unwind": "$snapshots.ips"},
        {"$group": {
            "_id": "$snapshots.date",
            "ips": {"$push": "$snapshots.ips"}
        }},
        {"$unwind": "$ips"},
        # for every snapshot if the IP was in the handler ips, they are joined
        {"$lookup":
            {
            "from": "handlers",
            "localField": "ips",
            "foreignField": "ips",
            "as": "handler"
            }
        },
        # for each comb of date and handler.name, will record and count number of occurences
        {"$unwind": "$handler"},
        {"$group": {
                # TODO: handle vs. name???
                "_id": {"_id": "$_id", "handlerName": "$handler.name"},
                "count": {"$sum": 1},
            }
        },
        {"$group": {
             "_id": "$_id._id",
            "handlers": {"$push": {"handlerName": "$_id.handlerName", "countIps": "$count"}}
        }},
        {"$unwind": "$handlers"},
        # we need to merge duplicates summing their ip counts
        {"$group": {
            "_id": {"_id": "$_id", "handler": "$handlers.handlerName"},
            "countIps": {"$sum": "$handlers.countIps"}
        }},
        # finally, group by date of snapshot
        {"$group": {
            "_id": "$_id._id",
            "handlers": {"$addToSet": {"handlerName": "$_id.handler", "countIps": "$countIps"}}
            }
        },

        # get aggregated count of ips for each snapshot
        {"$project": {
            "date": "$_id",
            "handlers": 1,
            "totalIps": {"$sum": "$handlers.countIps"},
            "_id": 0
        }
        },
        # for each handler in handlers, compute the ratio: countIps / totalIps
        {"$unwind": "$handlers"},

        {"$group": {
            "_id": "$date",
            "totalIps": {"$first": "$totalIps"},
            "handlers": {"$addToSet":
                {"handlerName": "$handlers.handlerName",
                "countIps": "$handlers.countIps",
                "ratio": {"$multiply": [{"$divide": ["$handlers.countIps", "$totalIps"]}, 100]}
                }
            }
        }},
        {"$project": {
            "_id": 0,
            "date": "$_id",
            "handlers": 1,
            "totalIps": 1
        }},



        # sort by date
        {"$sort": {"date": 1}}
    ]

    cur = colSites.aggregate(pipeline)

    #
    # # replace handler with name
    # for date in cur:
    #     for handle in date['handlers']:
    #     colHandlers.find({x})
    #


    return list(cur)
# f.writelines(str(list(cur)).replace("'", '"'))

# f.write("{dates: [\n")
# for x in cur:
#     print(x)
#     f.write(str(x) + ",\n")
# f.write("]}\n")
# f.close()
#
# print("succesfully created statfiles in directory: stats")
