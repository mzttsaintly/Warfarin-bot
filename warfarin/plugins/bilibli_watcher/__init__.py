import os
import json
from pathlib import Path
import re

import nonebot
from nonebot import get_driver, on_command, on_message, require, permission
from nonebot import logger
from nonebot.exception import ParserExit, FinishedException
from message_sender.message_sender import send_group_msg

from nonebot.adapters.mirai2 import MessageSegment, Event

from .vedio_info import follow_up_modify, unfollow_up_modify, check_ups_update

path = Path(__file__).parent
group = nonebot.get_driver().config.group
scheduler = require("nonebot_plugin_apscheduler").scheduler

follow_up = on_command("followup", aliases={"关注up"}, block=True)


@follow_up.handle()
async def follow_up(event: Event):
    """
    根据命令关注up

    Args:
        event: 所接收的事件

    Returns: None

    """
    uid = event.get_plaintext().split()
    logger.debug(f"收到指令：{uid}")
    await follow_up_modify(uid[1])
    await follow_up.finish(f"已关注{uid[1]}")


unfollow_up = on_command("unfollow-up", aliases={"取关up"}, block=True)


@unfollow_up.handle()
async def unfollow_up(event: Event):
    """

    Args:
        event: 所接收的事件

    Returns: None

    """
    uid = event.get_plaintext().split()
    logger.debug(f"收到指令：{uid}")
    await unfollow_up_modify(uid[1])

manual_check = on_command("check_update", aliases={"查询更新"}, block=True)


@manual_check.handle()
async def manual_check_update(event: Event):
    uid = event.get_plaintext().split()
    logger.debug(f"收到指令：{uid}")
    try:
        res = await check_ups_update(uid[1])
        msg = [MessageSegment.plain(res[1]), MessageSegment.image(url=res[2])]
        await manual_check.finish(msg)
    except ParserExit:
        await manual_check.finish("不能查询未关注的up")


@scheduler.scheduled_job("cron", minute="*/3", day="*")
async def auto_check_update():
    up_path = str(path) + os.sep + "data" + os.sep + "up" + os.sep + "up.json"
    wait_list = []
    with open(up_path, "r+", encoding='UTF-8') as f:
        up_info = json.load(f)
        for _ in up_info:
            wait_list.append(_)
    logger.debug(f"等待查询的列表{wait_list}")
    for i in wait_list:
        res = await check_ups_update(i)
        if res[0]:
            msg = [MessageSegment.plain(res[1]), MessageSegment.image(url=res[2])]
            for j in group:
                await send_group_msg(msg, int(j))
        else:
            pass
