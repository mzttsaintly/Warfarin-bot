import os
import datetime
import hashlib
import json

import nonebot
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment, GroupMessageEvent

from nonebot.plugin import on_keyword


driver: nonebot.Driver = nonebot.get_driver()

keyword = on_keyword(set(["求签", "电子观音"]), priority=1)


@keyword.handle()
async def sensojiluckpick(bot: Bot, event: MessageEvent):
    """浅草寺求签，移植自獭爹bot"""
    qq_id = MessageEvent.get_user_id(event)
    random_num = await get_pape_num(qq_id)
    path = os.path.join(f"{os.getcwd()}", "warfarin", "plugins", "Luckpick", "Luck.json")
    with open(path, 'r', encoding='utf-8') as luck_data:
        data = json.load(luck_data)[random_num]['fields']['text']
    formatt_data = ["---每人每天可以抽一次哟---\n\n"]
    formatt_data.append(data)
    formatt_data.append('抽到凶签也不要气馁，明天还可以继续抽喔')
    content = "".join(formatt_data)
    await keyword.finish(content)


async def get_pape_num(qq_id):
    today = datetime.date.today()
    formattoday = int(today.strftime('%y%m%d'))
    strnum = str(formattoday * qq_id)

    md5 = hashlib.md5()
    md5.update(strnum.encode('utf-8'))
    res = md5.hexdigest()

    return int(res.upper(), 16) % 100
