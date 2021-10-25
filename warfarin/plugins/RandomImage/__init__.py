import re
import datetime

from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment, GroupMessageEvent, PrivateMessageEvent

from nonebot.plugin import on_regex, on_metaevent
from .sqlite_image import *
from .get_image import *

driver: nonebot.Driver = nonebot.get_driver()

keyword = on_regex(r"hso", priority=1)


@driver.on_startup
async def startup():
    await engine.create_all()


@keyword.handle()
async def send_image(bot: Bot, event):
    n = MessageEvent.get_plaintext(event)
    if n := re.match(r"hso[*=\s]?([0-9]*)?", n):
        if n[1]:
            num = int(n[1])
            msg = None
            if 0 < num <= 10:
                for i in range(num):
                    msg += await get_local_image(num, "setu")
                await add_sqlite(event, msg)
                await keyword.finish(msg)
                await keyword.send(message="发完了")
            else:
                await keyword.finish("要得太多了可不给发的喔(上限是十张)")
        else:
            msg = await get_local_image(1, "setu")
            await add_sqlite(event, msg)
            await keyword.finish(msg)
    else:
        await keyword.finish(None)


async def get_local_image(num=1, kind="setu"):
    image = await get_image(kind)
    logger.debug("image = " + image)
    return MessageSegment.image(image)


async def add_sqlite(event, msg):
    if isinstance(event, GroupMessageEvent):
        await engine.add(Setu,
                         {"Group_id": GroupMessageEvent.get_session_id(event),
                          "user_id": int(MessageEvent.get_user_id(event)),
                          "image": str(msg),
                          "time": datetime.datetime.now()})
        logger.debug("已添加群组信息进入数据库")
    else:
        await engine.add(Setu,
                         {"Group_id": "0",
                          "user_id": int(MessageEvent.get_user_id(event)),
                          "image": str(msg),
                          "time": datetime.datetime.now()})
        logger.debug("已添加私聊信息进入数据库")
