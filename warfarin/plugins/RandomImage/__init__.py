import re
import datetime

from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment

from nonebot.plugin import on_regex

import nonebot
from .config import Config

from .get_image import *

keyword = on_regex(r"hso", priority=1)
export = nonebot.require("nonebot_plugin_navicat")
db = export.sqlite_pool


@keyword.handle()
async def send_image(bot: Bot, event: MessageEvent):
    n = MessageEvent.get_plaintext(event)
    if n := re.match(r"hso[*=\s]?([0-9]*)?", n):
        if n[1]:
            num = int(n[1])
            msg = None
            if 0 < num <= 10:
                for i in range(num):
                    msg += await get_local_image(num, "setu")
                await keyword.finish(msg)
                await keyword.send(message="发完了")
            else:
                await keyword.finish("要得太多了可不给发的喔(上限是十张)")
        else:
            msg = await get_local_image(1, "setu")
            await keyword.finish(msg)
    else:
        await keyword.finish(None)


async def get_local_image(num=1, kind="setu"):
    image = await get_image(kind)
    logger.debug("image = " + image)
    return MessageSegment.image(image)
