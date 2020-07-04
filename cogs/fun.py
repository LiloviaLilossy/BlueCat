import aiohttp
import base64
import json
from discord import Embed
from discord.ext import commands
from random import choice

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "Fun"
        self.session = aiohttp.ClientSession()
    
    async def cog_unload(self):
        await self.session.close()
        self.session = None
    
    @commands.command(name="bored", aliases=["whattodo", "nothingtodo"], usage="")
    async def bored(self, ctx):
        msg = await ctx.send("So... you're bored and you have nothing to do. Maybe there'll be something for you.")
        async with self.session.get("http://www.boredapi.com/api/activity/") as resp:
            data = await resp.json()
        embed = Embed(colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Guess I found something.", value=data["activity"])
        embed.set_footer(text="Powered by boredapi.com ~nyan!")
        await msg.edit(embed=embed)
    
    @commands.command(name="qr", aliases=["qrcode"], usage=" <text>")
    async def qrcode(self, ctx, *, text=None):
        if not text: raise commands.BadArgument("Maybe, it'll be better, *if you'll send anything to encode?*")
        text = text.split()
        msg = await ctx.send("Let's see, what we can do with this...")
        embed = Embed(title="Something like this, I think.", colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_image(url="https://api.qrserver.com/v1/create-qr-code/?data="+"+".join(text))
        embed.set_footer(text="Powered by api.qrserver.com ~nyan!")
        await msg.edit(embed=embed)
    

    @commands.group(name="encode", invoke_without_command=True, usage="")
    async def encodegroup(self, ctx):
        await ctx.send("The command is still in development!")

    @encodegroup.command(name="b64", usage=" <text>")
    async def b64(self, ctx, *, text:str=None):
        if not text: raise commands.BadArgument("You can't encode no text-nyan!")
        text = text.encode()
        out = base64.b64encode(text)
        await ctx.send(f"Your encoded text: {str(out)}")
    
    @commands.command(name="giveaway", usage=" <thing> <howlong> [howmany]")
    async def giveaway(self, ctx, thing:str=None, howlong:int=None, howmany:int=1):
        if not thing: raise commands.BadArgument("You can't giveaway nothing.")
        if not howlong or howlong <= 0: raise commands.BadArgument("You can't start giveaway for 0 minutes.")
        if howmany <= 0: raise commands.BadArgument("I won't let you set an amount to less than 1.")
        await ctx.send(f"Okay-nyan! {howmany} {thing.title()} giveaway started and will end in {howlong} minutes!", 
                    delete_after=10)
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
                await ctx.send("Giveaway is done! " + ", ".join(winners) + f" will get {thing}"
                            f" from {ctx.author.mention}!")

def setup(bot):
    bot.add_cog(Fun(bot))
