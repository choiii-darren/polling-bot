import discord
import os
from classes.polling_bot import PollBot

bot = PollBot(command_prefix = '!',help_command=None)
bot.run(os.environ['BOT_TOKEN'])