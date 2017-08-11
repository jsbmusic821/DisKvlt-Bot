import discord
from discord.ext import commands
import logging
import asyncio
import random

des = 'This is the description inside my code file!'
prefix = '!'
client = commands.Bot(description=des, command_prefix=prefix);

@client.event
async def on_ready():
    print("Bot is starting...")

# PING
@client.command(pass_context=True)
async def ping(ctx):
    await client.say('pong')

# COIN FLIP
@client.command(pass_context=True)
async def coinflip(ctx):
    if random.randint(0, 1):
        await client.say('Heads')
    else: await client.say('Tails')

# INPUT OF INFORMATION
@client.command(pass_context=True)
async def test(ctx,args):
    await client.say('Your text was: {}'.format(args))

#################### WEBSITE SEARCHERS #################################
# Wiki command
@client.command(pass_context=True)
async def wiki(ctx,args):
    await client.say('https://en.wikipedia.org/wiki/{}'.format(args))

# Metal Archives command
@client.command(pass_context=True)
async def metal(ctx,args):
    temp = '{}'
    await client.say('https://www.metal-archives.com/search?searchString=' + temp + '&type=band_name'.format(args))

##################### END WEBSITE SEARCHERS #############################


#################### HARD CODINGS #################################
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
##################### END HARD CODINGS #############################


client.run('MzQ1NDAwODA0OTY4MTAzOTM3.DG676w.gt_HkXfpCQbxuEwoiHGACywn5Bs')
