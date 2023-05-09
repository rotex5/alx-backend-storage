#!/usr/bin/env python3
"""
Log stats
"""
from pymongo import MongoClient

OP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def get_nginx_details():
    """
    provides some stats about Nginx logs stored in MongoDB
    """
    _collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx

    num_logs = _collection.count_documents({})
    print("{} logs".format(num_logs))

    print('Methods:')
    for method in OP_METHODS:
        output_count = _collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, output_count))

    status_checked = _collection.count_documents(
            {"method": "GET", "path": "/status"})

    print("{} status check".format(status_checked))

    addresses = _collection.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }
         }
    ])

    print("IPs:")

    for ip in addresses:
        ip_count = ip.get("count")
        ip_add = ip.get("ip")
        print("\t{}: {}".format(ip_add, ip_count))


if __name__ == "__main__":
    get_nginx_details()
