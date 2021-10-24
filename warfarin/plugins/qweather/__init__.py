import re

import nonebot
from nonebot.plugin import on_regex
from nonebot.adapters.mirai import Bot, MessageEvent, MessageChain, MessageSegment
from nonebot.log import logger

from .getweather import *


weather = on_regex(r'(.*)天气$', priority=1)


@weather.handle()
async def send_weather_message(bot: Bot, event: MessageEvent):
    n = MessageEvent.get_plaintext(event)
    logger.debug(n)
    if n := re.match(r'(.*)天气$', n, re.I):
        logger.debug(n)
        if n[1]:
            city_name = str(n[1])
            logger.debug(city_name)
            msg = await now_weather(city_name)
            await weather.finish(MessageSegment.plain(msg))
        else:
            await weather.finish(None)
