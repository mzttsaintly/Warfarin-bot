import re
from nonebot.plugin import on_regex
from nonebot.adapters.mirai2 import MessageSegment, Bot, Event

from .get_image import *
# from .on_time import *
from orm.sqlite import *
from orm.tables import Setu

driver: nonebot.Driver = nonebot.get_driver()

send_Setu = on_regex(r"hso", priority=1)
send_SFW = on_regex(r"sfw", priority=1)


@driver.on_startup
async def startup():
    await engine.create_all()
    logger.debug("开始链接数据库")


@send_SFW.handle()
@send_Setu.handle()
async def send_image(bot: Bot, event: Event):
    n = event.get_plaintext()
    if setu_key := re.match(r"hso[*=\s]?([0-9]*)?", n):
        keyword = "setu"
        if setu_key[1]:
            num = int(setu_key[1])
            msg, image_name = await get_local_image(num, keyword)
            await add_sqlite(event, Setu, image_name, keyword)
            await send_Setu.finish(msg)

        else:
            msg, image_name = await get_local_image(1, keyword)
            await add_sqlite(event, Setu, image_name, keyword)
            await send_Setu.finish(msg)

    elif girl_key := re.match(r"sfw[*=\s]?([0-9]*)?", n):
        keyword = "wallpaper"
        if girl_key[1]:
            num = int(girl_key[1])
            # msg = None
            msg, image_name = await get_local_image(num, keyword)
            await add_sqlite(event, Setu, image_name, keyword)
            await send_Setu.finish(msg)

        else:
            msg, image_name = await get_local_image(1, keyword)
            await add_sqlite(event, Setu, image_name, keyword)
            await send_Setu.finish(msg)
    else:
        await send_Setu.finish(None)


async def add_sqlite(event, db, msg, keyword):
    logger.debug("logging = " + str(msg))
    user_id = int(event.get_user_id())
    session_id = event.get_session_id()
    if event.get_event_name() == "GroupMessage":
        group_id = int(re.match(r"group_([0-9]*)?_", session_id)[1])
    else:
        group_id = 0
    await engine.add(db,
                     {"Group_id": group_id,
                      "user_id": user_id,
                      "image": msg,
                      "type": keyword
                      })
    logger.debug("已添加信息进入数据库")

    # if isinstance(event, GroupMessageEvent):
    #     if group_id := re.match(r"group_([0-9]*)?_", GroupMessageEvent.get_session_id(event)):
    #         for i in msg_list:
    #             await engine.add(db,
    #                              {"Group_id": int(group_id[1]),
    #                               "user_id": int(MessageEvent.get_user_id(event)),
    #                               "image": i,
    #                               "type": keyword
    #                               })
    #         logger.debug("已添加群组信息进入数据库")
    # else:
    #     for i in msg_list:
    #         await engine.add(db,
    #                          {"Group_id": "0",
    #                           "user_id": int(MessageEvent.get_user_id(event)),
    #                           "image": i,
    #                           "type": keyword
    #                           })
    #     logger.debug("已添加私聊信息进入数据库")
