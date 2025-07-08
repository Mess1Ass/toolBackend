服务器启动flask项目流程
进入toolBackend文件夹
source venv/bin/activate
pm2 start "gunicorn -w 4 app:app -b 0.0.0:5000" --name backend
pm2 logs backend
安装所需依赖（pip install ）
