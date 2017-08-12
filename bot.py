import discord
from discord.ext import commands
import logging
import asyncio
import random
from io import StringIO
from datetime import datetime
from discord import Game, InvalidArgument, HTTPException
import lyricfetcher
import translate
from translate import Translator


des = "Hi, I'm /r/TapeKvlt's bot! Beep, bop, boop..."
prefix = '!'
client = commands.Bot(description=des, command_prefix=prefix);

@client.event
async def on_ready():
    print("~~~~~~~ bot is starting... ~~~~~~~~~~~~")

#################### FUNCTIONS #################################################
async def send_expiring_message(message : discord.Message, seconds):
    await client.send_message(message.channel, message)
#    await client.wait_until_ready()
    await asyncio.sleep(int(seconds)) # how many seconds before deletion
    await client.delete(message.channel, message)
################### END FUNCTIONS ##############################################

# Server Welcome
@client.event
async def on_member_join(member):
    server = member.server
    fmt = 'Everybody welcome {0.mention} to the server!'
    await client.send_message(server, fmt.format(member, server))

# LYRIC FETCHER
@client.command(pass_context=True)
async def lyrics(ctx,args):
    arr = '{}'.format(args).split(' - ')
    lyrics = lyricfetcher.get_lyrics('lyricswikia', arr[0], arr[1])
    if lyrics is None or lyrics == 404 or lyrics == '404':
        send_expiring_message(await client.say('Not found. ¯\_(ツ)_/¯ *Format:* `"Artist - Song"`'), 15)
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

##################### END WEBSITE SEARCHERS #############################


################################### MEMES #######################################
# CRISPY
@client.command(pass_context=True)
async def crispy(ctx):
    i = random.randint(0, 2)
    if i == 0: await client.say('https://i.imgur.com/YVfXE7W.gif')
    elif i == 1: await client.say('https://i.imgur.com/2SRtfz5.jpg')
    elif i == 2: await client.say('https://i.imgur.com/TiESUTE.jpg')

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
    a = await client.send_message(ctx.message.channel, 'pong')
    send_expiring_message(a, 5)
# PONG... lulz
@client.command(pass_context=True)
async def pong(ctx):
    await client.say('Hey, stop that.')
###################################################################

client.run('MzQ1NDAwODA0OTY4MTAzOTM3.DG676w.gt_HkXfpCQbxuEwoiHGACywn5Bs')

#################################################################################

# Notes

# INPUT OF INFORMATION EXAMPLE
# @client.command(pass_context=True)
# async def test(ctx,args):
#     await client.say('Your text was: {}'.format(args))
