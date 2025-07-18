import requests
import datetime
from models.user import (
    find_user, insert_user, update_user,
    get_collection
)
from urllib.parse import urlparse, parse_qs
from playwright.sync_api import sync_playwright

def login_user(user: dict):
    username = user.get("username", "")
    password = user.get("password", "")

    try:
        existing = find_user(username)

        if existing and existing["password"] == password:
            if existing.get("expired_at") and existing["expired_at"] > datetime.datetime.now():
                print("使用缓存 cookie")
                return existing["cookies"], existing["totalCount"], existing["brand_id"], 200
            else:
                print("cookie 过期，重新登录")
        else:
            print("用户不存在或密码不匹配，重新登录")

        # 登录逻辑
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            context = browser.new_context()
            page = context.new_page()

            page.goto("https://user.48.cn/Login/index.html", timeout=120000, wait_until="domcontentloaded")
            page.click("xpath=/html/body/div[1]/div/div[1]/div/ul/li[1]/a")
            page.wait_for_selector("xpath=/html/body/div[1]/div/div[2]/form/div[1]/input", timeout=5000)

            page.fill('xpath=/html/body/div[1]/div/div[2]/form/div[1]/input', username)
            page.fill('xpath=//html/body/div[1]/div/div[2]/form/div[2]/input', password)
            page.click('xpath=/html/body/div[1]/div/div[2]/form/a')

            page.wait_for_url("https://user.48.cn/**", timeout=10000)
            page.wait_for_timeout(3000)
            page.goto("https://shop.48.cn/pai")
            page.wait_for_selector('a[href*="totalCount"]', timeout=10000)
            
            href = page.get_attribute('a[href*="totalCount"]', "href")

            totalCount, brand_id = None, None
            if href:
                query = urlparse(href).query
                params = parse_qs(query)
                totalCount = int(params.get("totalCount", [0])[0])
                brand_id = int(params.get("brand_id", [0])[0])

            cookies = context.cookies(["https://user.48.cn", "https://shop.48.cn", "https://.48.cn"])


            page.wait_for_timeout(5000)
            browser.close()

            # 更新数据库
            update_user(username, password, cookies, totalCount, brand_id)

            return cookies, totalCount, brand_id, 200

    except Exception as e:
        return str(e), None, None, 500

