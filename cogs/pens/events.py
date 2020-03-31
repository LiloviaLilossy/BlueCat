from discord.ext import commands, tasks
from json import load
from random import randint, choice

class StarColorPensEvents(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.name = "Princesses' Star Color Pens: Events"
		self.lastid = None
		# self.minutes = randint(1, 60)
	
	@tasks.loop(minutes=1)
	async def event_send(self):
		# self.minutes = randint(1, 60)
		for guild in self.bot.guilds:
			if guild.id == self.lastid: continue
			try: 
				settings = open(f"guild-settings/{guild.id}/colorpens.json", "r")
				self.lastid = guild.id
				data = load(settings)
				settings.close()
				break
			except FileNotFoundError: pass
		if not data: return

		event_send.change_interval(minutes=randint(1,5))

def setup(bot):
	bot.add_cog(StarColorPensEvents(bot))