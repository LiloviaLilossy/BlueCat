import json
from addons.get_something import get_smth
from discord import Embed, utils
from discord.ext import commands
from sys import version, platform

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner = utils.get(self.bot.users, id=516280857468731395)

    @commands.command(name="botinfo")
    async def botinfo(self, ctx):
        embed = Embed()
        embed.add_field(name="Owner info:", value="**Username:**"+str(self.owner)+"\n**ID:**"+str(self.owner.id))
        embed.add_field(name="Bot info:", value="**Bot users:** "+str(len(self.bot.users))+"\n**Bot guilds:** "+str(len(self.bot.guilds))+"\n**Python version:** "+str(version)+"\n**OS:** "+platform)
        embed.add_field(name="Bot links:", value="**Invite:** soon \n**Support server:** [click here](https://discord.gg/Z2nKuYG) \n**Source code:** soon")
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=embed)

    @commands.command(name="changelog")
    async def changelog(self, ctx):
        changelog = get_smth("changelog")
        text = f"""
```
{changelog}
```
        """
        embed = Embed()
        embed.set_author(name="Owner is "+self.owner)
        embed.add_field(title="Blue Cat Changelog!", value=text)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=embed)

    @commands.command(name="prefixes")
    async def prefixes(self, ctx):
        embed = Embed()
        with open(f"guild-settings/{ctx.guild.id}/prefixes.json", "r") as file:
            data = json.load(file)
        prefixes = ""
        for prefix in data["prefixes"]:
            prefixes+="***"
            prefixes+=prefix
            prefixes+="***, "
        embed.add_field(name="Bot prefixes for "+ctx.guild.name, value=prefixes)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
