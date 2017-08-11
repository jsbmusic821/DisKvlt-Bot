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

@client.command(pass_context=True)
async def ping(ctx):
    await client.say('pong')

@client.command(pass_context=True)
async def coinflip(ctx):
    if random.randint(0, 1):
        await client.say('Heads')
    else: await client.say('Tails')

client.run('MzQ1NDAwODA0OTY4MTAzOTM3.DG676w.gt_HkXfpCQbxuEwoiHGACywn5Bs')
