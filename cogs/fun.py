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
        embed.set_footer(text="Powered by boredapi.com")
        await msg.edit(embed=embed)
	
    @commands.command(name="qr", aliases=["qrcode"], usage=" <text>")
    async def qrcode(self, ctx, *, text=None):
        if not text: raise commands.BadArgument("Maybe, it'll be better, *if you'll send anything to encode?*")
        text = text.split()
        msg = await ctx.send("Let's see, what we can do with this...")
        embed = Embed(title="Something like this, I think.", colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_image(url="https://api.qrserver.com/v1/create-qr-code/?data="+"+".join(text))
        embed.set_footer(text="Powered by api.qrserver.com -nyan!")
        await msg.edit(embed=embed)

    @commands.command(name="cat", aliases=["catimg"], usage="")
    async def randomcatimage(self, ctx):
        e = Embed(colour=self.bot.defaultcolor)
        url = "http://aws.random.cat/meow"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
        e.set_image(url=data["file"])
        e.set_footer(text="Powered by aws.random.cat -nyan!")
        await ctx.send(embed=e)

    @commands.command(name="emoji", usage=" <letters>")
    async def emojisend(self, ctx, *, letters:str=None):
        if not letters: raise commands.BadArgument("I can't send emoji letters from nothing, y'know?")
        allowed = list("qwertyuiopasdfghjklzxcvbnm")
        letters = list(letters)
        emojis = ""
        for i in letters:
            if not i.lower() in allowed: continue
            if i == " ": emojis+= "  "
            else: emojis+= ":regional_indicator_"+i.lower()+":"
        await ctx.send(emojis)

def setup(bot):
    bot.add_cog(Fun(bot))
