from discord.ext import commands
from discord import Embed

class RoleCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.path = "guild-settings/{}/roles.json"
	
	@commands.group(invoke_without_command=True)
	async def autorole(self, ctx):
		e = Embed()