import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from replit import db

class Poll(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.emojiLetters = [
            "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
            "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER T}"
        ]

  @commands.cooldown(2,60, BucketType.user)
  @commands.command(name="poll")
  async def poll(self, ctx):
    message = ctx.message
    if not (self.is_role('coach', ctx.author) or self.is_role('player',ctx.author)):
      await message.channel.send("You don't have the permissions required to use this feature.")
      return
    if not message.author.bot:
      messageContent = message.clean_content 
      if (messageContent.find("[") == -1):
        if (self.find_question(messageContent) == "Use the Polling feature by containing your question in {}."):
          question = "Quick Poll"
        else:
          question =  self.find_question(messageContent)
        reactionMessage = await message.channel.send(question)
        await reactionMessage.add_reaction('👍')
        await reactionMessage.add_reaction('👎')
        await reactionMessage.add_reaction('🤷')
        await message.channel.send(f"Poll ID: {str(reactionMessage.id)}")
        await message.delete()
      else:
        title = self.find_question(messageContent)
        options = self.find_options(messageContent, [])
        if (type(options) == int):
          await message.channel.send("Give me more than 1 option!")
          return

        try:
          pollMessage = ''
          i = 0
          for choice in options:
            if not options[i] == '':
              if len(options) > 20:
                await message.channel.send('Limit of 20 reactions :(')
                return
              elif not i == len(options):
                pollMessage = pollMessage + "\n" + self.emojiLetters[i] + " " + choice
              i += 1

          e = discord.Embed(title='**' + title + '**', description=pollMessage, colour=0x83bae3)
          pollMessage = await message.channel.send(embed=e)
          i = 0
          final_options = []
          for choice in options:
            if not i == len(options) and not options[i] == "":
             final_options.append(choice)
             await pollMessage.add_reaction(self.emojiLetters[i])
            i += 1
          await message.channel.send(f"Poll ID: {str(pollMessage.id)}")
          await message.delete()
        except KeyError:
          return "Please make sure you are using the format '!poll {question} [Option1] [Option2] [Option3]'"
    else: 
      return
  
  @commands.cooldown(3, 30, BucketType.user)
  @commands.command(name="remind")
  async def remind(self, ctx, arg):
    if not (self.is_role('coach', ctx.author) or self.is_role('player',ctx.author)):
      await ctx.channel.send("You don't have the permissions required to use this feature.")
      return
    self.messageReactors = dict(db['messageReactors'])
    self.pollKey = arg
    if (len(arg) == 0):
      await ctx.channel.send("You forgot to include the pollID, please use `!remind <pollId>`")
      return
    try:
      await ctx.fetch_message(int(self.pollKey))
    except:
      await ctx.channel.send("The pollID you inserted does not exist, please use a valid pollID!")
      return      
    if not (str(self.pollKey) in self.messageReactors) or len(self.messageReactors[str(self.pollKey)]) == 0:
      await ctx.channel.send('No one has responded to this poll yet! @everyone')
      return
    self.specificMessageReactors = self.messageReactors[str(self.pollKey)]
    #get all channel dudes
    #channel = self.client.get_channel(ctx.channel.id)
    #if they exist in the database, take them out of the array
    members= ctx.channel.members
    memids = []
    for member in members:
      memids.append(member.id)
      if (member.id == self.client.user.id):
        memids.remove(member.id)
    for reactors in self.specificMessageReactors:
      for member in memids:
        if str(member) == reactors:
          memids.remove(member)
    #mention all users
    if len(memids) == 0:
      await ctx.channel.send('Everyone responded! Yay!')
      return
    responseMessage = f'The following have not responded to Poll {self.pollKey}: \n'
    for member in memids:
      responseMessage += f"<@{member}> \n"
    await ctx.channel.send(responseMessage)
    
  @commands.cooldown(3, 30, BucketType.user)
  @commands.command(name="pollResults")
  async def pollResults(self, ctx, arg):
    if not (self.is_role('coach', ctx.author) or self.is_role('player',ctx.author)):
      await ctx.channel.send("You don't have the permissions required to use this feature.")
      return
    self.pollKey = arg
    if (len(arg) == 0):
      await ctx.channel.send("You forgot to include the pollID, please use `!remind <pollId>`")
      return
    try:
      await ctx.fetch_message(int(self.pollKey))
    except:
      await ctx.channel.send("The pollID you inserted does not exist, please use a valid pollID!")
      return    
    message = await ctx.fetch_message(int(self.pollKey))
    returnString = (f'Poll results for Poll {self.pollKey} are: \n')
    for reaction in message.reactions:
        returnString += f'{reaction.emoji} was voted {str(int(reaction.count) - 1)} time(s)\n'
    await ctx.channel.send(returnString)

  def find_question(self, message):
    first = message.find('{') + 1 
    last = message.find('}')
    if first == 0 or last == -1:
      return "Use the Polling feature by containing your question in {}."
    return message[first:last]
  
  def find_options(self,message, options):
    first = message.find('[') + 1
    last = message.find(']')
    if (first == 0 or last == -1):
      if len(options) < 2:
        return -1
      else:
        return options
    options.append(message[first:last])
    message = message[last+1:]
    return self.find_options(message,options)
  
  def is_role(self, role, author):
    for y in author.roles:
      if role.lower() == str(y).lower():
        return True
    return False


def setup(client):
  client.add_cog(Poll(client))