import nonebot
from nonebot import get_bot
from nonebot.exception import TypeMisMatch
from nonebot.adapters.mirai2.message import MessageSegment, MessageChain

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
    if isinstance(msg, MessageSegment):
        await bot.send_group_message(message_chain=[msg], target=group_id)
    elif isinstance(msg, MessageChain):
        await bot.send_group_message(message_chain=msg, target=group_id)
    elif isinstance(msg, list):
        await bot.send_group_message(message_chain=msg, target=group_id)
    elif isinstance(msg, str):
        plain = MessageSegment.plain(text=msg)
        await bot.send_group_message(message_chain=[plain], target=group_id)
    else:
        raise TypeMisMatch


async def send_group_msgchain(msg, group_id: int):
    """

    Args:
        msg: 发送的内容(MessageChain)
        group_id: 需要发送至的群组id

    Returns:

    """
    bot = get_bot(str(bot_qq))
    await bot.send_group_message(message_chain=msg, target=group_id)


async def send_friend_msg(msg, friend_id: int):
    """
    将消息发送至指定好友

    Args:
        msg: 发送的内容(str, MessageSegment),不能是MessageChain
        friend_id: 需要发送至的好友qq号

    Returns:

    """
    bot = get_bot(str(bot_qq))
    if isinstance(msg, MessageSegment):
        await bot.send_friend_message(target=friend_id, message_chain=[msg])
    elif isinstance(msg, MessageChain):
        await bot.send_friend_message(target=friend_id, message_chain=msg)
    elif isinstance(msg, list):
        await bot.send_friend_message(target=friend_id, message_chain=msg)
    elif isinstance(msg, str):
        plain = MessageSegment.plain(text=msg)
        await bot.send_friend_message(target=friend_id, message_chain=[plain])
    else:
        raise TypeMisMatch
