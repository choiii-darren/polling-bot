import discord
import random
import logging
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

TOKEN = "ODk5MTIyMTQ3NzY5ODQ3ODA5.YWuKwA.KUl_k3wHaCRi0lebfJbE5s-6DxE"


class PollBot(commands.Bot):
    def __init__(self, command_prefix, help_command=..., description=None, **options):
        super().__init__(command_prefix, help_command=help_command,
                         description=description, **options)

    async def test(ctx, arg):
        await ctx.send('yeo {}'.format(arg))


# @PollBot.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))


# @PollBot.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('!hello'):
#         await message.channel.send('Hello!')

PollBot.run()
