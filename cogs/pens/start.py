import json
from addons.check import *
from asyncio import TimeoutError
from discord import PermissionOverwrite, utils, Member
from discord.ext import commands
from os import remove

class StarColorPensStart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name="Princesses' Star Color Pens: Start"

    @commands.check(is_guild_admin)
    @commands.guild_only()
    @commands.command(name="pen-enable")
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
    @commands.command(name="pen-disable")
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

    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True, manage_channels=True)
    @commands.command(name="team-create", aliases=["create-team"])
    async def team_create(self, ctx, *, name:str=None):
        try:
            file = open(f"guild-settings/{ctx.guild.id}/colorpens.json", "r")
        except FileNotFoundError:
            return await ctx.send("Princesses' Star Color Pens is disabled here-nyan.")
        data = json.load(file)
        file.close()
        mainchannel = ctx.guild.get_channel(data["MainChannelID"])
        if name == None:
            await ctx.send("Hey, you need a team name, after all. I'll wait for a minute, when you'll send me the name-nyan.")
            def check(m):
                return m.author == ctx.author
            try:
                answer = await self.bot.wait_for('message', check=check, timeout=60.0)
            except TimeoutError:
                return await ctx.send("Okay, then you don't want to create the team. Sadly-nyan.")
            name = answer.content
            await ctx.send(f"Okay-nyan, you called the team {name}.")
        teamrole = await ctx.guild.create_role(name=name, reason="Creating a team role.")
        await ctx.author.add_roles(teamrole)
        msg = "Okay-nyan, I created a role and gave it to the leader. (it's you)"
        await ctx.send(msg)
        overwrites = {ctx.guild.me: PermissionOverwrite(manage_messages=True, send_messages=True), 
                    teamrole: PermissionOverwrite(send_messages=True, read_messages=True),
                    ctx.author: PermissionOverwrite(manage_messages=True),
                    ctx.guild.default_role: (PermissionOverwrite(read_messages=False, send_messages=False))}
        teamchannel = await ctx.guild.create_text_channel(name=name.lower().replace(" ", "-"), overwrites=overwrites, category=mainchannel.category, reason="Creating a team chat.")
        await teamchannel.send(f"{ctx.author.mention}, there's your chat.")
        data["Teams"][name] = {"Leader": ctx.author.id, "TeamRole": teamrole.id, "TeamChannel": teamchannel.id}
        with open(f"guild-settings/{ctx.guild.id}/colorpens.json", "w") as file:
            json.dump(data, file)

    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True, manage_channels=True)
    @commands.command(name="team-remove", aliases=["remove-team"])
    async def team_remove(self, ctx, *, name:str = None):
        try:
            file = open(f"guild-settings/{ctx.guild.id}/colorpens.json", "r")
        except FileNotFoundError:
            return await ctx.send("Princesses' Star Color Pens is disabled here-nyan.")
        data = json.load(file)
        file.close()
        if name == None:
            return await ctx.send("I can't remove nothing, tell your team's name.")
        try:
            team = data["Teams"][name]
        except KeyError:
            return await ctx.send("There are no team with that name here-nyan.")
        if team["Leader"] != ctx.author.id:
            return await ctx.send("Hey! You aren't the owner of this team!")
        await ctx.send(f"Okay. Goodbye, {name}")
        teamchannel = ctx.guild.get_channel(team["TeamChannel"])
        teamrole = ctx.guild.get_role(team["TeamRole"])
        await teamchannel.delete()
        await teamrole.delete()
        del data["Teams"][name]
        with open(f"guild-settings/{ctx.guild.id}/colorpens.json", "w") as file:
            json.dump(data, file)

        
def setup(bot):
    bot.add_cog(StarColorPensStart(bot))
