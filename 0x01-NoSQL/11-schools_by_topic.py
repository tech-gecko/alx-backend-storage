#!/usr/bin/env python3
"""
    Module containing the 'schools_by__topic' function.
"""


def schools_by_topic(mongo_collection, topic):
    """
        Function that returns the list of schools having
        a specific topic.
        'mongo_collection' will be the pymongo collection object.
        'topic' (string) will be the topic searched.
    """
    schools = mongo_collection.find(
        {"topics": topic},
        {"name": 1, "topics": 1}
    )

    return list(schools)


if __name__ == "__main__":
    pass
