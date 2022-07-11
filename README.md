# Warfarin
基于nonebot2的聊天机器人  
目前仍在开发中，代码可能会有大幅度变动，请知悉  
采用mirai-api-http 2.x 作为适配器  
（在nonebot2中采用mah的我是不是搞错了什么）  
因为商店中很多功能都是采用onebot，直接搬到mah中会无法使用...  
所以我只能对它们进行修改以适配mah。  


## FUNCTION
* 从文件夹中随机选择图片发送
* 从bangumi.moe获取番剧时间表。主要代码实现来自[anime_news](https://github.com/5656565566/anime_news); 在其基础稍作修改，感谢原作者
* 每日浅草寺求签
* 塔罗牌抽取
* 天气预报(信息来源：和风天气)
* B站链接、小程序解析并生成（伪）分享卡片。
修改自[nonebot_plugin_bilibili_viode](https://github.com/ASTWY/nonebot_plugin_bilibili_viode)
和[nonebot_plugin_analysis_bilibili](https://github.com/mengshouer/nonebot_plugin_analysis_bilibili)。
感谢两位的代码。  
* 适配mah的涩图插件，来自于[youth-version-of-setu4](https://github.com/Special-Week/youth-version-of-setu4)。
我喜欢这个插件的实现方式。十分感谢作者详尽的注释，让适配得以轻松进行。
但在适配mah的同时根据自身使用情况做了一些小小的改动。

## TO DO
* 通过图片标签发送图片（目前通过别人的插件实现了一部分）

## How to start

1. generate project using `nb create` .
2. writing your plugins under `warfarin/plugins` folder.
3. run your bot using `nb run` .
