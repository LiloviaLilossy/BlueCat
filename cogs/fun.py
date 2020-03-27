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
    async def qrcode(self, ctx, *, text=None):
        if not text:
            raise commands.BadArgument("Maybe, it'll be better, *if you'll send anything to encode?*")
        text = text.split()
        msg = await ctx.send("Let's see, what we can do with this...")
        embed = Embed(title="Something like this, I think.", colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_image(url="https://api.qrserver.com/v1/create-qr-code/?data="+"+".join(text))
        embed.set_footer(text="Powered by api.qrserver.com -nyan!")
        await msg.edit(embed=embed)
	
    @commands.command(name="img", aliases=["randomimg", "bluecatimg"])
    async def randomyuniimage(self, ctx):
        with open("bot-settings/images.json", "r") as file:
            data = json.load(file)
        image = choice(data["urls"])
        embed = Embed(colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_image(url=image)
        embed.set_footer(text="Just an image of me-nyan! {0}/{1}".format(data["urls"].index(image), len(data["urls"])))
        await ctx.send(embed=embed)

    @commands.command(name="cat", aliases=["catimg"])
    async def randomcatimage(self, ctx, *, text=None):
        e = Embed(colour=self.bot.defaultcolor)
        url = "http://aws.random.cat/meow"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
        e.set_image(url=data["file"])
        e.set_footer(text="Powered by aws.random.cat -nyan!")
        await ctx.send(embed=e)

    @commands.group(name="encode", invoke_without_command=True)
    async def encodegroup(self, ctx):
        await ctx.send("do you see this")

    @encodegroup.command(name="b64")
    async def b64(self, ctx, *, text:str=None):
        if text == None:
            raise commands.BadArgument("You can't encode no text-nyan!")
        text = text.encode()
        out = base64.b64encode(text)
        await ctx.send(f"Your encoded text: {out}")

def setup(bot):
    bot.add_cog(Fun(bot))
