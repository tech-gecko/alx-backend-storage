#!/usr/bin/env python3
""" 12-log_stats.py - Show stats of Nginx logs in MongoDB """

from pymongo import MongoClient

if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    nginx_collection = client.logs.nginx

    # Get the total number of logs
    log_count = nginx_collection.count_documents({})
    print(f"{log_count} logs")

    # Count for each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count for status check
    get_status_count = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{get_status_count} status check")

    # Top 10 most present IPs
    print("IPs:")
    pipeline = [
        {
            "$group": {
                "_id": "$ip",  # Group by IP address
                "count": {"$sum": 1}  # Count occurrences of each IP
            }
        },
        {"$sort": {"count": -1}},  # Sort by count in descending order
        {"$limit": 10}  # Limit to the top 10 IPs
    ]

    # Run the aggregation pipeline
    top_ips = nginx_collection.aggregate(pipeline)

    # Print the top 10 IPs
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")
