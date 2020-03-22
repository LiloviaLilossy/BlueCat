from discord.ext import commands
from json import dump, load

class BotListeners(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.name = "Bot listeners"
	
	@commands.Cog.listener()
	async def on_command_completion(self, ctx):
		with open("bot-settings/invokedcmds.json", "r") as f:
			data = load(f)
		try:
			data[ctx.command] += 1
		except KeyError:
			data[ctx.command] = 1
		with open("bot-settings/invokedcmds.json", "w") as f:
			dump(data, f)

def setup(bot):
	bot.add_cog(BotListeners(bot))