import random
import os
from nonebot.adapters.mirai2 import Bot, Event, MessageSegment, MessageChain

import nonebot
from .config import Config
from nonebot.log import logger

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

setuPath = str(plugin_config.setupath)
realPath = str(plugin_config.realpath)
wallpaperPath = str(plugin_config.wallpaperpath)
logger.debug("setuPath = " + setuPath + "\nrealPath = " + realPath + "\nwallpaperPath = " + wallpaperPath)


def random_pic(base_path: str) -> str:
    path_dir = os.listdir(base_path)
    # logger.debug("path_dir = " + str(path_dir))
    path = random.sample(path_dir, 1)[0]
    return str(base_path) + path


async def get_image(kind="setu"):
    if kind == "setu":
        choice_kinds = random.choice(['setu', 'setu', 'setu', 'real'])
    elif kind == "wallpaper":
        choice_kinds = 'wallpaper'
    else:
        choice_kinds = random.choice(['setu', 'real', 'wallpaper'])
    image_path = f"{os.getcwd()}/error/path_not_exists.png"
    if choice_kinds == 'setu':
        base_path = setuPath + os.sep
        logger.debug("setuPath = " + str(base_path))
        image_path = random_pic(base_path)
    if choice_kinds == 'real':
        base_path = realPath + os.sep
        image_path = random_pic(base_path)
    if choice_kinds == 'wallpaper':
        base_path = wallpaperPath + os.sep
        image_path = random_pic(base_path)
    logger.debug("image_path = " + image_path)
    return image_path


async def get_local_image(num=1, keyword="setu"):
    img_name = ""
    if 0 < num <= 1:
        msg = []
        for i in range(num):
            # msg += await get_local_image(num, keyword)
            # image_path = "".join(await get_image(keyword))
            img_name = await get_image(keyword)
            msg.append(MessageSegment.image(path=img_name))

    else:
        # msg = MessageSegment.plain("要得太多了可不给发的喔(上限是十张)")
        msg = MessageSegment.plain("要得再多了也不会给你发的喔(上限是一张)")

    return msg, img_name
