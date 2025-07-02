import requests
from models.user import User
from config import LOGIN_ENDPOINT
from playwright.sync_api import sync_playwright

def login_user(user: User) -> list:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://user.48.cn/Login/index.html", timeout=120000, wait_until="domcontentloaded")
        page.click("xpath=/html/body/div[1]/div/div[1]/div/ul/li[1]/a")
        page.wait_for_selector("xpath=/html/body/div[1]/div/div[2]/form/div[1]/input")

        # 填写登录表单
        page.fill('xpath=/html/body/div[1]/div/div[2]/form/div[1]/input', user.username)      # 用户名
        page.fill('xpath=//html/body/div[1]/div/div[2]/form/div[2]/input', user.password)      # 密码
        page.click('xpath=/html/body/div[1]/div/div[2]/form/a')          # 登录按钮


        # 等待登录跳转成功
        page.wait_for_url("https://user.48.cn/", timeout=10000)

        # 登录后访问 user.48.cn 获取 cookie
        page.goto("https://shop.48.cn/pai")
        cookies = context.cookies("https://shop.48.cn/pai")
        browser.close()

        # 返回字典格式的 cookies
        return cookies

