from nonebot import logger, on_message
from nonebot.adapters.mirai2 import MessageSegment, Bot, Event

test_message = on_message(priority=1)


@test_message.handle()
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
