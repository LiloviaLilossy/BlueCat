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

    @commands.command(name="botinfo")
    async def botinfo(self, ctx):
        embed = Embed(colour=self.bot.defaultcolor)
        embed.add_field(name="Owner info:", value="**Username:** LiloviaLilossy#1830\n**ID:**516280857468731395")
        embed.add_field(name="Bot info:", value="**Bot users:** "+str(len(self.bot.users))+"\n**Bot guilds:** "+str(len(self.bot.guilds))+"\n**Python version:** "+str(version)+"\n**OS:** "+platform)
        embed.add_field(name="Bot links:", value="**Invite:** [click here](https://discordapp.com/api/oauth2/authorize?client_id=676417304707203132&permissions=379968&scope=bot) \n**Support server:** [click here](https://discord.gg/Z2nKuYG) \n**Source code:** [click here](https://github.com/LiloviaLilossy/BlueCat)")
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
        embed = Embed(colour=self.bot.defaultcolor)
        embed.add_field(text="Blue Cat Changelog!", value=text)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=embed)

    @commands.command(name="prefixes", aliases=["prefix"])
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
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=embed)

    @commands.command(name="help")
    async def help(self, ctx):
        embed = Embed(colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        for cog in sorted(self.bot.cogs, reverse=True):
            help_value = ""
            c = self.bot.get_cog(cog)
            if cog == "Jishaku":
                c.name = "Jishaku"
            cmds = c.get_commands()
            if cmds != []:
                for cmd in cmds:
                    if cmd.hidden == True:
                        pass
                    elif cmd.aliases:
                        help_value += f"`{cmd} | "+" | ".join(cmd.aliases) + "`☆"
                    else:
                        help_value += f"`{cmd}`☆"
                if help_value != "":
                    embed.add_field(name=c.name, value=help_value)
        await ctx.send(embed=embed)
    
    @commands.command(name="invite")
    async def invite(self, ctx):
        e = Embed(colour=self.bot.defaultcolor)
        e.add_field(name="Invite me to your server!", value="[here](https://discordapp.com/api/oauth2/authorize?client_id=676417304707203132&permissions=379968&scope=bot)")
        e.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=e)
    
    @commands.command(name="support")
    async def support(self, ctx):
        e = Embed(colour=self.bot.defaultcolor)
        e.add_field(name="So, you need help with me. Here's an invite, try ask them.", value="[here](https://discord.gg/Z2nKuYG)")
        e.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=e)
    
    @commands.command(name="suggest", aliases=["suggestion"])
    async def suggestion(self, ctx, *, suggestion=None):
        if suggestion == None:
            raise commands.BadArgument("You can't suggest nothing.")
        ue = Embed(colour=self.bot.defaultcolor)
        ue.set_author(name=ctx.author)
        ue.add_field(name="Your suggestion now is in the support server, where you can check when it'll be approved(or denied).", value="**Your suggestion:** \n"+suggestion)
        ue.timestamp = datetime.datetime.now()
        await ctx.send(embed=ue)
        
        oe = Embed(colour=self.bot.defaultcolor)
        oe.set_author(name=ctx.author)
        oe.add_field(name="New suggestion!", value="**From:** "+str(ctx.guild)+"\n**Suggestion**:\n"+suggestion)
        oe.timestamp = datetime.datetime.now()
        channel = self.bot.get_channel(id=690843403507728406)
        await channel.send(embed=oe)

    @commands.command(name="giveaway")
    async def giveaway(self, ctx, thing: str, howlong:int=60, howmany:int=1):
    	await ctx.send(f"Okay-nyan! {howmany} {thing.title()} giveaway started and will end in {howlong} minutes!", delete_after=10)
    	e = Embed(colour=self.bot.defaultcolor)
    	e.set_author(name="Giveaway by "+ctx.author)
    	e.add_field(name=str(howmany)+" "+thing, value="Click on reaction below to win!")
    	e.set_footer(text="Giveaway will end in "+str(howlong)+" minutes!")
    	emote = utils.get(bot.emojis, name='BlueCatWink')
    	msg = await ctx.send(embed=e)
    	await msg.add_reaction(emote)
    	await sleep(howlong*60)
    	winners = []
    	for reaction in msg.reactions:
            if reaction.emoji == emote:
                users = await msg.reactions.users().flatten()
                for i in range(howmany):
                    winner = choice(users)
                    while winner == self.bot.user:
                        winner = random.choice(users)
                    winners.append(winner)
                await ctx.send("Giveaway is done! "+", ".join(winners)+f" will get {thing} from {ctx.author.mention}!")

def setup(bot):
    bot.add_cog(Misc(bot))
