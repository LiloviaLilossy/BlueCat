import json
from discord.ext import commands
from discord import Member, Forbidden

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "Moderation"

    @commands.has_permissions(manage_guild=True)
    @commands.command(name="addprefix", aliases=["ap", "add-prefix"])
    async def addprefix(self, ctx, prefix):
        with open(f"guild-settings/{ctx.guild.id}/prefixes.json", "r") as file:
            data = json.load(file)
        data["prefixes"].append(prefix)
        with open(f"guild-settings/{ctx.guild.id}/prefixes.json", "w") as file:
            json.dump(data, file)
        await ctx.send(f"Fine. \"{prefix}\" will work in this guild.")
        
    @commands.has_permissions(manage_guild=True)
    @commands.command(name="removeprefix", aliases=["rp", "remove-prefix"])
    async def removeprefix(self, ctx, prefix):
        with open(f"guild-settings/{ctx.guild.id}/prefixes.json", "r") as file:
            data = json.load(file)
        try:
            data["prefixes"].remove(prefix)
            with open(f"guild-settings/{ctx.guild.id}/prefixes.json", "w") as file:
                json.dump(data, file)
            await ctx.send(f"Fine. \"{prefix}\" will not work in this guild.")
        except ValueError:
            await ctx.send(f"Don't try to fool me-nyan! This guild doesn't use \"{prefix}\" prefix!")

    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(name="ban")
    async def ban(self, ctx, user:Member=None, reason:str=None): 
        if not user:
            return await ctx.send("Do you know you can't ban nothing?")
        if not reason:
            reason = "Banned by Blue Cat, bye-bye-nyan!☆"
        try:
            await user.ban(reason=reason)
            await ctx.send("Bye-bye-nyan!☆")
        except Forbidden:
            await ctx.send("Hm. Don't you think this user is too high for me?")
        
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.command(name="kick")
    async def kick(self, ctx, user:Member=None, reason:str=None):
        if not user:
            return await ctx.send("Do you know you can't kick the air? It looks strange.")
        if not reason:
            reason = "Kicked by Blue Cat, see you later."
        try:
            await user.kick(reason=reason)
            await ctx.send("Bye-bye-nyan!☆")
        except Forbidden:
            await ctx.send("Hm. Don't you think this user is too high for me?")

def setup(bot):
    bot.add_cog(Moderation(bot))
