from nonebot import on_command


helper_dict = {"今日新闻": "获取今日的60s新闻（每日8点05分也会自动在群广播）",
               "/help": "获取可用指令列表",
               "今日新番": "获取当日新番列表(晚上也会定时在群广播）",
               "/get anime": "手动更新番剧时间表（仅管理员可用）",
               "/new season": "手动更新季度新番表（仅管理员可用）",
               "/get season": "获得本季度新番列表(以长图片形式，用时较长）",
               "(地名)天气": "获取地点天气预报",
               "塔罗牌": "随机抽取塔罗牌",
               "hso": "能获得一张图片吧大概"}
bot_helper = on_command('help', aliases={"帮助"}, priority=5, block=True)


@bot_helper.handle()
async def helper():
    """
    发送可用指令列表

    Returns:

    """
    msg = "指令列表：\n"
    for num, (key, value) in enumerate(helper_dict.items(), start=1):
        msg = msg + f"[{num}]{str(key)}: {value}\n"
    await bot_helper.finish(msg)
