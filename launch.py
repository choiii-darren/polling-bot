import discord
import json
from polling_bot import PollBot

f = open('config.json')
bot = PollBot("!",None)
bot.run(json.load(f)["bot_token"])