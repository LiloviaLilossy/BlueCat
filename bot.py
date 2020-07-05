from discord.ext import commands
from addons.get import *

class BlueCat(commands.Bot):
    def __init__(self):

        # Init the bot itself
        super().__init__(command_prefix=get_prefix, owner_ids=[321566831670198272, 516280857468731395])

        # Getting and loading the cogs
        self.coglist = get_cogs()
        self.load_extension("jishaku")
        for cog in self.coglist:
            self.load_extension(cog)
        
        # Other settings that are probably useless
        self.version = "2.0"

bot = BlueCat()
bot.run(get_token("discord"))
