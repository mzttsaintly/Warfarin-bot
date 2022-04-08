from .data_use import get_to_day_anime, get_season_anime_list
from .get import get_data, get_new_season_data

import os
from pathlib import Path

from nonebot.permission import SUPERUSER
from nonebot import on_command, on_regex, logger, require, get_driver
from message_sender.message_sender import send_group_msg

path = Path(__file__).parent
group = get_driver().config.group

if not os.path.isfile(str(path) + os.sep + "anime_list" + os.sep + "data.json"):
    try:
        os.mkdir(str(path) + os.sep + "anime_list")
    except FileExistsError:
        pass
    get_data()
    get_new_season_data()
    logger.info("创建存储用json并成功加载插件!")
else:
    logger.info("番剧时间表加载成功!")

today_anime = on_regex(r'^(今日|今天|今)+.*(新番|番|动漫|番剧)+', priority=5, block=True)

scheduler = require("nonebot_plugin_apscheduler").scheduler


@today_anime.handle()
async def handle():
    """
    获取当日新番列表

    Returns: None

    """
    msg = get_to_day_anime()
    await today_anime.finish(msg)


@scheduler.scheduled_job("cron", minute="30", hour="22", day="*")
async def auto_send_anime():
    """
    定时向设定的群聊发送当日新番列表

    Returns: None

    """
    msg = get_to_day_anime()
    for i in group:
        await send_group_msg(msg, int(i))


get_anime = on_command('get anime', aliases={"更新番剧时间表"}, permission=SUPERUSER, priority=5, block=True)


@get_anime.handle()
async def handle():
    """
    更新番剧时间表

    Returns: None

    """
    msg = get_data()
    await get_anime.finish(msg)


@scheduler.scheduled_job("cron", hour="*/2")
async def news():
    get_data()

new_anime_season = on_command('new season', aliases={"更新季度表"}, permission=SUPERUSER, priority=5, block=True)


@new_anime_season.handle()
async def handle():
    """
    手动更新季度新番表

    Returns: None

    """
    msg = get_new_season_data()
    await new_anime_season.finish(msg)


@scheduler.scheduled_job("cron", day="1")
async def get_bangumi_season():
    """
    更新季度新番表

    Returns: None

    """
    get_season_data()

get_season_data = on_command('get season', aliases={"番剧季度表"}, priority=5, block=True)


@get_season_data.handle()
async def get_season_list():
    """
    获得本季度新番列表

    Returns: None

    """
    msg = get_season_anime_list()
    await get_season_data.finish(msg)
