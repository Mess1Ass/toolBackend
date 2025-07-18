from bs4 import BeautifulSoup
from lxml import etree
import re


def get_seat_type(item_name):
    """根据商品名称判断座位类型"""
    # 根据商品名称判断座位类型
    if "超级" in item_name:
        return "超级"
    elif "SVIP" in item_name:
        return "SVIP"
    elif "摄影" in item_name:
        return "摄影"
    elif "杆位" in item_name:
        return "杆位"
    elif "普站" in item_name:
        return "普站"
    elif "VIP" in item_name:
        return "VIP"
    elif "普座" in item_name:
        return "普座"  
    elif "MINILIVE" in item_name:
        return "MINILIVE"
    elif "拍立得" in item_name or "百场徽章粉丝纪念礼盒" in item_name:
        return "拍立得"
    elif "生日会" in item_name:
        return "生日会"
    elif "全纪录" in item_name:
        return "全纪录"
    else:
        return "其他"
    

# 定义一个函数来计算站区座位数
def calculate_seat_count(pattern_1, pattern_2, text):
    # 匹配单一区间
    matches_1 = re.findall(pattern_1, text)
    # 匹配多个区间
    matches_2 = re.findall(pattern_2, text)

    total_seats = 0
    print(matches_1, matches_2)
    # 如果有单一区间
    if matches_1:
        for match in matches_1:
            start, end = map(int, match)  # 转换为整数
            total_seats += (end - start + 1)  # 计算区间内的座位数

    # 如果有多个区间
    elif matches_2:
        for match in matches_2:
            start, end = map(int, match[:2])  # 第一个区间
            total_seats += (end - start + 1)  # 计算第一个区间的座位数

            # 处理第二个区间（如果存在）
            if match[2] and match[3]:
                start2, end2 = map(int, match[2:4])  # 第二个区间
                total_seats += (end2 - start2 + 1)

    return total_seats


#获取SNH剧场竞价门票数量
def get_bid_number_SNH(goodDetail_text, bid_type):

    if "普站" in bid_type:
        # 正则表达式匹配座位区间（例如“025至100”或“025至30、36至100”）
        seat_pattern_1 = r"站区序号(\d{3})至(\d{3})"  # 单一区间（如：025至100）
        seat_pattern_2 = r"站区序号(\d{3})至(\d{2})(?:、(\d{2})至(\d{3}))*"  # 多个区间（如：025至30、36至100）
        seat_count = calculate_seat_count(seat_pattern_1, seat_pattern_2, goodDetail_text)
        return seat_count


    #如果是生公
    if "生日潮流包" in goodDetail_text:
        # 根据商品名称判断座位类型
        if "SVIP" in bid_type:
            return 24
        elif "VIP" in bid_type:
            return 79
        elif "摄影" in bid_type:
            return 24
        elif "杆位" in bid_type:
            return 24
        elif "超级" in bid_type:
            return 3
        elif "普座" in bid_type:
            return 122
        return 0
    else:
        # 根据商品名称判断座位类型
        if "SVIP" in bid_type:
            return 24
        elif "VIP" in bid_type:
            return 84
        elif "摄影" in bid_type:
            return 24
        elif "杆位" in bid_type:
            return 24
        elif "超级" in bid_type:
            return 3
        elif "普座" in bid_type:
            return 132
        return 0



#获取杭州剧场竞价门票数量
def get_bid_number_HGH(bid_type):
    # 根据商品名称判断座位类型
    if "VIP" in bid_type:
        return 106
    elif "超级" in bid_type:
        return 54
    elif "普座" in bid_type:
        return 224
    elif "摄影" in bid_type:
        return 19
    return 0
    
#获取MINILIVE竞价门票数量    
def get_bid_number_MiniLive(html):
    tree = etree.fromstring(html, parser=etree.HTMLParser())
    span_elements = tree.xpath('//*[@id="TabTab03Con1"]/span')

    # 使用正则表达式提取所有票数信息，只需包含 "演出门票"
    if span_elements:
        ticket_counts = re.findall(r"入场资格(\d+)位", span_elements[0].text or "")

    # 如果找到了票数信息
    if ticket_counts:
        total_tickets = int(ticket_counts[0])  # 取第一个匹配的票数
        return total_tickets
    else:
        return 0
    
#获取竞价拍立得数量
def get_bid_number_pld(goodDetail_text):

    # 使用正则表达式提取所有票数信息，只需包含 "演出门票"
    ticket_counts = re.findall(r".*?共.*?(\d+)套", goodDetail_text)

    # 如果找到了票数信息
    if ticket_counts:
        total_tickets = int(ticket_counts[0])  # 取第一个匹配的票数
        return total_tickets
    else:
        return 0
    
    #获取竞价拍立得数量
def get_bid_number_birthparty(goodDetail_text, theater_name):
    if("SNH" in theater_name):
        # 使用正则表达式提取所有票数信息，只需包含 "演出门票"
        ticket_counts = re.findall(r".*?名额：.*?(\d+)名", goodDetail_text)
        # 如果找到了票数信息
        if ticket_counts:
            total_tickets = int(ticket_counts[0])  # 取第一个匹配的票数
            return total_tickets
        else:
            return 0
    elif("BEJ" in theater_name):
        # 使用正则表达式提取所有票数信息，只需包含 "演出门票"
        ticket_counts = re.findall(r".*?竞拍数量：.*?(\d+)张", goodDetail_text)
        # 如果找到了票数信息
        if ticket_counts:
            total_tickets = int(ticket_counts[0])  # 取第一个匹配的票数
            return total_tickets
        else:
            return 0
        
def get_bid_number_xiezhen(goodDetail_text):
    # 使用正则表达式提取所有票数信息，只需包含 "演出门票"
    ticket_counts = re.findall(r".*?共.*?(\d+)套", goodDetail_text)

    # 如果找到了票数信息
    if ticket_counts:
        total_tickets = int(ticket_counts[0])  # 取第一个匹配的票数
        return total_tickets
    else:
        return 0
    
def get_bid_number_other(goodDetail_text):

    # 使用正则表达式提取所有票数信息，只需包含 "演出门票"
    ticket_counts1 = re.findall(r".*?共.*?(\d+)套", goodDetail_text)

    ticket_counts2 = re.findall(r".*?仅.*?(\d+)套", goodDetail_text)

    # 如果找到了票数信息
    if ticket_counts1:
        total_tickets = int(ticket_counts1[0])  # 取第一个匹配的票数
        return total_tickets
    elif ticket_counts2:
        total_tickets = int(ticket_counts2[0])  # 取第一个匹配的票数
        return total_tickets
    else:
        return 0