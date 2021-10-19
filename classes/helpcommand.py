import discord
import os 
from discord.ext import commands

class CustomHelpCommand(commands.HelpCommand):
  def __init__(self):
    super().__init__()
    self.help = "Poll Bot is a useful discord bot used to create polls and remind users to react to polls. It enables the following commands:\n poll, pollResults, remind. Try `!help <command>` for more details"
    self.cogHelp = {
      "Poll":"Handles all Poll events with the commands: \n !poll, !pollResults, !remind. Try `!help <command>` for more details",
      "PollListener":"Detects Reactions to monitor who has/hasn't responded to a poll"
    }
    self.commandHelp = {
      "poll":"Poll command can be used to create quick polls or option polls:\nUse `-poll` for a quick poll\nUse `-poll {Title}` for a quick poll with a title\nUse `-poll {Title} [Option1] [Option2]` ... for a poll with options",
      "pollResults": "!pollResults can be used to quickly recap how many members voted for each option with the format `!pollResults <pollId>`",
      "remind": "!remind can be used to ping the members who have not responded to the poll whose ID was passed in using the format `!remind <pollId>`"
    }
    self.groupHelp = {

    }

    self.failure = "Command not found, please try !help poll for commands"

  async def send_bot_help(self, mapping):
    await self.get_destination().send(f'{self.help}')
    
  async def send_get_help(self, cog):
    if cog.qualified_name in self.cogHelp:
      await self.get_destination().send(f'{self.cogHelp[cog.qualified_name]}')
    else:
      await self.get_destination().send(self.failure)

  async def send_group_help(self, group):
    if group.name in self.groupHelp:
      await self.get_destination().send(f'{self.cogHelp[group.name]}')
    else:
      await self.get_destination().send(self.failure)

  async def send_command_help(self, command):
    if command.name in self.commandHelp:
      await self.get_destination().send(f'{self.commandHelp[command.name]}')
    else:
      await self.get_destination().send(self.failure)