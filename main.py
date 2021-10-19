import discord
import os
from classes.polling_bot import PollBot
from replit import db
from classes.helpcommand import CustomHelpCommand
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True

keep_alive()

bot = PollBot(command_prefix = '!',help_command=CustomHelpCommand(), disableEveryone=False, intents=intents, allowed_mentions=discord.AllowedMentions(
  users=True,
  everyone=True,
  roles=True,
  replied_user=True
))
bot.run(os.environ['BOT_TOKEN'])