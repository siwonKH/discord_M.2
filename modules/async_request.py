import asyncio
import functools
import requests
user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}


async def get_request(url, loop: asyncio.BaseEventLoop = None):
    loop = loop or asyncio.get_event_loop()
    partial = functools.partial(requests.get, url, headers=user_agent)
    res = await loop.run_in_executor(None, partial)
    return res
