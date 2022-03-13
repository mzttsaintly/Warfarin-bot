# coding=utf-8
from nonebot import logger
import requests
from pathlib import Path
import os


def get_data():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56',
               'accept-language': 'zh-CN'
               }
    proxies = {"http": None, "https": None}

    web_data = requests.get("https://bangumi.moe/api/bangumi/timeline", headers=headers, timeout=2, proxies=proxies)

    if web_data.status_code == 200:
        logger.info("新番时间表更新成功")
        data = web_data.content.decode()
        path = Path(__file__).parent
        data_file = str(path) + os.sep + "anime_list" + os.sep + "data.json"
        with open(data_file, 'w', encoding='UTF-8') as f:
            f.write(data)
        return f"更新成功"
    else:
        logger.warning(f"新番时间表更新失败 web code:{web_data.status_code}")
        return f"更新失败 web code:{web_data.status_code}"
