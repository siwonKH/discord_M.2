import time
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from modules.async_request import get_request
from modules.async_bs4 import do_beautiful_soup


class Lyrics(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Initialized cog Lyrics")

    def cog_unload(self):
        print("closing")

    async def cog_command_error(self, ctx: SlashContext, error: commands.CommandError):
        print('{}'.format(str(error)))

    @cog_ext.cog_slash(name="lyrics", description="Finds Music Lyrics")
    async def _lyrics(self, ctx: SlashContext, *, search: str = ""):
        parse_len = 1000

        log = []
        p = 7
        start = time.time()

        log.append(f"----------{search}-----------")
        log.append("GET Request Sent.")

        url = "https://www.google.com/search?q=" + search + " lyrics"
        res = await get_request(url, loop=self.bot.loop)
        log.append(f"GET Response ({round(time.time() - start, p)}s)")

        soup = await do_beautiful_soup(res.text, loop=self.bot.loop)
        log.append(f"Parsed HTML. ({round(time.time() - start, p)}s)")

        try:
            log.append("Checking if lyrics exist..")
            title = soup.select_one('.kno-ecr-pt > span').text
            log.append(f"Parsed title of music. ({round(time.time() - start, p)}s)")
            try:
                singer = soup.select_one('.wwUB2c').text
            except:
                singer = ""
            log.append(f"Parsed singer. ({round(time.time() - start, p)}s)")
            lyrics_element = soup.select('.bbVIQb')[1]
            log.append(f"Parsed lyrics element. ({round(time.time() - start, p)}s)")

            lyrics = ""
            for paragraph in lyrics_element.select('div'):
                for sentence in paragraph.select('span'):
                    lyrics += sentence.text + "\n"
                lyrics += "\n"
            log.append(f"Parsed lyrics. ({round(time.time() - start, p)}s)")
            lyrics_len = len(lyrics)
        except:
            await ctx.send(content=f'Can not find lyrics of ***{search}***')
            log.append("Lyrics doesn't exists..")
            for line in log:
                print(line)
            return

        parse_pos = [0]

        pos = parse_len
        while lyrics_len > pos:
            while lyrics[pos] != "\n":
                pos -= 1
            parse_pos.append(pos)
            pos += parse_len
        parse_pos.append(lyrics_len)
        log.append(f"Lyrics parse positions all set. ({round(time.time() - start, p)}s)")

        for x in range(0, len(parse_pos) // 6 + 1):
            embed = discord.Embed(
                        title=f'{title}',
                        description=f'{singer}',
                        color=discord.Color.blurple()
                    )
            try:
                for i in range(0, 6):
                    embed.add_field(name=f'** **', value=f'{lyrics[parse_pos[i]:parse_pos[i + 1]]}', inline=False)
            except:
                pass
            log.append(f"Sending embed.. ({round(time.time() - start, p)}s)")
            await ctx.send(embed=embed)
            log.append(f"Embed sent. ({round(time.time() - start, p)}s)")

        for line in log:
            print(line)
        # for p in parse_pos:
        #     print(p, end=", ")
        # print("")


def setup(bot):
    bot.add_cog(Lyrics(bot))
