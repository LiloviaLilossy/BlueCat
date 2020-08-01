from discord import PermissionOverwrite, Embed
from discord.ext import commands
from addons import colorpens
from addons.botinput import botinput
from os import remove

class ColorPensAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = "guild-settings/{}/colorpensadmin.json"
    
    async def cog_check(self, ctx):
        if ctx.author.guild_permissions.administrator:
            return True
        else:
            return False
    
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
        inp = await botinput(bot=self.bot, ctx=ctx, typ=str, ch=check, cancel_str="no", err="That's not \"yes\" or "
                                "\"no\" answer!")
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
        await ctx.send("Excellent~nyan! Now I can create the main channel... Give me second.")
        overwrites = {
            ctx.guild.me: PermissionOverwrite(manage_messages=True, send_messages=True, read_messages=True),
            ctx.guild.default_role: PermissionOverwrite(send_messages=False, read_messages=True)
        }
        channel = await ctx.guild.create_text_channel(name="star-color-pens-main", overwrites=overwrites, 
                                                    category=ctx.channel.category)
        await channel.send(f"{ctx.author.mention}, done! Discord part is done, everything I need to do is to save the "
                        "data to the file. And, by the way. People can see this channel, but only those people who "
                        "joined the game can write here. So... If someone wants to join us, read the next message I"
                        " send.")
        colorpens.create(self.path.format(ctx.guild.id), {"enabler_id": ctx.author.id, "main_channel_id": channel.id},
                        "main")
        e = Embed(title="Blue Cat's Princess Star Color Pens Cog Starting FAQ!")
        e.add_field(name="How will I join the game?", value="It's easy~nyan! You'll need to create a character first. "
                    "You can do it by `bc~character create`. After this you'll be free to write in main channel~nyan!")
        e.add_field(name="How will I create my own team?", value="You can create your own team by `bc~team create "
                    "[name]`. Note: if you won't find someone to join your team in two days, it'll be deleted."
                    " So use it only if you're sure you have someone to team-up~nyan! \n")
        e.add_field(name="How will I join the team?", value="You can do it by `bc~team join [name]`. Your request will"
                    " be send to the team owner, and they'll decide accept you or not.")
        e.add_field(name="How to accept or decline someone in my team?", value="To accept someone to your team use "
                    "`bc~team accept [user]`. To decline... you see the logic~nyan!")
        e.add_field(name="Okay, we understood the team thing. What's after?", value="After this I'll send you the "
                    "quests and events. You'll see~nyan.")
        e.set_footer(text="Blue Cat-bot v"+self.bot.version)
        embedmsg = await channel.send(embed=e)
        await embedmsg.pin()


def setup(bot):
    bot.add_cog(ColorPensAdmin(bot))
        
