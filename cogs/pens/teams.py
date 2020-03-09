import json
from discord.ext import commands

class StarColorPensTeams(commands.Cog, name="Princesses' Star Color Pens: Teams"):
    def __init__(self, bot):
        self.bot = bot


    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.command(name="team-join")
    async def team_join(self, ctx, *, name=None):
        try:
            file = open(f"guild-settings/{ctx.guild.id}/colorpens.json", "r")
        except FileNotFoundError:
            return await ctx.send("Princesses' Star Color Pens is disabled here-nyan.")
        if name == None:
            return await ctx.send("You know, you can't join nothing. Maybe you'll say, which team do you want to join-nyan?")
        data = json.load(file)
        file.close()
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

def setup(bot):
    bot.add_cog(StarColorPensTeams(bot))