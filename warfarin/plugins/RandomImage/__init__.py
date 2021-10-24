import re

from nonebot.adapters.mirai import Bot, MessageEvent, MessageChain
from nonebot.plugin import on_regex

from .get_image import *

keyword = on_regex(r"hso", priority=1)


@keyword.handle()
async def send_image(bot: Bot, event: MessageEvent):
    n = MessageEvent.get_plaintext(event)
    logger.debug(n)
    if n := re.match(r"hso[*=\s]?([0-9]*)?", n):
        if n[1]:
            num = int(n[1])

            if 0 < num <= 10:
                for i in range(num):
                    await get_ten_image(num, "setu")
                await keyword.finish(message="发完了")
            else:
                return await keyword.finish(MessageSegment.plain(text="要得太多了可不给发的喔(上限是十张)"))
        else:
            await get_ten_image(1, "setu")
    else:
        await keyword.finish(None)


async def get_ten_image(num=1, kind="setu"):
    image = await get_image(kind)
    logger.debug("image = " + image)
    pro_path = os.path.relpath(image, "Z:\\mcl-1.2.2\\data\\net.mamoe.mirai-api-http\\images\\")
    await keyword.send(MessageSegment.image(path=pro_path))
