import json
import os
import random

from nonebot import on_keyword, logger
from nonebot.adapters.mirai2 import MessageSegment, Bot, Event

tarot = on_keyword({"塔罗牌"}, priority=1)


@tarot.handle()
async def send_tarot(bot: Bot, event: Event):
    """塔罗牌"""
    card, filename = await get_random_tarot()
    image_dir = random.choice(['normal', 'reverse'])
    card_type = '正位' if image_dir == 'normal' else '逆位'
    content = f"{card['name']} ({card['name-en']}) {card_type}\n牌意：{card['meaning'][image_dir]}"
    elements = []
    img_path = os.path.join(f"{os.getcwd()}", "warfarin", "plugins", "Tarot", "resource", f"{image_dir}",
                            f"{filename}.jpg")
    logger.debug(f"塔罗牌图片:{img_path}")
    if filename and os.path.exists(img_path):
        elements.append(MessageSegment.image(path=img_path))
        elements.append(MessageSegment.plain(content))

    await tarot.finish(elements)


async def get_random_tarot():
    # path = f"{os.getcwd()}/warfarin/plugins/Tarot/resource/tarot.json"
    path = os.path.join(f"{os.getcwd()}", "warfarin", "plugins", "Tarot", "resource", "tarot.json")
    with open(path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    kinds = ['major', 'pentacles', 'wands', 'cups', 'swords']
    cards = []
    for kind in kinds:
        cards.extend(data[kind])
    card = random.choice(cards)
    filename = ''
    for kind in kinds:
        if card in data[kind]:
            filename = '{}{:02d}'.format(kind, card['num'])
            break
    return card, filename
