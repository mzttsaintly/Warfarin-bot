import datetime
from nonebot.adapters.cqhttp import Bot
from nonebot import on_command
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.functions import count
from .sqlite_image import engine, Setu


send_count = on_command('count', priority=1)


@send_count.handle()
async def count_image_oneday(bot: Bot, event):
    res = await search_sqlite_in_table_by_where((Setu.Group_id, Setu.user_id, Setu.time), Setu.time > f"{datetime.date.today()}")
    con = len(res)
    await send_count.finish(con)


async def search_sqlite_in_table_by_where(table_and_column, search_equation):
    """
    从表中搜索符合条件的数据
    table_and_column: 表名和表内的项目名，可填多个(Setu.Group_id, Setu.user_id, Setu.time etc.)
    search_equation: 搜索的条件,填写关系式，如(Setu.time > f"{datetime.date.now()}")
    """
    today = datetime.date.today()
    # tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    res = engine.load_all(select(table_and_column).where(search_equation))
    return res
