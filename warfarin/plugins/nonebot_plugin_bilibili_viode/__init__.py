import re

from nonebot.adapters.mirai2 import MessageEvent, MessageSegment
from nonebot.plugin import on_regex
from nonebot.exception import FinishedException

from . import config
from .img import build_get_share_info, build_video_poster
from .utils import *
from .analysis_app import bili_keyword

share_av_sort_url = on_regex(
    r"(b23.tv)|(bili(22|23|33|2233).cn)|(.bilibili.com)|(^(av|cv)(\d+))|(^BV([a-zA-Z0-9]{10})+)|(\[\[QQ小程序\]哔哩哔哩\])|(QQ小程序&amp;#93;哔哩哔哩)|(QQ小程序&#93;哔哩哔哩)",
    flags=re.I,
)


@share_av_sort_url.handle()
async def _(event: MessageEvent):
    n = event.get_message()
    # print("str = ", n)
    # if re.search(r"(b23.tv)|(bili(22|23|33|2233).cn)", text, re.I):
    if re.search(r'"desc":".*?"', str(n)):
        video_info = await get_video_info(await bili_keyword(str(n)))
        msg = await deal_video_info(video_info)
        await share_av_sort_url.finish(msg)
    n = n.extract_plain_text()
    # print("after extract_text = ", n)
    if av_id := re.match(r"av[*=\s]?(\d*)?", n):
        video_info = await get_video_info(av_id[1])
    elif bv_id := re.match(r"BV[*=\s]?(.*)?", n):
        av_id = await bv_to_av(bv_id[0])
        video_info = await get_video_info(av_id)
    else:
        raise FinishedException
    msg = await deal_video_info(video_info)
    await share_av_sort_url.finish(msg)


async def deal_video_info(video_info):
    tem_img = await build_video_poster(video_info)
    # img = await build_get_share_info(video_info)
    if img:
        msg = [MessageSegment.image(base64=tem_img), MessageSegment.plain(
            "\n点击前往:" + video_info.shareUrl
        )]
    else:
        raise FinishedException
    return msg
