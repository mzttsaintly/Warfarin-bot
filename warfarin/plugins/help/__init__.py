from nonebot import on_command

helper_dict = {"今日新闻": "获取今日的60s新闻（每日8点05分也会自动在群广播）",
               "/help": "获取可用指令列表",
               "今日新番": "获取当日新番列表(晚上也会定时在群广播）",
               "/get anime": "手动更新番剧时间表（仅管理员可用）",
               "/new season": "手动更新季度新番表（仅管理员可用）",
               "/get season": "获得本季度新番列表(以长图片形式，用时较长）",
               "(地名)天气": "获取地点天气预报",
               "塔罗牌": "随机抽取塔罗牌",
               "setu|涩图|色图 + (几张) + (r18) + (关键词)": "括号中指令选填，没有的可以跳过，但有的话顺序不能错；\n"
                                                    "群聊中图片填多少都默认为一张，且r18指令不生效；\n"
                                                    "关键词可以有多个，"
                                                    "以空格分割时关键词之间匹配规则为and，会同时搜索符合两个关键词的图片（最多3个）\n"
                                                    "以|分割时关键词之间匹配规则为or，会搜索符合其中一个关键词的图片（最多20个）",
               "hso": "能从我本地图库获得一张图片吧大概",
               "/followup {uid}": "关注up(后接uid（仅管理员可用）)",
               "/unfollow-up {uid}": "取注up(后接uid（仅管理员可用）)",
               "/check_list": "查询关注的up主列表"}
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
