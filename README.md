服务器启动flask项目流程 <br>
进入toolBackend文件夹 <br>
source venv/bin/activate <br>
pm2 start "venv/bin/gunicorn -w 4 app:app -b 0.0.0.0:5000" --name backend <br>
pm2 logs backend <br>
安装所需依赖（pip install -r requirements.txt ） <br>
服务器配置： <br>
sudo apt update <br>
sudo apt install nginx <br>
创建配置文件: <br>
sudo nano /etc/nginx/sites-available/48api.tool4me.cn <br>
写入以下内容： <br>
server { <br>
    listen 80; <br>
    server_name 48api.tool4me.cn; <br>
    location / { <br>
        proxy_pass http://127.0.0.1:5000; <br>
        proxy_set_header Host $host; <br>
        proxy_set_header X-Real-IP $remote_addr; <br>
    } <br>
} <br>
保存并创建链接启用配置： <br>
sudo ln -s /etc/nginx/sites-available/48api.tool4me.cn /etc/nginx/sites-enabled/ <br>
sudo nginx -t <br>
sudo systemctl reload nginx <br>

✅ 解决方案：启动 Nginx 服务 <br>
请执行以下命令： <br>
sudo systemctl start nginx <br>
然后查看是否启动成功： <br>
sudo systemctl status nginx <br>

🧩 第三步：配置 HTTPS（强烈推荐） <br>
安装 certbot： <br>
sudo apt install certbot python3-certbot-nginx <br>
申请 HTTPS 证书： <br>
sudo certbot --nginx -d 48api.tool4me.cn <br>



nginx<br>
location / {<br>
    # 处理 CORS 预检请求<br>
    if ($request_method = OPTIONS) {<br>
        add_header 'Access-Control-Allow-Origin' 'https://tool4me.vercel.app' always;<br>
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;<br>
        add_header 'Access-Control-Allow-Headers' 'Origin, Content-Type, Accept, Authorization' always;<br>
        add_header 'Access-Control-Allow-Credentials' 'true' always;<br>
        add_header 'Access-Control-Max-Age' 3600 always;<br>
        add_header 'Content-Length' 0;<br>
        add_header 'Content-Type' 'text/plain; charset=UTF-8';<br>
        return 204;<br>
    }<br>
<br>
    # 正常代理 Flask<br>
    proxy_pass http://127.0.0.1:5000;<br>
    proxy_set_header Host $host;<br>
    proxy_set_header X-Real-IP $remote_addr;<br>
<br>
    # CORS 响应头<br>
    add_header 'Access-Control-Allow-Origin' 'https://tool4me.vercel.app' always;<br>
    add_header 'Access-Control-Allow-Headers' 'Origin, Content-Type, Accept, Authorization' always;<br>
    add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;<br>
    add_header 'Access-Control-Allow-Credentials' 'true' always;<br>
}<br>




