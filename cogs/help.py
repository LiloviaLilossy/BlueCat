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
        if ctx.prefix == "<@!676417304707203132> " or ctx.prefix == "<@!691358641886068766> ": #2nd is beta
            ctx.prefix = "@Blue Cat "
        embed.add_field(name=ctx.prefix+"help colorpens", value="Star Color Pens commands. For most of them bot requires"
            " `Manage Roles` and `Manage Channels` permissions.", inline=False)
        embed.add_field(name=ctx.prefix+"help fun", value="Fun commands.", inline=False)
        embed.add_field(name=ctx.prefix+"help misc", value="Misc commands.", inline=False)
        embed.add_field(name=ctx.prefix+"help mod", value="Moderation commands.", inline=False)
        embed.add_field(name=ctx.prefix+"help owner", value="Owner commands. Only the bot owner can invoke commands in this category.", inline=False)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(HelpCog(bot))
