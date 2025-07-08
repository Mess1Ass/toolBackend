from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

client = MongoClient("mongodb://admin:admin@106.14.212.1:27017")
db = client["SNH48"]
collection = db["BidsExcels"]

def insert_file_info(filename, size, path, is_folder=False, parent="root"):
    return collection.insert_one({
        "filename": filename,
        "size": size,
        "path": path,
        "is_folder": is_folder,
        "upload_time": datetime.datetime.now(datetime.timezone.utc),
        "parent": parent
    })

def list_files(parent="root"):
    files = list(collection.find({"parent": parent}).sort("is_folder", -1))
    for file in files:
        file["_id"] = str(file["_id"])
    return files

def delete_file(file_id):
    return collection.delete_one({"_id": ObjectId(file_id)})

def find_file_by_id(file_id):
    return collection.find_one({"_id": ObjectId(file_id)})

def find_by_name_and_parent(name, parent):
    return collection.find_one({
        "filename": name,
        "parent": parent
    })
