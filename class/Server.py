import discord
import asyncio
import datetime
from discord.ext import commands
from discord_slash import SlashContext

import config
from Cache import Cache
from modules.async_request import get_request
from modules.make_embed import make_embed
from modules.get_meal import get_meal_type


class Server:
    def __init__(self, bot: commands.Bot, ctx: SlashContext):
        self.bot = bot

        self._ctx = ctx
        self.channel = None
        self.toggle = False
        self.lastAutoMsg = None
        self.lastAutoMsgDate = None

        self.cache = Cache()
        self.lastCache = Cache()
        self.auto_set = bot.loop.create_task(self.bob_task())

    async def wait_until(self, hour, minute):
        t = datetime.datetime.now().hour
        m = datetime.datetime.now().minute
        while t != hour or t == hour and m != minute:
            if not self.toggle:
                return False
            await asyncio.sleep(1)
            t = datetime.datetime.now().hour
            m = datetime.datetime.now().minute
        return True

    async def bob_task(self):
        while True:
            await asyncio.sleep(1)
            if self.toggle:
                # Gets from config.py
                set_hour = config.set_hour
                set_min = config.set_min
                ready_hour = config.ready_hour
                ready_min = config.ready_min

                guild_id = self._ctx.guild.id

                # Wait Until Ready Time
                print(f"TASK({guild_id}): waiting til {ready_hour}:{ready_min}")
                wait_result = await self.wait_until(ready_hour, ready_min)

                # if toggled before set time
                if not wait_result:
                    print(f"TASK({guild_id}): <!> Process Disabled")
                    continue

                print(f"TASK({guild_id}): Registered process starting")

                # Makes edit Embed if last msg exists
                if self.lastAutoMsg:
                    print(f"TASK({guild_id}): I've sent embed yesterday! Let me edit it..")
                    edit_embed = await make_embed(self.lastAutoMsgDate, self.cache.nextBreakfast, self.cache.nextLunch, self.cache.nextDinner)
                    await self.lastAutoMsg.edit(embed=edit_embed)

                # Requests menu
                breakfast = await self.bob("nextBreakfast")
                lunch = await self.bob("nextLunch")
                dinner = await self.bob("nextDinner")

                if not self.toggle:
                    print(f"TASK({guild_id}): <!> Process Disabled")
                    continue

                # check menu
                if len(breakfast + lunch + dinner) > 10:
                    self.lastAutoMsg = None
                    print(f"TASK({guild_id}): There is nothing to send.")
                    continue

                # Makes embed
                embed = await make_embed("오늘 급식", breakfast, lunch, dinner)

                # Waiting Until Set Time
                print(f"TASK({guild_id}): embed ready. waiting til {set_hour}:{set_min}")
                wait_result = await self.wait_until(set_hour, set_min)

                # if toggled before set time
                if not wait_result:
                    print(f"TASK({guild_id}): <!> Process Disabled")
                    continue

                # Embed sending Process
                print(f"TASK({guild_id}): Sending embed")
                embed_msg = await self.channel.send(embed=embed)
                print(f"TASK({guild_id}): embed sent")

                # saves infos to edit tomorrow
                today = datetime.datetime.now()
                self.lastAutoMsg = embed_msg
                self.lastAutoMsgDate = f'{today.month}월 {today.day}일 급식'

                # wait 1m to prevent process loop
                print(f"TASK({guild_id}): waiting 1 minute")
                print("-" * 30)
                await asyncio.sleep(60)

    async def bob(self, b_type):
        sc_type = "high"
        code = "R100000822"

        today = datetime.datetime.now()
        date = today.date()
        day = today.day

        guild_id = self._ctx.guild.id

# next day option
        skip_days = 0
        if b_type.startswith("next"):
            skip_days = 1
        day += skip_days
# Lookup Cache and Returns Available Cache
        try:
            if self.lastCache.get_cache(b_type) == date:
                print(f"TASK({guild_id}): <cached {b_type}>")
                return self.cache.get_cache(b_type)
        except:
            print(f"TASK({guild_id}): Error on Caching")

        print(str(today) + "-" * 4)
# Requesting to API
        b_type2 = b_type
        if b_type.startswith("next"):
            b_type2 = b_type[4:].lower()

        url = f"https://schoolmenukr.ml/api/{sc_type}/{code}?date={day}"
        print(f"TASK({guild_id}): Requesting {b_type} menu from API..")
        res = await get_request(url, loop=self.bot.loop)

        try:
            meals = res.json()["menu"][0][b_type2]
        except:
            try:
                print(f"TASK({guild_id}): Trying Again.1) maybe today is end of a month.")
                url = f"https://schoolmenukr.ml/api/{sc_type}/{code}?month={today.month + 1}&date={1}"
                res = await get_request(url, loop=self.bot.loop)
                meals = res.json()["menu"][0][b_type2]
                print(f"TASK({guild_id}): Trying Again.1) Yes! It was a end of a month!")
            except:
                try:
                    print(f"TASK({guild_id}): Trying Again.2) maybe today is end of a year.")
                    url = f"https://schoolmenukr.ml/api/{sc_type}/{code}?year={today.year + 1}&month=1&date=1"
                    res = await get_request(url, loop=self.bot.loop)
                    meals = res.json()["menu"][0][b_type2]
                    print(f"TASK({guild_id}): Trying Again.2) Yes! It was a end of a Year! Happy new year~!")
                except:
                    print(f"TASK({guild_id}): WTF? I'm not trying any more. This is a lie!")
                    return "ERROR. This cannot be! 싹다 갈아 엎어!!"

# Response Parsing Process
        msg = ""
        for meal in meals:
            meal = str(meal)
            while meal[len(meal) - 1] == "." or meal[len(meal) - 1].isdigit():
                meal = meal[:-1]
            msg += meal + "\n"

        if msg == "":
            msg = "-" if skip_days != 0 else "급식이 없습니다."

# Caching Process
        if skip_days > 1:
            pass
        else:
            self.lastCache.set_cache(b_type, date)
            self.cache.set_cache(b_type, msg)
        print(f"Done. Saved cache {b_type}")
        print("-" * 30)
        return msg