import requests
import json
from bs4 import BeautifulSoup
from .bidExport.bidExport_service import (
    parse_good_detail_html, export_one_item_data)

def get_shop_page(total_count, brand_id, cookie_str, page_num: int = 1):
    cookies = {}
    for pair in cookie_str.split(";"):
        if "=" in pair:
            key, val = pair.strip().split("=", 1)
            cookies[key] = val


    url = "https://shop.48.cn/pai"
    params = {
        "totalCount": total_count,
        "pageNum": page_num,
        "brand_id": brand_id
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=10)
        response.raise_for_status()
        return response.text, None  # 返回 HTML 页面内容
    except Exception as e:
        return None, str(e)
    


def parse_shop_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = []

    for box in soup.select(".gs_xx"):
        item = {}
        a_tag = box.select_one(".gs_1 a")
        if a_tag:
            href = a_tag.get("href")
            href = href[0] if isinstance(href, list) else href
            if href:
                item["item_id"] = href.split("/")[-1]
                item["url"] = "https://shop.48.cn" + href

        img_tag = box.select_one(".gs_1 img")
        if img_tag:
            item["image"] = img_tag["src"]

        title_tag = box.select_one(".gs_2 a")
        if title_tag:
            item["title"] = title_tag.text.strip()

        price_tag = box.select_one(".gs_4 .jg")
        if price_tag:
            item["price"] = price_tag.text.strip()

        bid_count_tag = box.select_one(".gs_6 .ic_cj")
        if bid_count_tag:
            item["bid_count"] = bid_count_tag.text.strip()

        status_tag = box.select_one(".gs_6 span:nth-of-type(2)")
        if status_tag:
            item["status"] = status_tag.text.strip().replace("竞价状态：", "")

        items.append(item)

    return {
        "count": len(items),
        "items": items
    }

def get_good_detail(url, cookie_str):
    cookies = {}
    for pair in cookie_str.split(";"):
        if "=" in pair:
            key, val = pair.strip().split("=", 1)
            cookies[key] = val

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Referer": "https://shop.48.cn/pai"
    }

    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        response.raise_for_status()
        # print(response.text)
        return response.text, None  # 返回 HTML 页面内容
    except Exception as e:
        return None, str(e)
    
def export_items_excel(data, cookies, output_stream):
    html, err = get_good_detail(data["url"], cookies)
    max_bid_num, theater_str, bid_type, excelName = parse_good_detail_html(html)
    export_one_item_data(data["itemId"], cookies, max_bid_num, theater_str, bid_type, excelName, output_stream)
    return excelName, None
