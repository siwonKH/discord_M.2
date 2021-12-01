import config
from discord.ext import commands
from discord_slash import SlashCommand

bot = commands.Bot(command_prefix="/")
slash = SlashCommand(bot, override_type=True, sync_commands=True)


@bot.event
async def on_ready():
    print('The Bot is Online')
    bot.load_extension('cogs.Lyrics')
    print('Bot Ready')
    print('-'*10)


bot.run('ODA3OTE3NzA3Mjc3NzYyNjIw.YB-9_w.3glf49IXESw3aN-k9CXZChA38y0')
