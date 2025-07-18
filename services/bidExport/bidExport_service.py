import requests
import json
import random
import time
import re
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from .getBidNumber_service import ( get_seat_type, get_bid_number_SNH, get_bid_number_HGH,
    get_bid_number_MiniLive, get_bid_number_pld, get_bid_number_birthparty, 
    get_bid_number_xiezhen, get_bid_number_other)
from .getSeatPosition_service import get_seat_positon
from .saveAsExcel_service import save_excel

def parse_good_detail_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    theaterName = soup.find(class_="fl icon ic_1")
    goodDetail = soup.find(id = "TabTab03Con1")
    excelName = soup.find(class_="i_tit")
    titleName = soup.find(class_="i_tit")
    goodDetail_text = ""
    birthday = False

    if theaterName and titleName and excelName:
        theater_str = str(theaterName.get_text(strip=True))
        title_str = str(titleName.get_text(strip=True))
        excel_str = str(excelName.get_text(strip=True))

    if goodDetail:
        goodDetail_text = goodDetail.get_text(strip=True, separator='\n')

    if("生日潮流包" in goodDetail_text):
        birthday = True
    else:
        birthday = False

    bid_type = get_seat_type(title_str)
    if("SNH" in theater_str and "星梦剧院" in title_str and "MINILIVE" not in title_str and "礼包" in title_str):
        bidNumber = get_bid_number_SNH(goodDetail_text, bid_type)
        if(birthday):
            theater_str = "SNHbirthday"
    elif("SNH" in theater_str and "星梦空间" in title_str and "MINILIVE" not in title_str and "礼包" in title_str):
        bidNumber = get_bid_number_HGH(bid_type)
        theater_str = "HGH"
    elif("MINILIVE" in title_str):
        bidNumber = get_bid_number_MiniLive(html)
        theater_str = "MINILIVE"
    elif("拍立得" in title_str  or "百场徽章粉丝纪念礼盒" in title_str):
        bidNumber = get_bid_number_pld(goodDetail_text)
        theater_str = "拍立得"
    elif("生日会" in title_str):
        bidNumber = get_bid_number_birthparty(goodDetail_text, theater_str)
        theater_str = "生日会"
    elif("全纪录" in title_str):
        bidNumber = get_bid_number_xiezhen(goodDetail_text)
        theater_str = "全纪录"
    else:
        bidNumber = get_bid_number_other(goodDetail_text)
        theater_str = "其它"
    
    print(f"一共有{bidNumber}个位置 {theater_str}" )

    return bidNumber, theater_str, bid_type, excel_str


def check_bid_exist(bids_data, bidder):
    # print(bids_data)
    if len(bids_data) == 0:
        return True
    for bid in bids_data:
        if bidder in bid['出价人']:
            # 如果出价人已经存在，则返回False
            return False
    # 如果出价人不存在，则返回True
    return True


def export_one_item_data(itemId, cookie_str, maxBidNum, theaterStr, bid_type, excelName, output_stream):
    cookies = {}
    for pair in cookie_str.split(";"):
        if "=" in pair:
            key, val = pair.strip().split("=", 1)
            cookies[key] = val

    pageNum = 1
    total_bids = []
    bid_status = ""
    while True:
        url = "https://shop.48.cn/pai/GetShowBids"
        data = {
            "id": itemId,
            "numPerPage": 200,
            "pageNum": pageNum,
            "r": random.random()
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "Referer": "https://shop.48.cn/pai/item/26831",
            "Origin": "https://shop.48.cn",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

        try:
            response = requests.post(url, data=data, headers=headers, cookies=cookies, timeout=10)

            for item in response.json()["list"]:
                if check_bid_exist(total_bids, item["user_name"]):
                    if(item["auction_status"] == 1):
                        bid_status = "竞价成功"
                    else:
                        bid_status = "竞价失败"

                    match = re.search(r"\d+", item["bid_time"])
                    if match:
                        timestamp_ms = int(match.group())
                        dt_utc = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
                        dt_beijing = dt_utc.astimezone(timezone(timedelta(hours=8)))
                        dt_str = dt_beijing.strftime("%Y-%m-%d %H:%M:%S")

                    total_bids.append({"出价状态": bid_status, "出价人": item["user_name"], "出价时间": dt_str, "出价金额": str(item["bid_amt"])})

            if(pageNum < response.json()["PageCount"]):
                pageNum += 1
                time.sleep(1)
            else:
                
                break
        except Exception as e:
            raise
    
    #获取座位号的数组
    seats = get_seat_positon(theaterStr, bid_type, maxBidNum) or []  # 保证 seats 一定是 list

    # 为每条竞价记录按剧场分配座位号
    for idx, bid in enumerate(total_bids):
        bid["座位类型"] = bid_type
        if idx >= len(seats):
            bid["座位号"] = "竞价失败"
        else:
            bid["座位号"] = seats[idx]
    
    save_excel(total_bids, itemId, output_stream, excelName)
