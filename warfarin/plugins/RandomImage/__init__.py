import re

from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment, GroupMessageEvent

from nonebot.plugin import on_regex, on_command
from .sqlite_image import *
from .get_image import *
# from .search_time import *

driver: nonebot.Driver = nonebot.get_driver()

send_Setu = on_regex(r"hso", priority=1)


@driver.on_startup
async def startup():
    await engine.create_all()


@send_Setu.handle()
async def send_image(bot: Bot, event):
    n = MessageEvent.get_plaintext(event)
    keyword = "setu"
    if n := re.match(r"hso[*=\s]?([0-9]*)?", n):
        if n[1]:
            num = int(n[1])
            msg = None
            if 0 < num <= 10:
                for i in range(num):
                    msg += await get_local_image(num, keyword)
                await add_sqlite(event, Setu, msg, keyword)
                await send_Setu.finish(msg)
                # await send_Setu.send(message="发完了")
            else:
                await send_Setu.finish("要得太多了可不给发的喔(上限是十张)")
        else:
            msg = await get_local_image(1, "setu")
            await add_sqlite(event, Setu, msg, keyword)
            await send_Setu.finish(msg)
    else:
        await send_Setu.finish(None)


async def get_local_image(num=1, kind="setu"):
    image = await get_image(kind)
    logger.debug("image = " + image)
    return MessageSegment.image(image)


async def add_sqlite(event, db, msg, keyword):
    logger.debug("logging = " + str(msg))
    msg_list = re.findall(r"file=(.*?),cache=true", str(msg))
    if isinstance(event, GroupMessageEvent):
        if group_id := re.match(r"group_([0-9]*)?_", GroupMessageEvent.get_session_id(event)):
            for i in msg_list:
                await engine.add(db,
                                 {"Group_id": int(group_id[1]),
                                  "user_id": int(MessageEvent.get_user_id(event)),
                                  "image": i,
                                  "type": keyword
                                  })
            logger.debug("已添加群组信息进入数据库")
    else:
        for i in msg_list:
            await engine.add(db,
                             {"Group_id": "0",
                              "user_id": int(MessageEvent.get_user_id(event)),
                              "image": i,
                              "type": keyword
                              })
        logger.debug("已添加私聊信息进入数据库")
# "time": datetime.datetime.now()
