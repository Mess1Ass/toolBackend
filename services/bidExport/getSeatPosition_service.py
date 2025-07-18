

def get_seat_positon(theater_name, bid_type, bid_count = 0):
    if "SNHbirthday" in theater_name and bid_count == 71 and bid_type == "普站":
        return get_seat_positon_SNH_birthday(bid_type)
    elif "SNHbirthday" in theater_name and bid_count == 76 and bid_type == "普站":
        return get_seat_positon_SNH(bid_type)
    elif "SNHbirthday" in theater_name:
        return get_seat_positon_SNH_birthday(bid_type)
    elif "SNH" in theater_name :
        return get_seat_positon_SNH(bid_type)
    elif "HGH" in theater_name:
        return get_seat_positon_HGH(bid_type)
    elif "BEJ" in theater_name:
        return get_seat_positon_BEJ(bid_type)
    elif "MINILIVE" in theater_name:
        return get_seat_positon_MiniLive(bid_count)
    elif "拍立得" in theater_name:
        return get_seat_positon_pld(bid_count)
    elif "生日会" in theater_name:
        return get_seat_positon_birthparty(bid_count)
    elif "全纪录" in theater_name:
        return get_seat_positon_xiezhen(bid_count)
    elif "其它" in theater_name:
        return get_seat_positon_other(bid_count)


def get_seat_positon_SNH(bid_type):
    """根据竞价类型和索引为每个竞价分配座位号"""
    seats = []
    
    # 普座
    if bid_type == "普座":
        rows_6_col_1_18 = [f"6排{j}" for j in range(1, 19)]  # 6排1到6排18
        rows_5_6_col_19_20 = [f"{i}排{j}" for i in range(5, 7) for j in range(19, 21)]  # 5排18、19 | 6排18、19
        rows_4_6_col_21_22 = [f"{i}排{j}" for i in range(4, 7) for j in range(21, 23)]  # 4排21、22 | 5排21、22 | 6排21、22
        rows_3_6_col_23_24 = [f"{i}排{j}" for i in range(3, 7) for j in range(23, 25)]  # 3排23、24 | 4排23、24 | 5排23、24 | 6排23、24
        rows_7_10 = [f"{i}排{j}" for i in range(7, 11) for j in range(1, 25)]  # 7排到10排
        seats = rows_6_col_1_18 + rows_5_6_col_19_20 + rows_4_6_col_21_22 + rows_3_6_col_23_24 + rows_7_10  # 普座座位
    elif bid_type == "SVIP":
        seats = [f"1排{i}" for i in range(1, 25)]  # 摄影座位
    elif bid_type == "VIP":
        seats = [f"{i}排{j}" for i in range(2, 6) for j in range(1, 25 - 2 * (i - 2))]  # VIP座位
        # seats = seats[:84]  # 限制为84个
    elif bid_type == "摄影":
        seats = [f"1排{i}" for i in range(1, 25)]  # 摄影座位
    elif bid_type == "杆位":
        seats = [str(i) for i in range(1, 25)]  # 杆位座位
    elif bid_type == "普站":
        seats = [str(i) for i in range(25, 101)]  # 普站座位
    elif bid_type == "超级":
        seats = ["中", "左", "右"] 
    
    return seats

def get_seat_positon_SNH_birthday(bid_type):
    """根据竞价类型和索引为每个竞价分配座位号"""
    seats = []
    # 普座
    if bid_type == "普座":
        rows_6_col_1_18 = [f"6排{j}" for j in range(1, 19)]  # 6排1到6排18
        rows_5_6_col_19_20 = [f"{i}排{j}" for i in range(5, 7) for j in range(19, 21)]  # 5排18、19 | 6排18、19
        rows_4_6_col_21_22 = [f"{i}排{j}" for i in range(4, 7) for j in range(21, 23)]  # 4排21、22 | 5排21、22 | 6排21、22
        rows_3_6_col_23_24 = [f"{i}排{j}" for i in range(3, 7) for j in range(23, 25)]  # 3排23、24 | 4排23、24 | 5排23、24 | 6排23、24
        rows_7_col_1_19 = [f"7排{j}" for j in range(1, 21) if j % 2 != 0]   #7排1、3、5、7、9、11、13、15、17、19
        rows_7_col_21_24 = [f"7排{j}" for j in range(21, 25)]           #7排21、22、23、24
        rows_8_10 = [f"{i}排{j}" for i in range(8, 11) for j in range(1, 25)]  # 8排到10排
        seats = rows_6_col_1_18 + rows_5_6_col_19_20 + rows_4_6_col_21_22 + rows_3_6_col_23_24 + rows_7_col_1_19 + rows_7_col_21_24 + rows_8_10  # 普座座位
    elif bid_type == "VIP":
        rows_2_col_2_10 = [f"2排{j}" for j in range(1, 11) if j % 2 == 0]
        rows_2_col_11_24 = [f"2排{j}" for j in range(11, 25)]
        rows_3_5 = [f"{i}排{j}" for i in range(3, 6) for j in range(1, 25 - 2 * (i - 2))]  # VIP座位
        seats = rows_2_col_2_10 + rows_2_col_11_24 + rows_3_5
        # seats = seats[:84]  # 限制为84个
    elif bid_type == "摄影":
        seats = [f"1排{i}" for i in range(1, 25)]  # 摄影座位
    elif bid_type == "杆位":
        seats = [str(i) for i in range(1, 25)]  # 杆位座位
    elif bid_type == "普站":
        stand_25_30 = [str(i) for i in range(25, 31)]  # 普站座位
        stand_31_100 = [str(i) for i in range(36, 101)]
        seats = stand_25_30 + stand_31_100
    elif bid_type == "超级":
        seats = ["中", "左", "右"]
    
    return seats

