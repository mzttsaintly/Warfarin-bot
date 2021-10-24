import random
import os

import nonebot
from nonebot.log import logger
from nonebot.adapters.mirai import MessageSegment


setuPath = "Z:\\boynextdoor\\bin\\res\\img\\ero\\"
realPath = "Z:\\boynextdoor\\bin\\res\\img\\real\\"
wallpaperPath = "Z:\\boynextdoor\\bin\\res\\img\\wallpaper\\"
logger.debug(setuPath)
logger.debug(realPath)
logger.debug(wallpaperPath)


def random_pic(base_path: str) -> str:
    path_dir = os.listdir(base_path)
    # logger.debug("path_dir = " + str(path_dir))
    path = random.sample(path_dir, 1)[0]
    return str(base_path) + path


async def get_image(kind="setu"):
    if kind == "setu":
        choice_kinds = random.choice(['setu', 'setu', 'real'])
    elif kind == "wallpaper":
        choice_kinds = 'wallpaper'
    else:
        choice_kinds = random.choice(['setu', 'real', 'wallpaper'])
    image_path = f"{os.getcwd()}/error/path_not_exists.png"
    if choice_kinds == 'setu':
        base_path = setuPath
        logger.debug("setuPath = " + str(base_path))
        image_path = random_pic(base_path)
    if choice_kinds == 'real':
        base_path = realPath
        image_path = random_pic(base_path)
    if choice_kinds == 'wallpaper':
        base_path = wallpaperPath
        image_path = random_pic(base_path)
    logger.debug("image_path = " + image_path)
    return image_path
