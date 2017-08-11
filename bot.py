import discord
from discord.ext import commands
import logging
import asyncio
import random
import sys
import os
from io import StringIO
from datetime import datetime
from discord import Game, InvalidArgument, HTTPException


des = 'This is the description inside my code file!'
prefix = '!'
client = commands.Bot(description=des, command_prefix=prefix);

@client.event
async def on_ready():
    print("Bot is starting...")

# Server Welcome
@client.event
async def on_member_join(member):
    server = member.server
    fmt = 'Everybody welcome {0.mention} to the server!'
    await client.send_message(server, fmt.format(member, server))

########### Keeping for historical purposes #######################
# PING
@client.command(pass_context=True)
async def ping(ctx):
    await client.say('pong')
# PONG... lulz
@client.command(pass_context=True)
async def pong(ctx):
    await client.say('Hey, stop that.')
###################################################################

# COIN FLIP
@client.command(pass_context=True)
async def coinflip(ctx):
    if random.randint(0, 1):
        await client.say('Heads')
    else: await client.say('Tails')

# INPUT OF INFORMATION EXAMPLE
@client.command(pass_context=True)
async def test(ctx,args):
    await client.say('Your text was: {}'.format(args))

@client.command()
async def joined(member : discord.Member):
##  Says the date when a member joined.
    await client.say('{0.name} joined in {0.joined_at}'.format(member))

#################### WEBSITE SEARCHERS #################################
# Wiki command
@client.command(pass_context=True)
async def wiki(ctx,args):
    await client.say('https://en.wikipedia.org/wiki/{}'.format(args))

# Metal Archives command
@client.command(pass_context=True)
async def metal(ctx,args):
    temp = '{}'.format(args)
    await client.say('https://www.metal-archives.com/search?searchString=' + temp + '&type=band_name'.format(args))

# YouTube command
@client.command(pass_context=True)
async def yt(ctx,args):
    await client.say('https://www.youtube.com/results?search_query={}'.format(args))

# Discogs command
@client.command(pass_context=True)
async def discogs(ctx,args):
    temp = '{}'.format(args)
    await client.say('https://www.discogs.com/search?q=' + temp + '&btn=&type=all'.format(args))

# Bandcamp command
@client.command(pass_context=True)
async def bandcamp(ctx,args):
    await client.say('https://bandcamp.com/search?q={}'.format(args))
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


##################### ADMIN-ONLY COMMANDS ############################
async def update_avatar(name, picture):
    picture = f"config/{picture}"
    if os.path.isfile(picture):
        with open(picture, "rb") as avatar:
            await bot.edit_profile(avatar=avatar.read())

# async def update_avatar(name, picture):
#     picture = f"config/{picture}"
#     if os.path.isfile(picture):
#         with open(picture, "rb") as avatar:
#             await bot.edit_profile(avatar=avatar.read())
################ END ADMIN-ONLY COMMANDS ##############################


client.run('MzQ1NDAwODA0OTY4MTAzOTM3.DG676w.gt_HkXfpCQbxuEwoiHGACywn5Bs')



#################################################################################

# NOTES

# allows you to send a message to a specific channel:
"""
def send_to_bot_channel(content):
    for server in client.servers:
        for channel in server.channels:
            if channel.name.casefold() == "chat-bot".casefold():
                client.send_message(channel, content)
                """
