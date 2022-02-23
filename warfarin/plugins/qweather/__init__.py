import re

import nonebot
from nonebot.plugin import on_regex
from nonebot.adapters.mirai2 import Bot, Event, MessageSegment


from .getweather import *


weather = on_regex(r'(.*)天气$', priority=4)


@weather.handle()
async def send_weather_message(event: Event):
    n = event.get_plaintext()
    logger.debug(n)
    if n := re.match(r'(.*)天气$', n, re.I):
        logger.debug(n)
        if n[1]:
            city_name = str(n[1])
            logger.debug(city_name)
            msg = await now_weather(city_name)
            await weather.finish(msg)
        else:
            await weather.finish(None)
