import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Menu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.servers = {}
        print("Initialized cog Lyrics")

    def cog_unload(self):
        print("closing")

    async def cog_command_error(self, ctx: SlashContext, error: commands.CommandError):
        print('{}'.format(str(error)))
