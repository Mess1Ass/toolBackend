服务器启动flask项目流程 <br>
进入toolBackend文件夹 <br>
source venv/bin/activate <br>
pm2 start "gunicorn -w 4 app:app -b 0.0.0:5000" --name backend <br>
pm2 logs backend <br>
安装所需依赖（pip install ） <br>
