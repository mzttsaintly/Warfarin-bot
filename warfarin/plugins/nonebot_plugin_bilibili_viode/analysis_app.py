import re
import aiohttp
import urllib.parse
import json
from nonebot.exception import FinishedException


async def bili_keyword(text):
    msg = ""
    pattern = re.compile(r'"desc":".*?"')
    desc = re.findall(pattern, text)
    i = 0
    while i < len(desc):
        title_dict = "{" + desc[i] + "}"
        title = json.loads(title_dict)
        i += 1
        if title["desc"] == "哔哩哔哩":
            continue
        vurl = await search_bili_by_title(title["desc"])
        if vurl:
            av_id = re.search(r"av[*=\s]?(\d*)?", str(vurl))
            msg = av_id[1]
            print("msg = ", msg)
            break
    return msg


async def search_bili_by_title(title: str):
    search_url = f"https://api.bilibili.com/x/web-interface/search/all/v2?keyword={urllib.parse.quote(title)}"

    async with aiohttp.request(
        "GET", search_url, timeout=aiohttp.client.ClientTimeout(10)
    ) as resp:
        result = (await resp.json())["data"]["result"]

    for i in result:
        if i.get("result_type") != "video":
            continue
        # 只返回第一个结果
        return i["data"][0].get("arcurl")


async def b23_extract(text):
    b23 = re.compile(r"b23.tv/(\w+)|(bili(22|23|33|2233).cn)/(\w+)", re.I).search(
        text.replace("\\", "")
    )
    url = f"https://{b23[0]}"
    async with aiohttp.request(
        "GET", url, timeout=aiohttp.client.ClientTimeout(10)
    ) as resp:
        return str(resp.url)