def get_seat_positon_HGH(bid_type):
    """根据竞价类型和索引为每个竞价分配座位号"""
    seats = []
    
    # 普座
    if bid_type == "超级":
        rows_1_col_1_25 = [f"1排{j}" for j in range(1, 26)]  # 1排1到1排25
        rows_2_col_1_29 = [f"2排{j}" for j in range(1, 30)]  # 2排1到2排29
        seats = rows_1_col_1_25 + rows_2_col_1_29  # 普座座位
    elif bid_type == "VIP":
        rows_3_5_col_1_29 = [f"{i}排{j}" for i in range(3, 6) for j in range(1, 30)]  # 3排1到29 至5排1到29
        rows_6_col_1_19 = [f"6排{j}" for j in range(1, 20)]  # 6排1到19
        seats = rows_3_5_col_1_29 + rows_6_col_1_19 # 限制为84个
    elif bid_type == "普座":
        rows_6_col_20_29 = [f"6排{j}" for j in range(20, 30)]  # 6排20到29
        rows_7_10_col_1_29 = [f"{i}排{j}" for i in range(7, 11) for j in range(1, 30)]  # 7排1到29 至10排1到29
        rows_11_col_20_29 = [f"11排{j}" for j in range(20, 30)]  # 11排20到29
        rows_12_13_col_1_29 = [f"{i}排{j}" for i in range(12, 14) for j in range(1, 30)]  # 12排1到29 至13排1到29
        rows_14_col_1_19 = [f"14排{j}" for j in range(1, 31)]  # 14排1到30
        seats = rows_6_col_20_29 + rows_7_10_col_1_29 + rows_11_col_20_29 + rows_12_13_col_1_29 +rows_14_col_1_19 
    elif bid_type == "摄影":
        seats = [f"11排{i}" for i in range(1, 20)]  # 摄影座位
    
    return seats

def get_seat_positon_BEJ(bid_type):
    """根据竞价类型和索引为每个竞价分配座位号"""
    seats = []
    
    # 普座
    if bid_type == "超级":
        seats = ["中", "左", "右"]
    elif bid_type == "VIP":
        rows_1_4 = [f"{i}排{j}" for i in range(1, 5) for j in range(1, 18)]  # VIP座位
        rows_5 = [f"5排3"] + [f"5排{j}" for j in range(5, 18)]  # VIP座位
        rows_6 = [f"6排13"] + [f"6排{j}" for j in range(15, 18)]  # VIP座位
        seats = rows_1_4 + rows_5 + rows_6  # 限制为84个
    elif bid_type == "摄影":
        # rows_6_col_5_12 = [f"6排{i}" for i in range(5, 13)]  # 摄影座位
        seats = [f"6排3"]+ [f"6排6"] + [f"6排5"] + [f"6排8"] + [f"6排7"] + [f"6排10"] + [f"6排9"] + [f"6排12"] + [f"6排11"] + [f"6排14"]
    
    return seats

def get_seat_positon_MiniLive(bid_number):
    """根据竞价类型和索引为每个竞价分配座位号"""
    seats = []
    seats = [str(i) for i in range(1, bid_number + 1)]  # MINILIVE座位
    
    return seats

def get_seat_positon_pld(bid_number):
    """根据竞价类型和索引为每个竞价分配座位号"""
    seats = []
    seats = [str(i) for i in range(1, bid_number + 1)]  # 拍立得位置
    
    return seats

def get_seat_positon_birthparty(bid_number):
    """根据竞价类型和索引为每个竞价分配座位号"""
    seats = []
    seats = [str(i) for i in range(1, bid_number + 1)]  # 冷餐座位
    
    return seats

def get_seat_positon_xiezhen(bid_number):
    """根据竞价类型和索引为每个竞价分配座位号"""
    seats = []
    seats = [str(i) for i in range(1, bid_number + 1)]  # 拍立得位置
    
    return seats

def get_seat_positon_other(bid_number):
    """根据竞价类型和索引为每个竞价分配座位号"""
    seats = []
    seats = [str(i) for i in range(1, bid_number + 1)]  # 拍立得位置
    return seats
