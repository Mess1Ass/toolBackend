from pymongo import MongoClient
from bson.objectid import ObjectId
from utils.db_util import get_collection
import datetime


collection = get_collection("Accounts")

# 插入用户
def insert_user(username, password, cookies):
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)

    return collection.insert_one({
        "username": username,
        "password": password,
        "cookies": cookies,
        "created_at": now,
        "expired_at": expire
    })

# 根据电话号查找
def find_user(username):
    return collection.find_one({
        "username": username
    })

# 根据电话号和密码更新用户信息
def update_user(username, password, cookies, totalCount, brand_id):
    now = datetime.datetime.now()
    new_expired_at = datetime.datetime.now() + datetime.timedelta(days=1)
    result = collection.update_one(
        {"username": username},
        {"$set": {
            "password": password,
            "cookies": cookies,
            "created_at": now,
            "expired_at": new_expired_at,
            "totalCount": totalCount,
            "brand_id": brand_id
        }},
        upsert=True
    )
    return result.modified_count > 0  # True 表示更新成功




