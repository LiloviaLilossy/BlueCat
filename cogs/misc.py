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
        self.creator = utils.get(self.bot.users, id=321566831670198272)

    @commands.command(name="botinfo", usage="")
    async def botinfo(self, ctx):
        embed = Embed(colour=self.bot.defaultcolor)
        ## Please don't remove creator info/support server.
        embed.add_field(name="Creator info:", value="**Username:** LiloviaLilossy#4389\n**ID:**321566831670198272")
        embed.add_field(name="Owner info:", value="**Username:** {insert here}")
        embed.add_field(name="Bot info:", value="**Bot users:** {0}\n**Bot guilds:** {1}\n**Python version:** {2}\n**OS:** {3}\n**Ping:** {4:.2f}ms".format(len(self.bot.users), len(self.bot.guilds), version, platform, self.bot.latency*1000))
        embed.add_field(name="Bot links:", value="**Invite:** [click here](https://discordapp.com/api/oauth2/authorize?client_id={!!!!INSERT BOT USER ID HERE!!!!}&permissions=379968&scope=bot) \n**Bot creator Support server:** [click here](https://discord.gg/Z2nKuYG) \n**Source code:** [click here](https://github.com/LiloviaLilossy/BlueCat)")
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
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
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=embed)
    
    @commands.command(name="invite", usage="")
    async def invite(self, ctx):
        e = Embed(colour=self.bot.defaultcolor)
        e.add_field(name="Invite me to your server!", value="[here](https://discordapp.com/api/oauth2/authorize?client_id={!!!!INSERT BOT USER ID HERE!!!!}&permissions=379968&scope=bot)")
        e.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=e)

    @commands.command(name="giveaway", usage=" <thing> <howlong> [howmany]")
    async def giveaway(self, ctx, thing:str=None, howlong:int=None, howmany:int=1):
        # Note: it won't finish if bot closes, all the giveaways should be ended while bot's online.
        if not thing: raise commands.BadArgument("You can't giveaway nothing.")
        if not howlong: raise commands.BadArgument("You can't start giveaway for 0 minutes.")
        await ctx.send(f"Okay-nyan! {howmany} {thing.title()} giveaway started and will end in {howlong} minutes!", delete_after=10)
        e = Embed(colour=self.bot.defaultcolor)
        e.set_author(name="Giveaway by "+str(ctx.author))
        e.add_field(name=str(howmany)+" "+thing, value="Click on reaction below to win!")
        e.set_footer(text="Giveaway will end in "+str(howlong)+" minutes!")
        emote = utils.get(self.bot.emojis, name='BlueCatWink')
        msg = await ctx.send(embed=e)
        await msg.add_reaction(emote)
        await sleep(howlong*60)
        winners = []
        reacts = (await ctx.channel.fetch_message(msg.id)).reactions
        for reaction in reacts:
            if reaction.emoji == emote:
                users = await reaction.users().flatten()
                for i in range(howmany):
                    winner = choice(users)
                    while winner == self.bot.user:
                        winner = choice(users)
                    winners.append(winner.mention)
                await ctx.send("Giveaway is done! " + ", ".join(winners) + f" will get {thing} from {ctx.author.mention}!")

def setup(bot):
    bot.add_cog(Misc(bot))
