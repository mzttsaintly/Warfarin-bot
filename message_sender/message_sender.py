import nonebot
from nonebot import get_bot

bot_qq = nonebot.get_driver().config.mirai_qq[0]


async def send_group_msg(msg, group_id: int):
    """
    将消息发送至指定群组
    Args:
        msg: 发送的内容(str, MessageSegment)
        group_id: 需要发送至的群组id

    Returns: None

    """
    bot = get_bot(str(bot_qq))
    await bot.send_group_message(message_chain=[msg], target=group_id)
