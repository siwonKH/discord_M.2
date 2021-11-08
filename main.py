from discord.ext import commands
from discord_slash import SlashCommand

bot = commands.Bot(command_prefix="!@#$@#!")
slash = SlashCommand(bot, override_type=True, sync_commands=True)


@bot.event
async def on_ready():
    print('The Bot is Online')
    bot.load_extension('cogs.Lyrics')
    print('Bot Ready')
    print('-'*10)


# bot.run('')  # M.2
bot.run('')  # Beta M.2
