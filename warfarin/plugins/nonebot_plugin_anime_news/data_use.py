from pathlib import Path
import json
from .time import what_time, is_today, get_time_date
from txt2img.txt2img import Txt2Img
from nonebot.adapters.mirai2 import MessageSegment
import datetime
import os


def get_to_day_anime():
    """
    获取今日播放的番剧

    Returns: str

    """
    path = Path(__file__).parent
    data_file = str(path) + os.sep + "anime_list" + os.sep + "data.json"
    to_day_anime = ""
    with open(data_file, 'r', encoding='UTF-8') as f:
        info_data = json.load(f)
        try:
            for anime in info_data['timeline']['date']:
                time = datetime.datetime.strptime(anime['startDate']
                                                  , '%Y-%m-%dT%H:%M:%S.%fZ') + datetime.timedelta(hours=8)
                if is_today(time):
                    to_day_anime = to_day_anime + f"《{anime['headline'][40:-4]}》\n播出时间: {time}" + "\n\n"
        except:
            to_day_anime = f"今天没有番剧更新，明天再来问吧..."
    return to_day_anime


def get_season_anime_list():
    """
    获取本季度番剧列表

    Returns: MessageSegment

    """
    path = Path(__file__).parent
    data_file = str(path) + os.sep + "anime_list" + os.sep + "bangumi_season.json"
    season_anime = "本季度新番表\n"
    with open(data_file, 'r', encoding='UTF-8') as f:
        info_data = json.load(f)
        try:
            for num, anime in enumerate(info_data['items'], start=1):
                season_anime = season_anime + f"[{num}]标题：《{anime['title']}》\n" \
                                              f"译名：{anime['titleTranslate']}\n"
            font_size = 32
            title = "本季度新番表"
            text = season_anime
            img = Txt2Img(font_size)
            pic = img.save(title, text)
            res = MessageSegment.image(base64=pic)
        except:
            res = f"好像出问题，联系管理员问问吧..."
        return res
