from discord.ext import commands
from addons import colorpens
from addons.botinput import botinput

class ColorPensAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = "guild-settings/{}/colorpensadmin.json"
    
    @commands.group(name="colorpens", invoke_without_command=False)
    async def pen(self, ctx):
        return
    
    @pen.command(name="enable")
    async def pen_enable(self, ctx):
        try:
            i = colorpens.load_info(self.path.format(ctx.guild.id))
            del i
            return await ctx.send("You already enabled the game!")
        except: pass
        def check(m):
            return m.lower() == "yes"
        await ctx.send("So, you want to join our game and find Star Color Pens~nyan... That's good, I think. "
                    "But before I let you to start the adventure, I need to ask some questions first. Are you ready?")
        inp = await botinput(ctx, str, ch=check, cancel_str="no", err="That's not \"yes\" or \"no\" answer!")
        if inp == None:
            return await ctx.send("Okay, if you don't want to join us, it's fully okay~nyan. It will be even easier.")
        await ctx.send("Okay, fine. The next question. I'll need some additional permissions: "
                    "`Manage Channels` and `Manage Roles`. You could ask why do I need them? See. "
                    "I'll create the channel, where you and the other players will see the everything related to "
                    "this game, if that touches your server. I'll need Manage Roles for creating teams: when someone "
                    "creates the team, I'll create the channel which will be visible only to the people who has "
                    "the team's role. Everything you need is to give me those permissions and write anything here.")
        await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author == ctx.author)
        permissions = ctx.guild.me.guild_permissions
        if not permissions.manage_channels or not permissions.manage_roles:
            return await ctx.send("You didn't give me permissions. Aborting...")
        
