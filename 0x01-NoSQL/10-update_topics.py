#!/usr/bin/env python3
"""
Change school topics
"""


def update_topics(mongo_collection, name, topics):
    """
    changes all topics of a school document based on the name
    """
    key = {"name": name}
    values = {"$set": {"topics": topics}}

    return mongo_collection.update_many(key, values)
