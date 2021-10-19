import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from replit import db

class DevTools(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command(name="resetMessageReactors")
  async def resetMsgr(self, ctx):
    if not (self.is_role('coach', ctx.author) or self.is_role('player',ctx.author)):
      await ctx.channel.send("You don't have the permissions required to use this feature.")
      return
    db["messageReactors"] = {}

  @commands.command(name="showMessageReactors")
  async def showMsgr(self, ctx):
    if not (self.is_role('coach', ctx.author) or self.is_role('player',ctx.author)):
      await ctx.channel.send("You don't have the permissions required to use this feature.")
      return
    print(dict(db["messageReactors"]))

  @commands.command(name="foundRole")
  async def foundRole(self, message):
    content = message.message.content
    role = content[11:]
    await message.channel.send(self.is_role(role, message.author))

def setup(client):
  client.add_cog(DevTools(client))