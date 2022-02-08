from nonebot.plugin import on_regex
from nonebot.adapters.mirai2 import MessageSegment, Bot, Event

from .get_image import *
from .on_time import *
# from .sqlite_image import *
from orm.sqlite import *

driver: nonebot.Driver = nonebot.get_driver()

send_Setu = on_regex(r"hso", priority=1)
# send_SFW = on_regex(r"sfw", priority=1)


@driver.on_startup
async def startup():
    await engine.create_all()


# @send_SFW.handle()
@send_Setu.handle()
async def send_image(bot: Bot, event: Event):
    n = event.get_plaintext()
    if setu_key := re.match(r"hso[*=\s]?([0-9]*)?", n):
        keyword = "setu"
        if setu_key[1]:
            num = int(setu_key[1])
            # msg = None
            msg = await get_local_image(num, keyword)
            # await add_sqlite(event, Setu, msg, keyword)
            await send_Setu.finish(msg)
            # await send_Setu.send(message="发完了")

        else:
            msg = await get_local_image(1, keyword)
            # await add_sqlite(event, Setu, msg, keyword)
            await send_Setu.finish(msg)
    elif girl_key := re.match(r"sfw[*=\s]?([0-9]*)?", n):
        keyword = "wallpaper"
        if n[1]:
            num = int(girl_key[1])
            # msg = None
            msg = await get_local_image(num, keyword)
            # await add_sqlite(event, Setu, msg, keyword)
            await send_Setu.finish(msg)
            # await send_Setu.send(message="发完了")

        else:
            msg = await get_local_image(1, keyword)
            # await add_sqlite(event, Setu, msg, keyword)
            await send_Setu.finish(msg)
    else:
        await send_Setu.finish(None)


# async def add_sqlite(event, db, msg, keyword):
#     logger.debug("logging = " + str(msg))
#     msg_list = re.findall(r"file=(.*?),cache=true", str(msg))
#     if isinstance(event, GroupMessageEvent):
#         if group_id := re.match(r"group_([0-9]*)?_", GroupMessageEvent.get_session_id(event)):
#             for i in msg_list:
#                 await engine.add(db,
#                                  {"Group_id": int(group_id[1]),
#                                   "user_id": int(MessageEvent.get_user_id(event)),
#                                   "image": i,
#                                   "type": keyword
#                                   })
#             logger.debug("已添加群组信息进入数据库")
#     else:
#         for i in msg_list:
#             await engine.add(db,
#                              {"Group_id": "0",
#                               "user_id": int(MessageEvent.get_user_id(event)),
#                               "image": i,
#                               "type": keyword
#                               })
#         logger.debug("已添加私聊信息进入数据库")
