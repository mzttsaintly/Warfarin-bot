import requests
import json
from typing import Tuple
import os
from pathlib import Path
from nonebot.exception import NetworkError, IgnoredException, ParserExit, FinishedException

from nonebot import logger

path = Path(__file__).parent
if not os.path.isfile(str(path) + os.sep + "data" + os.sep + "up" + os.sep + "up.json"):
    logger.info("还没有关注的up喔")
    try:
        os.makedirs(str(path) + os.sep + "data" + os.sep + "up")
    except FileExistsError:
        pass
else:
    logger.info("up列表加载成功!")

baseUrl = 'https://api.bilibili.com/x/space/arc/search?mid={}&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp'
biliUserInfoUrl = 'https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1'
}


def get_latest_video(uid: str, last_post_time: int):
    """
    根据uid和时间戳查询用户是否有视频更新

    Args:
        uid: 查询的用户uid
        last_post_time: 文件中的最新时间戳

    Returns: 返回一个元组[是否更新, 标题，bv号，视频长度，封面的链接， 发布时间戳]

    """
    response = requests.get(url=baseUrl.format(uid), headers=header)
    if response.status_code == 200:
        pass
    else:
        raise NetworkError
    response = json.loads(response.text)
    if len(response['data']['list']['vlist']) == 0:
        raise IgnoredException

    latest_video = response['data']['list']['vlist'][0]
    post_time = int(latest_video['created'])
    title = latest_video['title']
    bvid = latest_video['bvid']
    length = latest_video['length']
    pic = latest_video['pic']
    if post_time > last_post_time:
        return True, title, bvid, length, pic, post_time
    else:
        return False, title, bvid, length, pic, post_time


def init_up_info(uid: str):
    """
    根据uid获取up名字和最后更新时间戳

    Args:
        uid: 需要关注的uid

    Returns: up名字, 最后更新时间戳

    """
    response = requests.get(url=biliUserInfoUrl.format(uid), headers=header)
    response = json.loads(response.text)
    if response['code'] == 0:
        up_name = response['data']['name']
        latest_update = get_latest_video(uid, 0)
        return up_name, latest_update[5]
    else:
        raise ParserExit


async def follow_up_modify(uid: str):
    """
    根据指令关注up

    Args:
        uid: 需关注的uid

    Returns: None

    """
    if not uid.isdigit():
        raise ParserExit
    up_path = str(path) + os.sep + "data" + os.sep + "up" + os.sep + "up.json"
    if os.path.exists(up_path):
        logger.debug("up关注列表已存在")
        with open(up_path, "r+", encoding='UTF-8') as f:
            try:
                up_info = json.load(f)
            except Exception as e:
                logger.debug(e)
                up_info = {}
            logger.debug("正在读取文件")
            if uid in up_info:
                logger.debug("up已存在于关注列表")
            else:
                name, latest_update = init_up_info(uid)
                up_info[uid] = [name, latest_update]
                f.seek(0)
                f.truncate()
                json.dump(up_info, f, ensure_ascii=False)
                logger.debug("已添加up")
    else:
        logger.debug("尚未创建关注列表")
        with open(up_path, "w+", encoding='UTF-8') as f:
            name, latest_update = init_up_info(uid)
            up_info = {uid: [name, latest_update]}
            json.dump(up_info, f, ensure_ascii=False)
        logger.debug("已创建关注列表")


async def unfollow_up_modify(uid: str):
    """
    根据命令取消关注up

    Args:
        uid: 需取关的uid

    Returns: None

    """
    if not uid.isdigit():
        raise ParserExit
    up_path = str(path) + os.sep + "data" + os.sep + "up" + os.sep + "up.json"
    if os.path.exists(up_path):
        with open(up_path, "r+", encoding='UTF-8') as f:
            up_info = json.load(f)
            logger.debug("正在读取文件")
            if uid in up_info:
                logger.debug("up已存在于关注列表")
                up_info.pop(uid)
                f.seek(0)
                f.truncate()
                json.dump(up_info, f, ensure_ascii=False)
            else:
                logger.debug("此up不在关注列表中")
                raise ParserExit
    else:
        logger.debug("关注列表不存在")
        raise ParserExit


async def check_ups_update(uid: str) -> Tuple[bool, str, str]:
    """
    根据uid检查up是否有视频更新

    Args:
        uid: 需检查的uid

    Returns: 是否更新，更新内容，封面url

    """
    if not uid.isdigit():
        uid = await check_watch(uid)
    up_path = str(path) + os.sep + "data" + os.sep + "up" + os.sep + "up.json"
    with open(up_path, "r+", encoding='UTF-8') as f:
        up_info = json.load(f)
        if uid not in up_info:
            raise ParserExit
        up_name = up_info[uid][0]
        logger.debug(f"查询对象为{up_name}")
        latest_update = int(up_info[uid][1])
        logger.debug(f"上次更新时间戳为{latest_update}")
        res = get_latest_video(uid, latest_update)
        title = res[1]
        bvid = res[2]
        time = res[3]
        pic_url = res[4]
        post_time = res[5]
        if res[0]:
            up_info[uid][1] = int(post_time)
            f.seek(0)
            f.truncate()
            json.dump(up_info, f, ensure_ascii=False)
            msg = f"[B站动态]\n{up_name} 更新了\n标题：{title}\n时长：{time}\n链接：https://www.bilibili.com/video/{bvid}"
            return True, msg, pic_url
        else:
            msg = f"{up_name} 尚未更新\n最后更新视频标题：{title}\n时长：{time}\n链接：https://www.bilibili.com/video/{bvid}"
            return False, msg, pic_url


async def check_watch(name: str):
    """
    根据关注列表中的名字查询uid
    Args:
        name: 所关注up的名称

    Returns: 列表中对应的uid

    """
    up_path = str(path) + os.sep + "data" + os.sep + "up" + os.sep + "up.json"
    with open(up_path, "r", encoding='UTF-8') as f:
        up_info = json.load(f)
        for key in up_info:
            if up_info[key][0] == name:
                return key
        raise FinishedException


async def check_list():
    """
    返回当前关注的所有up

    Returns: 一个包含当前关注列表中所有up的dict

    """
    up_path = str(path) + os.sep + "data" + os.sep + "up" + os.sep + "up.json"
    with open(up_path, "r", encoding='UTF-8') as f:
        up_info = json.load(f)
    return up_info

