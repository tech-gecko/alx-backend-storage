#!/usr/bin/env python3
""" 12-log_stats.py """
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    nginx_collection = client.logs.nginx

    log_count = nginx_collection.count_documents({})
    print(f"{log_count} logs")

    get_count = nginx_collection.count_documents({"method": "GET"})
    post_count = nginx_collection.count_documents({"method": "POST"})
    put_count = nginx_collection.count_documents({"method": "PUT"})
    patch_count = nginx_collection.count_documents({"method": "PATCH"})
    delete_count = nginx_collection.count_documents({"method": "DELETE"})
    print("Methods:")
    print(f"\tmethod GET: {get_count}")
    print(f"\tmethod POST: {post_count}")
    print(f"\tmethod PUT: {put_count}")
    print(f"\tmethod PATCH: {patch_count}")
    print(f"\tmethod DELETE: {delete_count}")

    get_status_count = nginx_collection.count_documents(
                {"method": "GET", "path": "/status"}
            )
    print(f"{get_status_count} status check")
