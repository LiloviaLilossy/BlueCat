import datetime
import json
from addons.get_something import get_smth
from asyncio import sleep
from discord import Embed, utils, Color
from discord.ext import commands
from humanize import naturaltime
from random import choice
from sys import version, platform

class Misc(commands.Cog):
    def __init__(self, bot):
        bot.defaultcolor = Color.from_rgb(65,105,225)
        self.bot = bot
        self.name = "Misc"
        self.owner = utils.get(self.bot.users, id=516280857468731395)

    @commands.command(name="botinfo", usage="")
    async def botinfo(self, ctx):
        embed = Embed(colour=self.bot.defaultcolor)
        embed.add_field(name="Owner info:", value="**Username:** LiloviaLilossy#1830\n**ID:**516280857468731395")
        embed.add_field(name="Bot info:", value="**Bot users:** {0}\n**Bot guilds:** {1}\n**Python version:** {2}\n**OS:** {3}\n**Ping:** {4:.2f}ms".format(len(self.bot.users), len(self.bot.guilds), version, platform, self.bot.latency*1000))
        embed.add_field(name="Bot links:", value="**Invite:** [click here](https://discordapp.com/api/oauth2/authorize?client_id=676417304707203132&permissions=379968&scope=bot) \n**Support server:** [click here](https://discord.gg/Z2nKuYG) \n**Source code:** [click here](https://github.com/LiloviaLilossy/BlueCat)")
        embed.set_footer(text="Nyan! Blue Cat-bot v"+self.bot.version)
        await ctx.send(embed=embed)

    @commands.command(name="changelog", usage="")
    async def changelog(self, ctx):
        changelog = get_smth("changelog")
        text = f"""
```
{changelog}
```
        """
        embed = Embed(colour=self.bot.defaultcolor)
        embed.add_field(name="Blue Cat Changelog!", value=text)
        embed.set_image(url="https://media.discordapp.net/attachments/616645258280828949/691873654639820900/changelog.png")
        embed.set_footer(text="Nyan! Blue Cat-bot v"+self.bot.version)
        await ctx.send(embed=embed)

    @commands.command(name="prefixes", aliases=["prefix"], usage="")
    async def prefixes(self, ctx):
        embed = Embed(colour=self.bot.defaultcolor)
        with open(f"guild-settings/{ctx.guild.id}/prefixes.json", "r") as file:
            data = json.load(file)
        prefixes = ""
        for prefix in data["prefixes"]:
            prefixes+="***"
            prefixes+=prefix
            prefixes+="***, "
        embed.add_field(name="Bot prefixes for "+ctx.guild.name, value=prefixes)
        embed.set_footer(text="Nyan! Blue Cat-bot v"+self.bot.version)
        await ctx.send(embed=embed)
    
    @commands.command(name="invite", usage="")
    async def invite(self, ctx):
        e = Embed(colour=self.bot.defaultcolor)
        e.add_field(name="Invite me to your server!", value="[here](https://discordapp.com/api/oauth2/authorize?client_id=676417304707203132&permissions=379968&scope=bot)")
        embed.set_footer(text="Nyan! Blue Cat-bot v"+self.bot.version)
        await ctx.send(embed=e)
    
    @commands.command(name="support", usage="")
    async def support(self, ctx):
        e = Embed(colour=self.bot.defaultcolor)
        e.add_field(name="So, you need help with me. Here's an invite, try ask them.", value="[here](https://discord.gg/Z2nKuYG)")
        embed.set_footer(text="Nyan! Blue Cat-bot v"+self.bot.version)
        await ctx.send(embed=e)
    
    @commands.command(name="suggest", aliases=["suggestion"], usage=" <suggestion>")
    async def suggestion(self, ctx, *, suggestion=None):
        if suggestion == None:
            raise commands.BadArgument("You can't suggest nothing.")
        ue = Embed(colour=self.bot.defaultcolor)
        ue.set_author(name=ctx.author)
        ue.add_field(name="Your suggestion now is in the support server, where you can check when it'll be approved(or denied).", value="**Your suggestion:** \n"+suggestion)
        ue.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=ue)
        
        oe = Embed(colour=self.bot.defaultcolor)
        oe.set_author(name=ctx.author)
        oe.add_field(name="New suggestion!", value="**From:** "+str(ctx.guild)+"\n**Suggestion**:\n"+suggestion)
        oe.timestamp = datetime.datetime.now()
        channel = self.bot.get_channel(id=690843403507728406)
        await channel.send(embed=oe)

def setup(bot):
    bot.add_cog(Misc(bot))
