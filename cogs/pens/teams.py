import json
from addons.check import is_in_any_team, is_team_leader
from discord import Embed, utils
from discord.ext import commands

class StarColorPensTeams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "Princesses' Star Color Pens: Teams"

    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.command(name="team-join", usage=" <name>")
    async def team_join(self, ctx, *, name=None):
        try:
            file = open(f"guild-settings/{ctx.guild.id}/colorpens.json", "r")
            data = json.load(file)
            file.close()
        except FileNotFoundError:
            return await ctx.send("Princesses' Star Color Pens is disabled here-nyan.")
        checkteams = await is_in_any_team(ctx, data)
        if checkteams == True:
            return await ctx.send("Sorry, but I'll not allow this. You have your own team.")
        if name == None:
            return await ctx.send("You know, you can't join nothing. Maybe you'll say, which team do you want to join-nyan?")
        try:
            team = data["Teams"][name]
        except KeyError:
            return await ctx.send("There are no team with that name here-nyan.")
        await ctx.send(f"Okay-nyan. <@"+str(team["Leader"])+">, there are a newbie. Do you want to accept them-nyan?")
        def check(m):
            return m.author.id == team["Leader"] and m.channel == ctx.channel
        answer = await self.bot.wait_for('message', check=check)
        if "yes" in answer.content:
            role = ctx.guild.get_role(team["TeamRole"])
            await ctx.author.add_roles(role)
            await ctx.send(f"Congrats and welcome to the {name} team-nyan!")
        else:
            await ctx.send(f"Sorry, {ctx.author.mention}, but <@"+str(team["Leader"])+"> said you can't.")

    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.command(name="team-leave", usage="")
    async def team_leave(self, ctx):
        try:
            file = open(f"guild-settings/{ctx.guild.id}/colorpens.json", "r")
            data = json.load(file)
            file.close()
        except FileNotFoundError:
            return await ctx.send("Princesses' Star Color Pens is disabled here-nyan.")
        checkteams = await is_in_any_team(ctx, data)
        if checkteams == False:
            return await ctx.send("You know, you can't leave nothing.")
        await ctx.send(f"Okay-nyan. Give me second.")
        role = ctx.guild.get_role(checkteams)
        await ctx.author.remove_roles(role)
        await ctx.send(f"Goodbye.☆")

    @commands.guild_only()
    @commands.command(name="team-info", aliases=["team"], usage=" <name>")
    async def team_info(self, ctx, *, name=None):
        try:
            file = open(f"guild-settings/{ctx.guild.id}/colorpens.json", "r")
        except FileNotFoundError:
            return await ctx.send("Princesses' Star Color Pens is disabled here-nyan.")
        if name == None:
            return await ctx.send("You know, you can't get info about nothing. Nothing is nothing. Maybe you'll say, which team do you want to know-nyan?")
        data = json.load(file)
        file.close()
        try:
            team = data["Teams"][name]
        except KeyError:
            return await ctx.send("There are no team with that name here-nyan.")
        channel = ctx.guild.get_channel(team["TeamChannel"])
        role = ctx.guild.get_role(team["TeamRole"])
        leader = utils.get(ctx.guild.members, id=team["Leader"])
        e = Embed(colour=self.bot.defaultcolor)
        e.add_field(name="Team info:", value="**Team name:** "+name+"\n**Team channel:** "+channel.mention+"\n**Team role:** "+role.mention+"\n**Member count:** "+str(len(role.members)))
        e.add_field(name="Team Leader info:", value="**Username:** "+leader.display_name+"\n**Is online?** "+str(leader.status))
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(StarColorPensTeams(bot))