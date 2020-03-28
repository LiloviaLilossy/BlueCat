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
        embed.set_image(url="https://media.discordapp.net/attachments/616645258280828949/691873653188460584/botinfo.png")
        #for cog in sorted(self.bot.cogs, reverse=True):
        #    help_value = ""
        #    c = self.bot.get_cog(cog)
        #    if cog == "Jishaku":
        #        c.name = "Jishaku"
        #    cmds = c.get_commands()
        #    if cmds != []:
        #        for cmd in cmds:
        #            if cmd.hidden == True:
        #                pass
        #            elif cmd.aliases:
        #                help_value += f"`{cmd} | "+" | ".join(cmd.aliases) + "`☆"
        #            else:
        #                help_value += f"`{cmd}`☆"
        #        if help_value != "":
        #            embed.add_field(name=c.name, value=help_value)
        embed.add_field(name=ctx.prefix+"help colorpens", value="Star Color Pens commands. For most of them bot requires"
            " `Manage Roles` and `Manage Channels` permissions.")
        embed.add_field(name=ctx.prefix+"help fun", value="Fun commands.")
        embed.add_field(name=ctx.prefix+"help misc", value="Misc commands.")
        embed.add_field(name=ctx.prefix+"help mod", value="Moderation commands.")
        embed.add_field(name=ctx.prefix+"help owner", value="Owner commands. Only the bot owner can invoke commands in this category.")
        await ctx.send(embed=embed)

    @help.command(name="colorpens")
    async def help_colorpens(self, ctx):
        embed = Embed(colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        embed.set_image(url="https://media.discordapp.net/attachments/616645258280828949/691873653188460584/botinfo.png")
        start = self.bot.get_cog("StarColorPensStart")
        teams = self.bot.get_cog("StarColorPensTeams")
        help_value = ""
        for cog in [start, teams]:
            cmds = cog.get_commands()
            for cmd in cmds:
                if cmd.aliases:
                    help_value += f"`{ctx.prefix}{cmd}|"+"|".join(cmd.aliases)+"`\n"
                else:
                    help_value += f"`{ctx.prefix}{cmd}`\n"
        embed.add_field(name="Star Color Pens!", value=help_value)
        await ctx.send(embed=embed)

    @help.command(name="fun")
    async def help_fun(self, ctx):
        embed = Embed(colour=self.bot.defaultcolor)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        embed.set_image(url="https://media.discordapp.net/attachments/616645258280828949/691873653188460584/botinfo.png")
        cog = self.bot.get_cog("Fun")
        cmds = cog.get_commands()
        help_value = ""
        for cmd in cmds:
            if cmd.aliases:
                help_value += f"`{ctx.prefix}{cmd}|"+"|".join(cmd.aliases)+"`\n"
            else:
                help_value += f"`{ctx.prefix}{cmd}`\n"
        embed.add_field(name="Fun commands!", value=help_value)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCog(bot))
