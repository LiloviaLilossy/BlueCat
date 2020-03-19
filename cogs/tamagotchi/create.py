from discord import Embed, Color
from discord.ext import commands

class TamagotchiCreate(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.name = "Tamagotchi"

def setup(bot):
	bot.add_cog(TamagotchiCreate(bot))