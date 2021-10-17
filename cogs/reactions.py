import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class Reactions(commands.Cog):
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

  #!poll {What is your favorite emoji} [Smile Face] [Sad Face]
  #!poll -r {What is your favorite emoji}
  @commands.cooldown(6,10, BucketType.user)
  @commands.command(name="poll")
  async def poll(self, ctx):
    message = ctx.message
    if not message.author.bot:
      messageContent = message.clean_content
      if not (messageContent.find('-r')  == -1):
        await message.add_reaction('👍')
        await message.add_reaction('👎')
        await message.add_reaction('🤷')
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
        except KeyError:
          return "Please make sure you are using the format '!poll {question} [Option1] [Option2] [Option3]'"
    else: 
      return

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

    



def setup(client):
  client.add_cog(Reactions(client))