import discord
from discord.ext import commands
from discord import Permissions
import logging
import asyncio
import random
from io import StringIO
from datetime import datetime
from discord import Game, InvalidArgument, HTTPException
import lyricfetcher
import translate
from translate import Translator
import sys
import subprocess
import urllib.request
import re


des = "Hi, I'm /r/TapeKvlt's bot! Beep, bop, boop..."
prefix = '!'
client = commands.Bot(description=des, command_prefix=prefix);

@client.event
async def on_ready(): print("~~~~~~~ bot is starting... ~~~~~~~~~~~~")

#################### FUNCTIONS #################################################
################### END FUNCTIONS ##############################################

# Server Welcome
@client.event
async def on_member_join(member):
    server = member.server
    fmt = '**Hey everyone @here, welcome {0.mention} to the server!**'
    await client.send_message(server, fmt.format(member, server))

# LYRIC FETCHER
@client.command(pass_context=True)
async def lyrics(ctx,args):
    arr = '{}'.format(args).split(' - ')
    lyrics = lyricfetcher.get_lyrics('lyricswikia', arr[0], arr[1])
    if lyrics is None or lyrics == 404 or lyrics == '404':
        message = await client.say('Not found. ¯\_(ツ)_/¯ *Format:* `"Artist - Song"`')
        await asyncio.sleep(7)
        await client.delete_message(message)
    else: await client.say('```' + lyrics + '```')

# Translator
@client.command(pass_context=True)
async def trans(ctx, args, message):
    arr = '{}'.format(args).split('->')
    t = Translator(from_lang=arr[0],to_lang=arr[1])
    await client.say('```' + t.translate(message) + '```')

# COIN FLIP
@client.command(pass_context=True)
async def coinflip(ctx):
    if random.randint(0, 1): await client.say('Heads')
    else: await client.say('Tails')

# JOINED
@client.command()
async def joined(member : discord.Member):
    await client.say('{0.name} joined in {0.joined_at}'.format(member))



#################### WEBSITE SEARCHERS #################################
# Wiki command
@client.command(pass_context=True)
async def wiki(ctx,args):
    await client.say('https://en.wikipedia.org/wiki/{}'.format(args.replace(' ', '_')))

# Metal Archives command
@client.command(pass_context=True)
async def metal(ctx,args):
    temp = '{}'.format(args.replace(' ', '+'))
    await client.say('https://www.metal-archives.com/search?searchString=' + temp + '&type=band_name'.format(args))

# YouTube command
@client.command(pass_context=True)
async def yt(ctx,args):
    await client.say('https://www.youtube.com/results?search_query={}'.format(args.replace(' ', '+')))

# Discogs command
@client.command(pass_context=True)
async def discogs(ctx,args):
    temp = '{}'.format(args.replace(' ', '+'))
    await client.say('https://www.discogs.com/search?q=' + temp + '&btn=&type=all'.format(args))

# Bandcamp-search command
@client.command(pass_context=True)
async def bcsearch(ctx,args):
    await client.say('https://bandcamp.com/search?q={}'.format(args.replace(' ', '+')))

# Bandcamp command
@client.command(pass_context=True)
async def bc(ctx,args):
    temp = '{}'.format(args.replace(' ', ''))
    await client.say('https://' + temp + '.bandcamp.com'.format(args))

# Google
@client.command(pass_context=True)
async def google(ctx,args):
    temp = '{}'.format(args.replace(' ', ''))
    await client.say('https://encrypted.google.com/search?hl=en&q={}'.format(args.replace(' ', '+')))

# DuckDuckGo / Disconnect
@client.command(pass_context=True)
async def ddg(ctx,args):
    temp = '{}'.format(args.replace(' ', ''))
    await client.say('https://search.disconnect.me/searchTerms/search?query={}'.format(args.replace(' ', '+')))

##################### END WEBSITE SEARCHERS #############################


################################### MEMES #######################################
# CRISPY
@client.command(pass_context=True)
async def crispy(ctx):
    i = random.randint(0, 3)
    if i == 0: await client.say('https://i.imgur.com/YVfXE7W.gif')
    elif i == 1: await client.say('https://i.imgur.com/2SRtfz5.jpg')
    elif i == 2: await client.say('https://i.imgur.com/TiESUTE.jpg')
    elif i == 3: await client.say('https://i.imgur.com/V1qfPgl.jpg')

# ITS HAPPENING!
@client.command(pass_context=True)
async def itshappening(ctx):
    await client.say('https://i.imgur.com/7drHiqr.gif')

# RANDOM CAT
@client.command(pass_context=True)
async def cat(ctx):
    with urllib.request.urlopen("https://random.cat/meow") as url:
        rawURL = str(url.read())
    parsedURL = re.search("(?P<url>https?://[^\s]+)", rawURL).group("url")
    await client.say(parsedURL)

# YEE
@client.command(pass_context=True)
async def Yee(ctx):
    await client.say('https://www.youtube.com/watch?v=q6EoRBvdVPQ')

# Hard-coded Babooshka
@client.command(pass_context=True)
async def babooshka(ctx):
    await client.say('https://www.youtube.com/watch?v=6xckBwPdo1c')

# Hard-coded Where there's a whip, there's a way
@client.command(pass_context=True)
async def whip(ctx):
    await client.say('https://www.youtube.com/watch?v=YdXQJS3Yv0Y')

# Hard-coded Moomin Theme Song
@client.command(pass_context=True)
async def moomin(ctx):
    await client.say('https://www.youtube.com/watch?v=oiZ0eBFTH6k')
############################## END MEMES #######################################

########### Keeping for historical purposes #######################
# PING
@client.command(pass_context=True)
async def ping(ctx):
    msg = await client.say('pong')
    await asyncio.sleep(10)
    await client.delete_message(msg)
# PONG... lulz
@client.command(pass_context=True)
async def pong(ctx):
    msg = await client.say('Hey, stop that.')
    await asyncio.sleep(10)
    await client.delete_message(msg)
###################################################################

############ MAINTENANCE COMMANDS ###################################

# RESTART
@client.command(pass_context=True)
async def restart(ctx):
    author = ctx.message.author
    if str(author.top_role) == "admin":
        message = await client.say("restarting...")
        subprocess.call("./restart.sh", shell=True)
        await asyncio.sleep(10)
        await client.say("Varg has restarted. *Let's find out!*")
        subprocess.call("python3.6 ./bot.py", shell=True)
        await client.delete_message(message)
        exit()
    else: await client.say("http://e.lvme.me/xmeh35.jpg")

# KILL
@client.command(pass_context=True)
async def kill(ctx):
    author = ctx.message.author
    if str(author.top_role) == "admin":
        await client.say("*Until the light takes us...* Which is now for me. *dies*")
        await exit()
    else: await client.say("http://e.lvme.me/xmeh35.jpg")



client.run('MzQ1NDAwODA0OTY4MTAzOTM3.DG676w.gt_HkXfpCQbxuEwoiHGACywn5Bs')

#################################################################################

# Notes

# INPUT OF INFORMATION EXAMPLE
# @client.command(pass_context=True)
# async def test(ctx,args):
#     await client.say('Your text was: {}'.format(args))
