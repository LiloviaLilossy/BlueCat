import json
from addons.check import is_guild_admin
from asyncio import TimeoutError
from discord import PermissionOverwrite, utils
from discord.ext import commands
from os import remove

class StarColorPens(commands.Cog, name="Princesses' Star Color Pens"):
    def __init__(self, bot):
        self.bot = bot

    @commands.check(is_guild_admin)
    @commands.guild_only()
    @commands.command(name="pen-enable", aliases=["penenable"])
    async def penenable(self, ctx):
        try:
            file = open(f"guild-settings/{ctx.guild.id}/colorpens.json", "r")
            return await ctx.send("You enabled Princesses' Star Color Pens here.")
        except FileNotFoundError:
            pass
        await ctx.send("Okay then. So you want to enable Princesses' Star Color Pens on this server-nyan. Am I right? You have only 10 seconds to answer. *only yes answer or ignore*")
        def check(m):
            return "yes" in m.content and m.author == ctx.author
        try:
            answer = await self.bot.wait_for('message', check=check, timeout=10.0)
        except TimeoutError:
            return await ctx.send("Okay, I understand you. Well, then there are less problems for me-nyan.")
        if answer:
            await ctx.send("Now I need some permissions for working: `Manage Channels`, `Manage Roles`. Send any message when you'll give me them-nyan.")
        def check(m):
            return m.author == ctx.author
        await self.bot.wait_for('message', check=check)
        perms = ctx.guild.me.guild_permissions
        if perms.manage_channels and perms.manage_roles:
            pass
        elif not perms.manage_channels or not perms.manage_roles:
            return await ctx.send("You didn't give me permissions-nyan. Do you know that it's a bad idea to ignore my words?")
        overwrites = {ctx.guild.me: PermissionOverwrite(manage_messages=True)}
        category = await ctx.guild.create_category("Princesses' Star Color Pens", overwrites=overwrites)
        channel = await ctx.guild.create_text_channel("main", category=category)
        await ctx.send("Okay, the main work is done-nyan. You can change the position of the new category I created, but you must not remove any channels from it-nyan. And the category itself too.")
        data = {"CategoryID": category.id, "MainChannelID": channel.id, "Teams": []}
        with open(f"guild-settings/{ctx.guild.id}/colorpens.json", "x") as file:
            json.dump(data, file)

    @commands.check(is_guild_admin)
    @commands.guild_only()
    @commands.command(name="pen-disable", aliases=["pendisable"])
    async def pendisable(self, ctx):
        try:
            file = open(f"guild-settings/{ctx.guild.id}/colorpens.json", "r")
        except FileNotFoundError:
            return await ctx.send("You didn't enable Princesses' Star Color Pens here-nyan.")
        data = json.load(file)
        file.close()
        mainchannel = ctx.guild.get_channel(data["MainChannelID"])
        category = mainchannel.category
        for channel in category.text_channels:
            await channel.delete()
        await category.delete()
        await ctx.send("Done. You can keep your roles, if you want.")
        remove(f"guild-settings/{ctx.guild.id}/colorpens.json")
        
def setup(bot):
    bot.add_cog(StarColorPens(bot))
