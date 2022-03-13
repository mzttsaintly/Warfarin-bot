# Warfarin
基于nonebot2的聊天机器人
目前仍在开发中，代码可能会有大幅度变动，请知悉
采用mirai-api-http 2.x 作为适配器

## FUNCTION
* 从文件夹中随机选择图片发送
* 从bangumi.moe获取番剧时间表。主要代码实现来自[anime_news](https://github.com/5656565566/anime_news); 在其基础稍作修改，感谢原作者
* 每日浅草寺求签
* 塔罗牌抽取
* 天气预报(信息来源：和风天气)

## TO DO
* 通过图片标签发送图片

## How to start

1. generate project using `nb create` .
2. writing your plugins under `warfarin/plugins` folder.
3. run your bot using `nb run` .
