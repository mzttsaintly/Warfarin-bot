import datetime
import re
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot import on_command, logger, require, get_bot
from sqlalchemy.sql.expression import select, and_
from .sqlite_image import engine, Setu
from .get_image import get_local_image

send_count = on_command('count', priority=1)
scheduler = require("nonebot_plugin_apscheduler").scheduler


async def search_sqlite_in_table_by_where(table_and_column, search_equation):
    """
    从表中搜索符合条件的数据
    table_and_column: 表名和表内的项目名，可填多个(Setu.Group_id, Setu.user_id, Setu.time etc.)
    search_equation: 搜索的条件,填写关系式，如(Setu.time > f"{datetime.date.now()}")
                     若需要填写多个关系式请用and_()连接；如and_(Setu.time > f"{datetime.date.today()}",
                                                       Setu.Group_id == f"{group_id}")
    """
    # today = datetime.date.today()
    # tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    res = await engine.load_all(select(table_and_column).where(search_equation))
    return res


@send_count.handle()
async def count_image_one_day(bot: Bot, event):
    if isinstance(event, GroupMessageEvent):
        group_ids = re.match(r"group_([0-9]*)?_", GroupMessageEvent.get_session_id(event))
        group_id = group_ids[1]
    else:
        group_id = "0"
    res = await search_sqlite_in_table_by_where((Setu.Group_id, Setu.time, Setu.user_id)
                                                , and_(Setu.time > f"{datetime.date.today()}",
                                                       Setu.Group_id == f"{group_id}"))
    image_amount = len(res)
    logger.debug("数量" + str(image_amount))
    if image_amount == 0:
        msg = "今天居然一张涩图都没发出来?!太过分了，你们都被资本家吸干了血汗了么?"
    elif 0 < image_amount < 20:
        msg = f"今天发出去的图都不到20张啊,米娜桑,要打起精神来喔"
    elif image_amount >= 20:
        msg = f"本群今日已请求{image_amount}份涩图,请再接再厉,都不要停下来啊"
    elif image_amount >= 100:
        msg = f"今天你们居然看了{image_amount}张图欸,不知道有没有看到重复的呢"
    else:
        msg = "啊嘞,不知道为什么居然查不到数据呢"
    await send_count.finish(msg)



# @scheduler.scheduled_job("cron", minute="*", day="*", id="setu")


@scheduler.scheduled_job("cron", minute="30", hour="23", day="*", id="setu")
async def scheduler_aqiang_reply(group="970243035"):
    bot = get_bot("983107785")
    res = await search_sqlite_in_table_by_where((Setu.Group_id, Setu.time, Setu.user_id)
                                                , and_(Setu.time > f"{datetime.date.today()}",
                                                       Setu.Group_id == f"{group}"))
    image_amount = len(res)
    # logger.debug("数量" + str(image_amount))
    if image_amount == 0:
        msg = "今天居然一张涩图都没发出来?!太过分了，你们都被资本家吸干了血汗了么?"
    elif 0 < image_amount < 20:
        msg = f"截止至现在,今天发出去的图都不到20张啊,米娜桑,要打起精神来喔"
    elif image_amount >= 20:
        msg = f"截止至现在,本群今日已请求{image_amount}份涩图,请再接再厉,不可以停下来啊"
    elif image_amount >= 100:
        msg = f"截止至现在,今天你们居然看了{image_amount}张图欸,不知道有没有看到重复的呢"
    else:
        msg = "啊嘞,不知道为什么居然查不到数据呢"
    if image_amount >= 10:
        await bot.call_api("send_group_msg", **{"message": f"{msg}", "group_id": "970243035"})
    else:
        msg = f"截止至现在,今天发出去的图都不到10张啊,你们不要我就自己发了咯"
        await bot.call_api("send_group_msg", **{"message": f"{msg}", "group_id": "970243035"})
        for i in range(10 - image_amount):
            auto_setu = await get_local_image(1, "setu")
            await bot.call_api("send_group_msg", **{"message": auto_setu, "group_id": "970243035"})
