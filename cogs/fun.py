import aiohttp
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
	
    @commands.command(name="bored", aliases=["whattodo", "nothingtodo"])
    async def bored(self, ctx):
        msg = await ctx.send("So... you're bored and you have nothing to do. Maybe there'll be something for you.")
        async with self.session.get("http://www.boredapi.com/api/activity/") as resp:
            data = await resp.json()
        embed = Embed(colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Guess I found something.", value=data["activity"])
        embed.set_footer(text="Powered by boredapi.com")
        await msg.edit(embed=embed)
	
    @commands.command(name="qr", aliases=["qrcode"])
    async def qrcode(self, ctx, text=None):
        if not text:
            return await ctx.send("Maybe, it'll be better, *if you'll send anything to encode?*")
        msg = await ctx.send("Let's see, what we can do with this...")
        embed = Embed(title="Something like this, I think.", colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_image(url=f"https://api.qrserver.com/v1/create-qr-code/?data={text}")
        embed.set_footer(text="Powered by api.qrserver.com")
        await msg.edit(embed=embed)
	
    @commands.command(name="bluecat-random", aliases=["randombluecat", "image-bluecat"])
    async def randomyuniimage(self, ctx):
        with open("bot-settings/images.json", "r") as file:
            data = json.load(file)
        image = choice(data["urls"])
        embed = Embed(colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_image(url=image)
        embed.set_footer(text="Just an image of me-nyan! "+str(data["urls"].index(image))+"/"+str(len(data["urls"])))
        await ctx.send(embed=embed)
		

def setup(bot):
    bot.add_cog(Fun(bot))
