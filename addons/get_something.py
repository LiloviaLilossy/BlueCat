import json
from discord import ChannelType
from discord.ext.commands import when_mentioned_or

def get_token(tokentype):
    with open("bot-settings/token.json", "r") as f:
        data = json.load(f)
        return data["token"][tokentype]

async def get_prefix(bot, message):
    if message.channel.type == ChannelType.private:
        return ["bc~", "Blue Cat "]
    try:
        with open(f"guild-settings/{message.guild.id}/prefixes.json", "r") as file:
            data = json.load(file)
            return when_mentioned_or(*data["prefixes"])(bot, message)
    except FileNotFoundError:
        from os import mkdir
        mkdir(f"guild-settings/{message.guild.id}")
        data = {"prefixes": ["bc~", "Blue Cat "]}
        with open(f"guild-settings/{message.guild.id}/prefixes.json", 'x') as file:
            json.dump(data, file)
        return when_mentioned_or(*data["prefixes"])(bot, message)
    #return "beta "

def get_cogs():
    from os import walk, path
    coglist = []
    for top, dirs, files in walk("cogs/"):
        for nm in files:
            if nm.endswith(".py"):
                clear = path.join(top, nm).replace("/", ".").replace("\\", ".")
                index = clear.find(".py")
                coglist.append(clear[0:index])
    return coglist

def get_smth(smth):
    with open("bot-settings/othersettings.json", "r") as f:
        data = json.load(f)
    return data["bot"][smth]
