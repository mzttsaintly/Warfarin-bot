import re

from nonebot.adapters.mirai2 import MessageEvent, MessageSegment
from nonebot.plugin import on_regex
from nonebot.exception import FinishedException

from . import config
from .img import build_get_share_info, build_video_poster
from .utils import *
from .analysis_app import b23_extract

share_av_sort_url = on_regex(
    r"(b23.tv)|(bili(22|23|33|2233).cn)|(.bilibili.com)|(^(av|cv)(\d+))|(^BV([a-zA-Z0-9]{10})+)|(\[\[QQ小程序\]哔哩哔哩\])|("
    r"QQ小程序&amp;#93;哔哩哔哩)|(QQ小程序&#93;哔哩哔哩)",
    flags=re.I,
)


@share_av_sort_url.handle()
async def _(event: MessageEvent):
    n = event.get_message()
    if re.search(r"B站动态|点击前往", str(n)):
        return
    video_info = None
    # 分享链接,从中提取短链接
    try:
        if video_url := await b23_extract(str(n)):
            bv_id = re.search(r"BV[*=\s]?(\w*)", video_url)
            av_id = await bv_to_av(bv_id[0])
            video_info = await get_video_info(av_id)
    # 聊天内容中有av号或BV号
    except TypeError:
        n = n.extract_plain_text()
        # 匹配av号
        if av_id := re.search(r"av[*=\s]?(\d*)", n):
            video_info = await get_video_info(av_id[1])
            # 匹配网页连接中的BV号
        elif bv_id := re.search(r"BV[*=\s]?(\w*)", n):
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
