import json
import re
from typing import List, Tuple
from nonebot import on_command
from nonebot.exception import ParserExit
import requests
import os
from nonebot import get_bot
from nonebot import logger


async def create_user_file(user_file: str, ups=None, streamer=None):
    """
    创建用户文件

    Args:
        streamer: 关注的主播列表
        user_file: 保存的文件名
        ups: 关注的up列表

    Returns: None

    """
    if ups is None:
        ups = []
    if streamer is None:
        streamer = []
    with open(user_file, 'w+') as f:
        user_info = [streamer, ups]
        json.dump(user_info, f)
    logger.debug(f'用户文件{user_file}创建成功')


async def follow_modify(user_file: str, success_list: List[str], w_type: str):
    """

    Args:
        user_file:
        success_list:
        w_type:

    Returns: None

    """
    if w_type == "streamer":
        f_type = 0
    elif w_type == "ups":
        f_type = 1
    else:
        raise ParserExit
    logger.debug(f'正在打开用户文件{user_file}')
    with open(user_file, "r+") as f:
        user_info = json.load(f)
        user_info[f_type] += success_list
        f.seek(0)
        f.truncate()
        json.dump(user_info, f)
        logger.debug(f'用户文件更新成功')


async def unfollow_modify(user_file: str, success_list: List[str], w_type: str):
    """

    Args:
        user_file:
        success_list:
        w_type:

    Returns:

    """
    if w_type == "streamer":
        f_type = 0
    elif w_type == "ups":
        f_type = 1
    else:
        raise ParserExit
    logger.debug(f'正在打开用户文件{user_file}')
    with open(user_file, "r+") as f:
        user_info = json.load(f)
        user_info[f_type] = list(set(user_info[f_type]) - set(success_list))
        f.seek(0)
        f.truncate()
        json.dump(user_info, f)
        logger.debug(f'用户文件更新成功')
