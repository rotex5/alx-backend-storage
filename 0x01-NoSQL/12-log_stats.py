#!/usr/bin/env python3
"""
Log stats
"""
from pymongo import MongoClient

OP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


if __name__ == "__main__":
    """
    provides some stats about Nginx logs stored in MongoDB
    """
    _collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx

    num_logs = _collection.count_documents({})
    print("{} logs".format(num_logs))

    print('Methods:')
    for method in OP_METHODS:
        output = _collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, output))

    status_checked = _collection.count_documents(
            {"method": "GET", "path": "/status"})

    print("{} status check".format(status_checked))
