#!/usr/bin/env python3
"""
    Module containing the 'update_topics' function.
"""


def update_topics(mongo_collection, name, topics):
    """
        Function that changes all topics of a school document
        based on the name.
        'mongo_collection' will be the pymongo collection object.
        'name' (string) will be the school name to update.
        'topics' (list of strings) will be the list of topics
        approached in the school.
    """
    mongo_collection.update_many(
        {"name": "example_name"},
        {"$set": {"address": "new_address"}}
    )

    return


if __name__ == "__main__":
    pass
