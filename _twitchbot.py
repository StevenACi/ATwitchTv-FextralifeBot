from twitchio.ext import commands as commands
from bs4 import BeautifulSoup as soup
import requests
import re 

token = "oauth:thisisnotarealoathtoken" # Oauth2 token that you generate
name = "NancyBot" # The bots username
channel = "Placeholder" # Twitch channel you are targetting

bot = commands.Bot(
            irc_token=token,
            api_token='test',
            nick=name,
            prefix='~',
            initial_channels=[channel])

# Register an event with the bot
@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')


@bot.event
async def event_message(message):
    print(message.content)

    # If you override event_message you will need to handle_commands for commands to work.
    await bot.handle_commands(message)

# TwitchIO event
async def event_message(self, message):
    print(message.content)
    # store message with time stamp

    await self.handle_commands(message)

# Register a command with the bot
@bot.command(name='wiki', aliases=['##'])
async def get_wikipage(ctx):
    words = ctx.message.content.split(' ')[1:]


    url = "https://finalfantasy7remake.wiki.fextralife.com/" # Base URL for the fextralife wiki

    poststring = "" 
    for x in words:
        poststring += x
        poststring += '+'
    poststring = poststring[:-1]
    url += poststring
    print("\t" + url)
    req = requests.get(url, auth=('user','pass'))

    page = soup(req.content, 'html.parser')
    paragraph = page.find(id="wiki-content-block").get_text()

    # Get the first 400 words from the wiki page
    paragraph = re.sub("\s\s+", " ", paragraph)[:400] 
    print(paragraph)
    if re.findall('404 ERROR',paragraph):
        print("errorpage")
        await ctx.send(f'Check spelling.. {ctx.author.name}' )
    else:
        await ctx.send(f'{ctx.author.name}, Here.. {paragraph}') 


bot.run()