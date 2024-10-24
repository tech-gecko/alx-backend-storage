#!/usr/bin/env python3
"""
    Module containing the 'top_students' function.
"""


def top_students(mongo_collection):
    """
        Function that returns all students sorted by average score.
        'mongo_collection' will be the pymongo collection object.
        The top must be ordered.
        The average score must be part of each item and should
        return with key = averageScore.
    """
    pipeline = [
        {
            "$project": {
                "name": 1,  # Include 'name' field in output.
                "averageScore": {"$avg": "$topics.score"} # Calculate avg score.
            }
        },
        {
            "$sort": {"averageScore": -1}  # Sort by averageScore in desc order
        },
    ]

    # Use the aggregation pipeline and return the result
    return list(mongo_collection.aggregate(pipeline))


if __name__ == "__main__":
    pass
