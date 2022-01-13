import os
import aiohttp
import asyncio
import json


BANGUMI_LIST = "https://cdn.jsdelivr.net/npm/bangumi-data@0.3/dist/data.json"


async def get_json_bangumi():
    head = {
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome "
                          "/ 80.0.3987.122  Safari / 537.36"}
    async with aiohttp.ClientSession() as session:
        async with session.get(BANGUMI_LIST, headers=head) as res:
            dates = await res.json()
            # date = json.dumps(dates, ensure_ascii=False)
            # with open(os.path.join(f"{os.getcwd()}, bangumidata.json"), "w") as f:
            with open(os.path.join(os.getcwd(), "warfarin", "plugins", "BangumiSchedule",
                                   "resource", "bangumidata.json"), "w", encoding='utf-8') as f:
                # f.write(date)
                json.dump(dates, f, ensure_ascii=False)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_json_bangumi())
