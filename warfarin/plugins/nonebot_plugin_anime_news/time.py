import datetime

'''
引入
'''


def get_time_list() -> list:
    a = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '0:00', '%Y-%m-%d%H:%M')
    # 中间是凌晨
    b = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '5:00', '%Y-%m-%d%H:%M')
    # 中间是早晨
    c = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '8:00', '%Y-%m-%d%H:%M')
    # 中间是上午
    d = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:00', '%Y-%m-%d%H:%M')
    # 中间是中午
    e = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '13:00', '%Y-%m-%d%H:%M')
    # 中间是下午
    f = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '16:00', '%Y-%m-%d%H:%M')
    # 中间是傍晚
    g = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '19:00', '%Y-%m-%d%H:%M')
    # 中间是晚上
    h = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '23:59', '%Y-%m-%d%H:%M')
    return [a, b, c, d, e, f, g, h]


def is_today(time) -> bool:
    """
    是否是今日
    使用: is_time(time)
    """
    time_list = get_time_list()
    if time_list[0] < time < time_list[7]:
        return True
    else:
        return False


def is_month(time: str) -> bool:
    """
    是否在这个月
    使用: is_month(time)
    time : %Y-%m-%d %H:%M:%S
    """
    if (datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')).month == datetime.datetime.now().month:
        return True
    else:
        return False


def is_year(time: str) -> bool:
    """
    是否在这一年
    使用: is_year(time)
    """
    if (datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')).year == datetime.datetime.now().year:
        return True
    else:
        return False


def what_time() -> str:
    """
    时间段判断
    使用: xxx = what_time()
    """
    time_list = get_time_list()
    time = datetime.datetime.now()
    if time_list[0] < time < time_list[1]:
        now_time = f"凌晨"
    elif time_list[1] < time < time_list[2]:
        now_time = f"早晨"
    elif time_list[2] < time < time_list[3]:
        now_time = f"上午"
    elif time_list[3] < time < time_list[4]:
        now_time = f"中午"
    elif time_list[4] < time < time_list[5]:
        now_time = f"下午"
    elif time_list[5] < time < time_list[6]:
        now_time = f"傍晚"
    else:
        now_time = f"晚上"
    return now_time


def get_time_date() -> str:
    """
    获取当前日期
    格式xxxx-xx-xx
    使用: get_time(time)
    """
    time = str(datetime.datetime.now().date())
    return time
