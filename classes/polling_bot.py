from replit import db
import discord
import random
import os
import logging
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

class PollBot(commands.Bot):
    def __init__(self, command_prefix, help_command=..., description=None, **options):
        super().__init__(command_prefix, help_command=help_command,
                         description=description, **options)
        self.add_commands()
        for filename in os.listdir("./cogs"):
          if filename.endswith(".py"):
            self.load_extension(f'cogs.{filename[0:-3]}')

    def add_commands(self):      
      @self.command(name='load')
      async def load(ctx, extension):
        self.load_extension(f'cogs.{extension}')

      @self.command(name='unload')
      async def unload(ctx, extension):
        self.unload_extension(f'cogs.{extension}')
      
  
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

    async def on_message(self, message):
        if message.author == self.user:
            return

        await self.process_commands(message)
