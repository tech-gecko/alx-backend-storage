#!/usr/bin/env python3
"""
    'list_all's module.
"""

if __name__ == "__main__":
    def list_all(mongo_collection):
        """
            Function that lists all documents in a collection.
            Returns an empty list if no document is in the collection.
            'mongo_collection' will be the pymongo collection object.
        """
        documents = mongo_collection.all()

        if not documents:
            return []

        return list(documents)
