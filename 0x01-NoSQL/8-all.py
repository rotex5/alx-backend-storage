#!/usr/bin/env python3
"""
List all documents in Python
"""


def list_all(school_collection):
    """
    lists all documents in a collection
    """
    documents = school_collection

    if documents.count_documents({}) == 0:
        return []
    return documents.find()
