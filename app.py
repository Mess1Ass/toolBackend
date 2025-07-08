from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from controllers.login_controller import login_blueprint
from controllers.file_controller import file_bp

app = Flask(__name__)
CORS(app)

# 初始化 Swagger 文档
swagger = Swagger(app)

# 注册接口蓝图
app.register_blueprint(login_blueprint)
app.register_blueprint(file_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
