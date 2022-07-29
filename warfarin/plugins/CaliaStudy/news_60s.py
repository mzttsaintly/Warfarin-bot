import nonebot
import aiohttp
from nonebot.adapters.mirai2 import MessageSegment, MessageChain
from nonebot import on_regex, require, get_bot, logger
from message_sender.message_sender import send_group_msg


group = nonebot.get_driver().config.group
logger.debug(f"group = {group}")


today_news = on_regex(r'^(今日|今天|今)+.*(新闻)+', priority=5, block=True)
scheduler = require("nonebot_plugin_apscheduler").scheduler


@today_news.handle()
async def send_news():
    msg = await get_news()
    await today_news.finish(msg)


@scheduler.scheduled_job("cron", hour="8", minute="5", day="*")
async def daily_news():
    msg = await get_news()
    for _ in group:
        await send_group_msg(msg, int(_))


async def get_news():
    try:
        url = "https://api.2xb.cn/zaob"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res_session:
                res = await res_session.json()
        lst = res['imageUrl']
        pic_ti = MessageSegment.image(url=lst)
        return pic_ti
    except:
        url = "https://api.iyk0.com/60s"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res_session:
                res = await res_session.json()
        lst = res['imageUrl']
        pic_ti = MessageSegment.image(url=lst)
        return pic_ti


def remove_unprintable_chars(s):
    return ''.join(x for x in s if x.isprintable())  # 去除imageUrl可能存在的不可见字符
