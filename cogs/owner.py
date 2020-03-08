import json
from addons.get_something import get_smth
from discord import Game, utils
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "Owner"

    async def cog_check(self, ctx):
        if ctx.author.id in get_smth("owner"):
            return True
        else:
            return commands.NotOwner("You aren't a bot owner-nyan!")

    @commands.command(name="reload", aliases=["r"])
    async def _reload(self, ctx, cog="*"):
        lilo = utils.get(self.bot.users, id=516280857468731395)
        if cog == "*":
            loadedcogs = []
            for cog in self.bot.coglist():
                try:
                    self.bot.reload_extension(cog)
                    loadedcogs.append(cog)
                except commands.ExtensionNotLoaded:
                    self.bot.load_extension(cog)
                    loadedcogs.append(cog)
                except commands.ExtensionError as e:
                    await lilo.send(f"{cog} - {e}")
                    await ctx.send(",".join(loadedcogs) + " - done-nyan!")
        else:
            try:
                self.bot.reload_extension(cog)
                await ctx.send(f"Cog {cog} - done-nyan!")
            except commands.ExtensionNotLoaded:
                self.bot.load_extension(cog)
                await ctx.send(f"Cog {cog} - done-nyan!")
            except commands.ExtensionNotFound:
                await ctx.send(f"Cog {cog} not found!")

    @commands.command(name="presence", aliases=["change-presence", "cp"])
    async def presence(self, ctx, text=None):
        if text==None:
            return await ctx.send("Seriously? Are you thinking I'll 'play' *nothing*?")
        game = Game(name=text+" | bc~help for help")
        await self.bot.change_presence(activity=game)
        await ctx.send(f"Done. The presence is {text} for now-nyan!")

def setup(bot):
    bot.add_cog(Owner(bot))
