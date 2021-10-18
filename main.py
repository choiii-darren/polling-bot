import discord
import os
from classes.polling_bot import PollBot
from replit import db

intents = discord.Intents.default()
intents.members = True

bot = PollBot(command_prefix = '!',help_command=None, disableEveryone=False, intents=intents, allowed_mentions=discord.AllowedMentions(
  users=True,
  everyone=True,
  roles=True,
  replied_user=True
))
bot.run(os.environ['BOT_TOKEN'])