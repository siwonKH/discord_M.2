import discord


async def make_embed(title, breakfast, lunch, dinner):
    embed = (
        discord.Embed(title=title, color=discord.Color.blurple())
    )
    if not breakfast == "-":
        embed.add_field(name='-아침-', value=breakfast)
    if not lunch == "-":
        embed.add_field(name='-점심-', value=lunch)
    if not dinner == "-":
        embed.add_field(name='-저녁-', value=dinner)

    return embed
