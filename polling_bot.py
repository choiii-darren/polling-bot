import discord
import random
import logging
from discord.ext import commands

logging.basicConfig(level=logging.INFO)


class PollBot(commands.Bot):
    def __init__(self, command_prefix, help_command=..., description=None, **options):
        super().__init__(command_prefix, help_command=help_command,
                         description=description, **options)

    async def test(self, ctx, arg):
        await ctx.send('yeo {}'.format(arg))

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!hello'):
            await message.channel.send('Hello World!')
