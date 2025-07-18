from pymongo import MongoClient
from bson.objectid import ObjectId
from utils.db_util import get_collection
import datetime


collection = get_collection("BidsExcels")

# 插入文件、文件夹
def insert_file_info(filename, size, path, is_folder=False, parent="root"):
    result = collection.insert_one({
        "filename": filename,
        "size": size,
        "path": path,
        "is_folder": is_folder,
        "upload_time": datetime.datetime.now(datetime.timezone.utc),
        "parent": parent
    })
    return result.inserted_id  # 返回新文档的_id

# 列出文件、文件夹
def list_files(parent="root"):
    files = list(collection.find({"parent": parent}).sort("is_folder", -1))
    for file in files:
        file["_id"] = str(file["_id"])
    return files

# 删除文件、文件夹
def delete_file(file_id):
    return collection.delete_one({"_id": ObjectId(file_id)})

# 根据id查找文件、文件夹
def find_file_by_id(file_id):
    return collection.find_one({"_id": ObjectId(file_id)})

# 根据父级路径查找文件、文件夹
def find_files_by_parent(parent):
    return list(collection.find({"parent": parent}))

# 根据当前文件名、父级路径查找文件、文件夹
def find_by_name_and_parent(name, parent):
    return collection.find_one({
        "filename": name,
        "parent": parent
    })


