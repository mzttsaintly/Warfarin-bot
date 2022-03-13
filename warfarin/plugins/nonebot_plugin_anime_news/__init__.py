from .data_use import get_to_day_anime
from .get import get_data

import os
from pathlib import Path

from nonebot.permission import SUPERUSER
from nonebot import on_command, on_regex, logger, require
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event

path = Path(__file__).parent

if not os.path.isfile(str(path) + os.sep + "anime_list" + os.sep + "data.json"):
    os.mkdir(str(path) + os.sep + "anime_list")
    get_data()
    logger.info("创建存储用json并成功加载插件!")
else:
    logger.info("番剧时间表加载成功!")

today_anime = on_regex(r'^(今日|今天|今)+.*(新番|番|动漫|番剧)+', priority=5, block=True)
get_anime = on_command('get anime', aliases={"更新番剧时间表"}, permission=SUPERUSER, priority=5, block=True)

scheduler = require("nonebot_plugin_apscheduler").scheduler


@today_anime.handle()
async def handle(
        bot: Bot,
        event: Event
):
    msg = get_to_day_anime()
    await today_anime.finish(msg)


@get_anime.handle()
async def handle(
        bot: Bot,
        event: Event
):
    msg = get_data()
    await get_anime.finish(msg)


@scheduler.scheduled_job("cron", hour="*/2")
async def news():
    get_data()
