from typing import Any, Tuple

import aiohttp
import nonebot
from nonebot.log import logger

apikey = nonebot.get_driver().config.qweather_apikey
if not apikey:
    raise ValueError(f"请在环境变量中添加 qweather_apikey 参数")
url_weather_api = "https://devapi.qweather.com/v7/weather/"
url_geoapi = "https://geoapi.qweather.com/v2/city/"
logger.debug(apikey)

# 获取城市ID
async def get_Location(city_kw: str, api_type: str = "lookup") -> Tuple[str, Any, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url_geoapi + api_type, params={"location": city_kw, "key": apikey}) as res_session:
            res = await res_session.json()
            if res["code"] == "200":
                location_id = res["location"][0]["id"]
                city_name = res["location"][0]["name"]
                return "200", location_id, city_name
            else:
                return res, None, city_kw


# 获取天气信息
async def get_WeatherInfo(city_name: str, keyword="now"):
    code, city_id, city_name = await get_Location(city_name)
    logger.debug(city_id)
    if code == "200":
        async with aiohttp.ClientSession() as session:
            async with session.get(url_weather_api + keyword,
                                   params={"location": city_id, "key": apikey}) as res_session:
                res = await res_session.json()
                return res, city_name
    else:
        return code, city_name


async def now_weather(city_name: str, keyword: str = "now") -> str:
    data, city_name = await get_WeatherInfo(city_name, keyword)
    if data["code"] == "200":
        now = data["now"]
        message = ["------实时天气数据------\n\n",
                   "城市：%s\n温度（℃）：%s\n体感温度（℃）：%s\n天气情况：%s\n风向：%s\n风力：%s\n风速（km/h）：%s\n相对湿度：%s\n云量：%s\n能见度：%s\n"
                   "大气压强（百帕）：%s\n" % (
                       city_name, now["temp"], now["feelsLike"], now["text"], now["windDir"], now["windScale"],
                       now["windSpeed"], now["humidity"], now["cloud"], now["vis"], now["pressure"]), "数据来源：和风天气\n",
                   "数据更新时间：%s\n" % data["updateTime"], "链接：%s" % data["fxLink"]]
        content = "".join(message)
        return content
    else:
        return "错误代码：%s" % data["code"]
