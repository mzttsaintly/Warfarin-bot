import datetime
import hashlib
import json
import os

import nonebot
from nonebot import logger
from nonebot.adapters.mirai2 import Bot, MessageSegment, Event
from nonebot.plugin import on_keyword

driver: nonebot.Driver = nonebot.get_driver()

keyword = on_keyword({"求签", "电子观音"}, priority=5)


@keyword.handle()
async def sensojiluckpick(bot: Bot, event: Event):
    """浅草寺求签，移植自獭爹bot"""
    qq_id = event.get_user_id()
    # logger.info(str(qq_id))
    random_num = await get_pape_num(qq_id)
    path = os.path.join(f"{os.getcwd()}", "warfarin", "plugins", "Luckpick", "Luck.json")
    with open(path, 'r', encoding='utf-8') as luck_data:
        data = json.load(luck_data)[random_num]['fields']['text']
    format_data = ["---每人每天可以抽一次哟---\n\n", data, '抽到凶签也不要气馁，明天还可以继续抽喔']
    content = "".join(format_data)
    await keyword.finish(content)


async def get_pape_num(qq_id):
    today = datetime.date.today()
    format_today = int(today.strftime('%y%m%d'))
    str_num = str(format_today * qq_id)

    md5 = hashlib.md5()
    md5.update(str_num.encode('utf-8'))
    res = md5.hexdigest()

    return int(res.upper(), 16) % 100
