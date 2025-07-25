import os



# 其他配置（例如最大上传大小，是否允许调试等）
MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 最大20MB文件

# 可选：你也可以添加数据库配置、CORS白名单等
LOGIN_ENDPOINT = 'https://user.48.cn/QuickLogin/login/'

MONGO_URI = "mongodb://admin:admin@106.14.212.1:27017"
MONGO_DB = "SNH48"
MONGO_COLLECTION = "admin"


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER_NAME = "uploads"
    # 其他配置（例如最大上传大小，是否允许调试等）
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 最大20MB文件
