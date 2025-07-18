# db_util.py
from pymongo import MongoClient
import config

# 初始化连接（全局只初始化一次）
_client = MongoClient(config.MONGO_URI)
_db = _client[config.MONGO_DB]

def get_db():
    """获取 MongoDB 数据库实例"""
    return _db

def get_collection(name=None):
    """
    获取指定的集合（collection），默认用配置里的集合
    :param name: 集合名，不传则使用默认配置
    """
    if name:
        return _db[name]
    return _db[config.MONGO_COLLECTION]
