import discord
from discord.ext import commands
from discord.ext import asyncio
from discord.ext import async
import logging
#import asyncio

des = 'This is the description inside my code file!'

prefix = '!'

client = commands.Bot(description=des, command_prefix=prefix);

@client.event
async def on_ready();
    print("Hello world!")

@client.command(pass_context=True)
async def ping(ctx):
    await client.say('pong')

client.run('MzQ1NDAwODA0OTY4MTAzOTM3.DG676w.gt_HkXfpCQbxuEwoiHGACywn5Bs')
