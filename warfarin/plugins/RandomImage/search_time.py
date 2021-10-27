import datetime
from nonebot.adapters.cqhttp import Bot
from nonebot import on_command
from .sqlite_image import engine, Setu


send_count = on_command('count', priority=1)


@send_count.handle()
async def count_sqlite(bot: Bot, event):
    res = await search_sqlite_of_time(Setu, "time")
    await send_count.finish(str(res))


async def search_sqlite_of_time(table_and_column, search_key):
    today = datetime.date.today()
    # tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    pass


