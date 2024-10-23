#!/usr/bin/env python3
""" 'insert_school's module."""

if __name__ == "__main__":
    def insert_school(mongo_collection, **kwargs):
        """
            Function that inserts a new document in a collection
            based on kwargs.
            'mongo_collection' will be the pymongo collection object.
            Returns the new '_id'.
        """
        new_doc = []
        new_doc.append(**kwargs)

        mongo_collection.insert(new_doc)

        return mongo_collection._id
