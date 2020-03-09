from addons.get_something import *
from discord.ext import commands

bot = commands.Bot(command_prefix=get_prefix)
bot.coglist = get_cogs
token = get_token("discord")

bot.remove_command("help")
bot.load_extension("jishaku")
for cog in bot.coglist():
    bot.load_extension(cog)

bot.run(token)
