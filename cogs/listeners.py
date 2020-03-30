from discord import Game, ActivityType, Activity
from discord.ext import commands, tasks
from json import dump, load
from random import choice

class BotListeners(commands.Cog):
    def __init__(self, bot):
        self.name = "Bot listeners"
        self.presence.start()
        self.bot = bot

    def cog_unload(self):
        self.presence.cancel()

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        with open("bot-settings/invokedcmds.json", "r") as f:
            data = load(f)
        try:
            data[str(ctx.command)] += 1
        except KeyError:
            data[str(ctx.command)] = 1
        with open("bot-settings/invokedcmds.json", "w") as f:
            dump(data, f)

    @tasks.loop(minutes=5)
    async def presence(self):
        with open("bot-settings/othersettings.json", "r") as f:
            data = load(f)
        presences = data["bot"]["presences"]
        ptype = choice(list(presences))
        text = choice(presences[ptype])
        if ptype == "playing":
            presence = Game(name=text+" | bc~help")
        elif ptype == "listening":
            presence = Activity(name=text+" | bc~help", type=ActivityType.listening)
        elif ptype == "watching":
            presence = Activity(name=text+" | bc~help", type=ActivityType.watching)
        await self.bot.change_presence(activity=presence)

    async def bot_check(self, ctx):
        with open("bot-settings/banned.json", "r") as f:
            self.banned = (load(f))["ban"]
        if ctx.author.id in self.banned:
            raise commands.CheckFailure("You've been banned from using my commands-nyan.")
        else: return True

    @presence.before_loop
    async def before_presence(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(BotListeners(bot))
