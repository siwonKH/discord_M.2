import asyncio
import functools
from bs4 import BeautifulSoup


async def do_beautiful_soup(text, loop: asyncio.BaseEventLoop = None):
    loop = loop or asyncio.get_event_loop()
    partial = functools.partial(BeautifulSoup, text, 'html.parser')
    soup = await loop.run_in_executor(None, partial)
    return soup
