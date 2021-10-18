import discord
import random
import json
from discord.ext import commands
from replit import db


class PollListener(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if self.client.user.id == payload.user_id:
      return
    self.messageReactors = dict(db["messageReactors"])
    if not (str(payload.message_id) in self.messageReactors):
      self.messageReactors[str(payload.message_id)] = []
      self.specificMessageReactors = list(self.messageReactors[str(payload.message_id)])
      self.messageReactors[str(payload.message_id)].append(str(payload.user_id))
      db["messageReactors"] = dict(self.messageReactors)
    elif (payload.user_id in self.messageReactors[str(payload.message_id)]):
      return
    else:
      self.messageReactors[str(payload.message_id)].append(str(payload.user_id))
      db["messageReactors"] = self.messageReactors
      
  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
    if self.client.user.id == payload.user_id:
      return
    self.messageReactors = db["messageReactors"]
    if len(self.messageReactors[str(payload.message_id)]) == 0:
      return
    elif (str(payload.user_id) in self.messageReactors[str(payload.message_id)]):
      self.messageReactors[str(payload.message_id)].remove(str(payload.user_id))
      db["messageReactors"] = self.messageReactors
    else:
      return

  @commands.command(name="showMsgr")
  async def showMsgr(self, ctx):
    self.messageReactors = db['messageReactors']
    print(self.messageReactors)

def setup(client):
  client.add_cog(PollListener(client))