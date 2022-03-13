from pathlib import Path
import json
from .time import what_time, is_today, get_time_date
import datetime
import os


def get_to_day_anime():
    path = Path(__file__).parent
    data_file = str(path) + os.sep + "anime_list" + os.sep + "data.json"
    data = open(data_file, 'r', encoding='UTF-8')
    info_data = json.load(data)
    to_day_anime = ""
    try:
        for anime in info_data['timeline']['date']:
            time = datetime.datetime.strptime(anime['startDate'], '%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=8)
            if is_today(time):
                to_day_anime = to_day_anime + f"《{anime['headline'][40:-4]}》\n播出时间: {time}" + "\n\n"
    except:
        to_day_anime = f"今天没有番剧更新，明天再来问吧..."
    return to_day_anime
