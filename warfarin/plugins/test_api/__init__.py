import time
from nonebot import logger, on_message
from nonebot.adapters.mirai2 import MessageSegment, Bot, Event, GroupMessage

# test_message = on_message(priority=5)


# @test_message.handle()
async def testapi(bot: Bot, event: Event):
    name = event.get_event_name()
    logger.debug(f"event_name = {name}")

    description = event.get_event_description()
    logger.debug(f"description = {description}")

    message = event.get_message()
    logger.debug(f"message = {message}")

    plain = event.get_plaintext()
    logger.debug(f"plain = {plain}")

    user_id = event.get_user_id()
    logger.debug(f"user_id = {user_id}")

    session_id = event.get_session_id()
    logger.debug(f"session_id = {session_id}")

    message_type = event.get_type()
    logger.debug(f"message_type = {message_type}")

    message_dict = event.normalize_dict()
    message_time = message_dict['source']['time']
    time_tup = time.strptime(message_time, "%Y-%m-%dT%H:%M:%S+00:00")
    logger.debug(f"message_time = {message_time}")
    logger.debug(f"时间数组为 {time_tup}")
    logger.debug(f"时间戳为 {time.mktime(time_tup)}")

    if isinstance(event, GroupMessage):
        message_group_id = event.normalize_dict()["sender"]["group"]["id"]
        logger.debug(f"group_id = {message_group_id}")

    # await test_message.finish(None)
