import json
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

    @commands.command(name="presence", aliases=["change-presence", "cp"], usage=" <text>")
    async def presence(self, ctx, *, text=None):
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
