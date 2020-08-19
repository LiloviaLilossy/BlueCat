from discord import Embed
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="help", invoke_without_command=True)
    async def help(self, ctx):
        embed = Embed(colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        embed.add_field(name=ctx.prefix+"help fun", value="Fun commands.", inline=False)
        embed.add_field(name=ctx.prefix+"help misc", value="Misc commands.", inline=False)
        embed.add_field(name=ctx.prefix+"help mod", value="Moderation commands.", inline=False)
        embed.add_field(name=ctx.prefix+"help owner", value="Owner commands. Only the bot owner can invoke commands in this category.", inline=False)
        await ctx.send(embed=embed)

    @help.command(name="fun")
    async def help_fun(self, ctx):
        embed = Embed(colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        cog = self.bot.get_cog("Fun")
        cmds = cog.get_commands()
        help_value = ""
        for cmd in cmds:
            if cmd.aliases:
                help_value += f"`{ctx.prefix}{cmd}|"+"|".join(cmd.aliases)+cmd.usage+"`\n"
            else:
                help_value += f"`{ctx.prefix}{cmd}{cmd.usage}`\n"
        embed.add_field(name="Fun commands!", value=help_value)
        await ctx.send(embed=embed)

    @help.command(name="misc")
    async def help_misc(self, ctx):
        embed = Embed(colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        cog = self.bot.get_cog("Misc")
        cmds = cog.get_commands()
        help_value = ""
        for cmd in cmds:
            if cmd.aliases:
                help_value += f"`{ctx.prefix}{cmd}|"+"|".join(cmd.aliases)+cmd.usage+"`\n"
            else:
                help_value += f"`{ctx.prefix}{cmd}{cmd.usage}`\n"
        embed.add_field(name="Misc commands!", value=help_value)
        await ctx.send(embed=embed)

    @help.command(name="mod")
    async def help_mod(self, ctx):
        embed = Embed(colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        cog = self.bot.get_cog("Moderation")
        cmds = cog.get_commands()
        help_value = ""
        for cmd in cmds:
            if cmd.aliases:
                help_value += f"`{ctx.prefix}{cmd}|"+"|".join(cmd.aliases)+cmd.usage+"`\n"
            else:
                help_value += f"`{ctx.prefix}{cmd}{cmd.usage}`\n"
        embed.add_field(name="Moderation commands!", value=help_value)
        await ctx.send(embed=embed)

    @help.command(name="owner")
    async def help_owner(self, ctx):
        embed = Embed(colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        cog = self.bot.get_cog("Owner")
        cmds = cog.get_commands()
        help_value = ""
        for cmd in cmds:
            if cmd.aliases:
                help_value += f"`{ctx.prefix}{cmd}|"+"|".join(cmd.aliases)+cmd.usage+"`\n"
            else:
                help_value += f"`{ctx.prefix}{cmd}{cmd.usage}`\n"
        embed.add_field(name="Owner commands! They can be invoked only by bot owner.", value=help_value)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCog(bot))
