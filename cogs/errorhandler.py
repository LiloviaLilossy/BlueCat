import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
	def __init__(self, bot):
		bot.errorcolor = discord.Color.from_rgb(255, 0, 0)
		self.bot = bot
		self.name = "..."
	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		oe = discord.Embed(color=self.bot.errorcolor)
		ue = discord.Embed(color=self.bot.errorcolor)
		if isinstance(error, commands.CommandNotFound):
			ue.description = "**You did something wrong.**"
			ue.add_field(name="Command Not Found:", value="Maybe you did a typo? Anyway, it'd be better, if you'll check a help command.")
		elif isinstance(error, commands.BadArgument):
			ue.description = "**You did something wrong.**"
			ue.add_field(name="Bad Argument:", value="Do you sure you wrote everything right? Like, didn't you mess with pings or something like this?")
		elif isinstance(error, commands.NoPrivateMessage):
			ue.description = "**No DMs.**"
			ue.add_field(name="No Private Message:", value="You can't use this command in DMs, only in servers.")
		elif isinstance(error, commands.CheckFailure):
			ue.description = "**Checks failed.**"
			ue.add_field(name="Check Failure:", value="Seems like you don't have something for running this command. I'm unsure what is this something, but maybe if you'll check your permissions...")
		elif isinstance(error, commands.NotOwner):
			ue.description = "**Checks failed.**"
			ue.add_field(name="Not Owner:", value="You can't run this command because you aren't a bot owner. And that's good.")
		elif isinstance(error, commands.MissingPermissions) or isinstance(error, commands.BotMissingPermissions):
			ue.description = "**Checks failed.**"
			ue.add_field(name="Missing Permissions:", value="Maybe you'll check your and my permissions? Seems like someone from us both can't do it now.")
		else:
			ue.description = "**I don't know what happened.**"
			ue.add_field(name="Something went too wrong:", value="Seems like there are something my owner missed. I already said them about this. \n ```\n"+error+"\n```")
			oe.add_field(name="Guild ID: "+ctx.guild.id, value="Member ID: "+ctx.author.id+"\nError: \n```\n"+error+"\n```")
			channel = self.bot.get_channel(id=690255812647583879)
			await channel.send(embed=oe)
		await ctx.send(embed=ue)

def setup(bot):
	bot.add_cog(ErrorHandler(bot))