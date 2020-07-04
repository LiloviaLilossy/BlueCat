import json
from addons.get_something import get_smth
from discord import Game, utils, User
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "Owner"

    async def cog_check(self, ctx):
        if ctx.author.id in self.bot.owner_ids:
            return True
        else:
            raise commands.NotOwner("You aren't a bot owner-nyan!")

    @commands.command(name="reload", aliases=["r"], usage=" [cog]")
    async def _reload(self, ctx, cog="*"):
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
                    await ctx.author.send(f"{cog} - {e}")
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

    @commands.command(name="presence", aliases=["change-presence", "cp"], usage=" <text>")
    async def presence(self, ctx, text=None):
        if text==None:
            raise commands.BadArgument("Seriously? Are you thinking I'll 'play' *nothing*?")
        game = Game(name=text+" | bc~help for help")
        await self.bot.change_presence(activity=game)
        await ctx.send(f"Done. The presence is {text} for now-nyan!")

    @commands.command(name="botban", usage=" <member>")
    async def botban(self, ctx, *, member: User):
        with open("bot-settings/banned.json", "r") as f:
            banned = json.load(f)
        banned["ban"].append(member.id)
        with open("bot-settings/banned.json", "w") as f:
            json.dump(banned, f)
        await ctx.send(f"{member} now **can't** use my commands. Nothing will change, but anyway.")

    @commands.command(name="botunban", usage=" <member>")
    async def botunban(self, ctx, *, member: User):
        with open("bot-settings/banned.json", "r") as f:
            banned = json.load(f)
        banned["ban"].remove(member.id)
        with open("bot-settings/banned.json", "w") as f:
            json.dump(banned, f)
        await ctx.send(f"{member} now **can** use my commands. Nothing will change, but anyway.")

def setup(bot):
    bot.add_cog(Owner(bot))
