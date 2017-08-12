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
bot = commands.Bot(description=des, command_prefix=prefix);

@bot.event
async def on_ready():
    print("~~~~~~~ Bot is starting... ~~~~~~~~~~~~")

#################### FUNCTIONS #################################################

################### END FUNCTIONS ##############################################

# Server Welcome
@bot.event
async def on_member_join(member):
    server = member.server
    fmt = 'Everybody welcome {0.mention} to the server!'
    await bot.send_message(server, fmt.format(member, server))

# LYRIC FETCHER
@bot.command(pass_context=True)
async def lyrics(ctx,args):
    arr = '{}'.format(args).split(' - ')
    lyrics = lyricfetcher.get_lyrics('lyricswikia', arr[0], arr[1])
    if lyrics is None or lyrics == 404 or lyrics == '404':
        await bot.say('Not found. ¯\_(ツ)_/¯ *Format:* `"Artist - Song"`')
    else: await bot.say('```' + lyrics + '```')

# Translator
@bot.command(pass_context=True)
async def trans(ctx, args, message):
    arr = '{}'.format(args).split('->')
    t = Translator(from_lang=arr[0],to_lang=arr[1])
    await bot.say('```' + t.translate(message) + '```')

# COIN FLIP
@bot.command(pass_context=True)
async def coinflip(ctx):
    if random.randint(0, 1): await bot.say('Heads')
    else: await bot.say('Tails')

@bot.command()
async def joined(member : discord.Member):
##  Says the date when a member joined.
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

#################### WEBSITE SEARCHERS #################################
# Wiki command
@bot.command(pass_context=True)
async def wiki(ctx,args):
    await bot.say('https://en.wikipedia.org/wiki/{}'.format(args.replace(' ', '_')))

# Metal Archives command
@bot.command(pass_context=True)
async def metal(ctx,args):
    temp = '{}'.format(args.replace(' ', '+'))
    await bot.say('https://www.metal-archives.com/search?searchString=' + temp + '&type=band_name'.format(args))

# YouTube command
@bot.command(pass_context=True)
async def yt(ctx,args):
    await bot.say('https://www.youtube.com/results?search_query={}'.format(args.replace(' ', '+')))

# Discogs command
@bot.command(pass_context=True)
async def discogs(ctx,args):
    temp = '{}'.format(args.replace(' ', '+'))
    await bot.say('https://www.discogs.com/search?q=' + temp + '&btn=&type=all'.format(args))

# Bandcamp-search command
@bot.command(pass_context=True)
async def bcsearch(ctx,args):
    await bot.say('https://bandcamp.com/search?q={}'.format(args.replace(' ', '+')))

# Bandcamp command
@bot.command(pass_context=True)
async def bc(ctx,args):
    temp = '{}'.format(args.replace(' ', ''))
    await bot.say('https://' + temp + '.bandcamp.com'.format(args))

##################### END WEBSITE SEARCHERS #############################


################################### MEMES #######################################
# CRISPY
@bot.command(pass_context=True)
async def crispy(ctx):
    i = random.randint(0, 2)
    if i == 0: await bot.say('https://i.imgur.com/YVfXE7W.gif')
    elif i == 1: await bot.say('https://i.imgur.com/2SRtfz5.jpg')
    elif i == 2: await bot.say('https://i.imgur.com/TiESUTE.jpg')

# YEE
@bot.command(pass_context=True)
async def Yee(ctx):
    await bot.say('https://www.youtube.com/watch?v=q6EoRBvdVPQ')

# Hard-coded Babooshka
@bot.command(pass_context=True)
async def babooshka(ctx):
    await bot.say('https://www.youtube.com/watch?v=6xckBwPdo1c')

# Hard-coded Where there's a whip, there's a way
@bot.command(pass_context=True)
async def whip(ctx):
    await bot.say('https://www.youtube.com/watch?v=YdXQJS3Yv0Y')

# Hard-coded Moomin Theme Song
@bot.command(pass_context=True)
async def moomin(ctx):
    await bot.say('https://www.youtube.com/watch?v=oiZ0eBFTH6k')
############################## END MEMES #######################################

########### Keeping for historical purposes #######################
# PING
@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say('pong')
# PONG... lulz
@bot.command(pass_context=True)
async def pong(ctx):
    await bot.say('Hey, stop that.')
###################################################################

bot.run('MzQ1NDAwODA0OTY4MTAzOTM3.DG676w.gt_HkXfpCQbxuEwoiHGACywn5Bs')

#################################################################################

# Notes

# INPUT OF INFORMATION EXAMPLE
# @bot.command(pass_context=True)
# async def test(ctx,args):
#     await bot.say('Your text was: {}'.format(args))
