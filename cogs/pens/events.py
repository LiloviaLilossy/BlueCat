from discord.ext import commands, tasks
from json import load
from random import randint, choice

class StarColorPensEvents(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.name = "Princesses' Star Color Pens: Events"
		self.minutes = randint(1, 60)
	
	@tasks.loop(minutes=self.minutes)
	async def event_send(self):
		self.minutes = randint(1, 60)
		for guild in self.bot.guilds:
			try: 
				settings = open(f"guild-settings/{guild.id}/colorpens.json", "r")
				break
			except FileNotFoundError: pass
		data = load(settings)
		settings.close()

def setup(bot):
	bot.add_cog(StarColorPensEvents(bot))