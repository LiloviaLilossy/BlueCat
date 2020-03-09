import json
from addons.get_something import get_smth
from discord import Embed, utils
from discord.ext import commands
from sys import version, platform

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "Misc"
        self.owner = utils.get(self.bot.users, id=516280857468731395)

    @commands.command(name="botinfo")
    async def botinfo(self, ctx):
        embed = Embed()
        embed.add_field(name="Owner info:", value="**Username:**"+str(self.owner)+"\n**ID:**"+str(self.owner.id))
        embed.add_field(name="Bot info:", value="**Bot users:** "+str(len(self.bot.users))+"\n**Bot guilds:** "+str(len(self.bot.guilds))+"\n**Python version:** "+str(version)+"\n**OS:** "+platform)
        embed.add_field(name="Bot links:", value="**Invite:** [click here](https://discordapp.com/api/oauth2/authorize?client_id=676417304707203132&permissions=379968&scope=bot) \n**Support server:** [click here](https://discord.gg/Z2nKuYG) \n**Source code:** [click here](https://github.com/LiloviaLilossy/BlueCat)")
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=embed)

    @commands.command(name="changelog")
    async def changelog(self, ctx):
        changelog = get_smth("changelog")
        text = f"""
```
{changelog}
```
        """
        embed = Embed()
        embed.set_author(name="Owner is "+self.owner)
        embed.add_field(title="Blue Cat Changelog!", value=text)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=embed)

    @commands.command(name="prefixes")
    async def prefixes(self, ctx):
        embed = Embed()
        with open(f"guild-settings/{ctx.guild.id}/prefixes.json", "r") as file:
            data = json.load(file)
        prefixes = ""
        for prefix in data["prefixes"]:
            prefixes+="***"
            prefixes+=prefix
            prefixes+="***, "
        embed.add_field(name="Bot prefixes for "+ctx.guild.name, value=prefixes)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=embed)

    @commands.command(name="help")
    async def help(self, ctx):
        embed = Embed()
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Nyan! Blue Cat-bot v1.0")
        for cog in sorted(self.bot.cogs, reverse=True):
            help_value = ""
            c = self.bot.get_cog(cog)
            if cog == "Jishaku":
                c.name = "Jishaku"
            cmds = c.get_commands()
            if cmds != []:
                for cmd in cmds:
                    if cmd.hidden == True:
                        pass
                    elif cmd.aliases:
                        help_value += f"`{cmd} | "+" | ".join(cmd.aliases) + "`☆"
                    else:
                        help_value += f"`{cmd}`☆"
                if help_value != "":
                    embed.add_field(name=c.name, value=help_value)
        await ctx.send(embed=embed)
    
    @commands.command(name="invite")
    async def invite(self, ctx):
        e = Embed()
        e.add_field(name="Invite me to your server!", value="[here](https://discordapp.com/api/oauth2/authorize?client_id=676417304707203132&permissions=379968&scope=bot)")
        e.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=e)
    
    @commands.command(name="support")
    async def support(self, ctx):
        e = Embed()
        e.add_field(name="So, you need help with me. Here's an invite, try ask them.", value="[here](https://discord.gg/Z2nKuYG)")
        e.set_footer(text="Nyan! Blue Cat-bot v1.0")
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Misc(bot))
