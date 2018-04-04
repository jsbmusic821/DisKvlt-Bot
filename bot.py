import discord
from discord.ext import commands
from discord import Permissions
import logging
import asyncio
import random
from datetime import datetime
from discord import Game, InvalidArgument, HTTPException
import lyricfetcher
import translate
from translate import Translator
import sys
import re
import requests
import json
import urllib
from bs4 import BeautifulSoup
from os import system
from time import sleep
from discord import opus

from globals import *
import globals
from emojis import *
from admin_utils import *
from pinboard import on_pushpin,remove_pin
from bookmark import on_bookmark
from banned import is_banned
from hatespeech import check_hate_speech
from image_search import search_for_image
from releases import get_releases
from bandpic import get_band_pic

client = commands.Bot(description="Hi, I'm DisKvlt's bot! Find my brain at http://github.com/mitchweaver/diskvlt-bot",\
                      command_prefix='!');

# opus.load_opus('libopus.so.0')
music_links_log="/home/banana/music_links_log.txt"

# server
diskvlt = ""

@client.event
async def on_ready():
    global diskvlt
    for server in client.servers:
        if server.name.lower() == "diskvlt":
            diskvlt = server
    print("~~~~~~~~~~~~ bot has started... ~~~~~~~~~~~~")


# BOOKMARK / PIN
@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == bookmark_emoji:
        await on_bookmark(reaction, user, client)
    elif reaction.emoji == pushpin_emoji:
        await on_pushpin(reaction, user, client, diskvlt)

# Remove Reaction
@client.event
async def on_reaction_remove(reaction, user):
    # delete message in #pin_board on removal of pushpin emoji
    if reaction.emoji == pushpin_emoji:
        await remove_pin(reaction.message, client)


# Server Welcome
@client.event
async def on_member_join(member):
    i = 0
    for m in diskvlt.members: i += 1
    msg = '**𝖂𝖊𝖑𝖈𝖔𝖒𝖊 𝖙𝖔 𝖙𝖍𝖊 𝖘𝖊𝖗𝖛𝖊𝖗 ' + member.mention + '!** ' + str(wavedog)
    await client.send_message(diskvlt, msg + "\n" + \
                "There are now **" + str(i) + "** members in the server!")

    for channel in diskvlt.channels:
        if channel.name == "bot_zone":
            await client.send_message(channel, member.mention \
                + " Welcome! I can do a lot of cool things. \n Use `!help`" \
                + " to find out more! " + str(vargbeanie))
            break

# Metal Archives releases scraper
@client.command(pass_context=True)
async def releases(ctx, *args):
    """Scrapes metal-archives for relases from <band>"""
    await get_releases(ctx, client, args)

# Metal Archives band pic scraper
@client.command(pass_context=True)
async def band(ctx, *args):
    """Scrapes metal-archives for band pic of <band>"""
    await get_band_pic(ctx, client, args)

# LYRIC FETCHER
@client.command(pass_context=True)
async def lyrics(ctx, *args):
    """Ex: '!lyrics artist name - song name'"""
    try:
        arr = '{}'.format(" ".join(args)).split(' - ')
        lyrics = lyricfetcher.get_lyrics('lyricswikia', arr[0], arr[1])
        if lyrics is None or lyrics == 404 or lyrics == "404":
            message = await client.say('Not found. ¯\_(ツ)_/¯ \
                                    *Format:* `"Artist - Song"`')
            await asyncio.sleep(10)
            await client.delete_message(message)
        else: await client.say('```' + lyrics + '```')
    except:
        await client.send_message(ctx.message.channel, \
            "Bad syntax - Format: `artist - song`")

# Translator
@client.command(pass_context=True)
async def trans(ctx, *args):
    """Ex: '!trans en->de example' OR '!trans de Beispiel'"""
    if "bugs" in args[0]:
        await client.say("Wraith... bugs is not a language.")
        return

    if len(args[0]) == 2:
        arr = [args[0], "en"]
    else: arr = '{}'.format(args[0]).split('->')
    t = Translator(from_lang=arr[0],to_lang=arr[1])
    await client.say('```' + t.translate(" ".join(args[1:])) + '```')

# Image
@client.command(pass_context=True)
async def image(ctx, *args):
    """Downloads the first image from google images and uploads it as a file"""
    await search_for_image(ctx, client, args)

# alias for images
@client.command(pass_context=True)
async def images(ctx, *args):
    await search_for_image(ctx, client, args)

# JOINED
@client.command()
async def joined(member : discord.Member):
    """Datestamp of user join - Ex: '!joined mitch'"""
    await client.say('{0.name} joined in {0.joined_at}'.format(member))

# Total Messages
# ---- this just gets totally abused
# @client.command(pass_context=True)
# async def total(ctx):
#     """Calculates total number of messages sent by you on the server - Please don't abuse this"""

#     author = ctx.message.author

#     start_message = await client.say(author.mention \
#             + " Working. This may take a while...")

#     from threading import Thread
#     count = 0
#     for channel in diskvlt.channels:
#         if channel.type == discord.ChannelType.text:
#             # try:
#             print("Starting to count messages in: " + channel.name)
#             async for message in client.logs_from(channel, limit=100000000):
#                 if message.author == author:
#                     count += 1
#                     print(count)
#             # except: continue

#     await client.delete_message(start_message)
#     await client.say(author.mention + " has sent " + str(count) \
#                      + " messages on the server")
#     print("Finished calculating total for user: " + author.mention)

# AGE
@client.command(pass_context=True)
async def age(ctx):
    """Datestamp of server's age"""
    for member in diskvlt.members:
        if member is diskvlt.owner:
            await client.say("The server was created on " \
                                + "{0.joined_at}".format(member))
            return

# MEMBERS
@client.command(pass_context=True)
async def members(ctx):
    """"Displays number of registered users"""
    i = 0
    for member in diskvlt.members: i += 1
    await client.say("There are **" + str(i) + "** members in the server!")


# Debug
@client.command(pass_context=True)
async def ban(ctx, args):
    """(admin) - Ex: '!ban user'"""
    try:
        if ctx.message.author.name == "mitch" or \
            ctx.message.author.top_role.name.lower() == "admin":
                globals.banned_users.add(" ".join(args))
    except:
        pass

#################### WEBSITE SEARCHERS #################################
# Wiki command
@client.command(pass_context=True)
async def wiki(ctx,*args):
    """Searches Wikipedia"""
    await client.say('https://en.wikipedia.org/wiki/{}'.format(" ".join(args).replace(' ', '_')))

# Metal Archives
@client.command(pass_context=True)
async def metal(ctx, *args):
    """Grabs metal-archives page for <band> - Ex: '!metal foo bar'"""
    await client.say('https://www.metal-archives.com/bands/' \
                     + '{}'.format(" ".join(args).replace(' ', '_')))

# YouTube command
@client.command(pass_context=True)
async def yt(ctx, *args):
    """Search and link a youtube video"""

    url = "https://www.youtube.com/results?search_query=" + \
            urllib.parse.quote(" ".join(args).lower())

    for vid in BeautifulSoup(urllib.request.urlopen(url).read(), \
            "html5lib").findAll(attrs={'class': 'yt-uix-tile-link'}, \
            limit = 1):
        if "user" not in vid["href"] and "googleads" not in vid["href"]:
            await client.say('https://www.youtube.com' + vid['href'])
            break

# Discogs command
@client.command(pass_context=True)
async def discogs(ctx,*args):
    """Search Discogs.com"""
    await client.say('https://www.discogs.com/search?q=' \
                     + '{}'.format(" ".join(args).replace(' ', '+')) \
                     + '&btn=&type=all'.format(" ".join(args)))

# Bandcamp command
@client.command(pass_context=True)
async def bc(ctx,args):
    """Link a bandcamp page - Note: must be exact"""
    temp = '{}'.format(args.replace(' ', ''))
    await client.say('https://' \
                     + '{}'.format(args.replace(' ', '')) \
                     + '.bandcamp.com'.format(args))

# Google
@client.command(pass_context=True)
async def google(ctx,*args):
    """Searches Google"""
    await client.say('https://encrypted.google.com/search?hl=en&q={}'.format(" ".join(args).replace(' ', '+')))

# LMGTFY
@client.command(pass_context=True)
async def lmgtfy(ctx, *args):
    """'Let me Google that for you.'"""
    await client.say('http://lmgtfy.com/?q={}'.format("+".join(args)))


# DuckDuckGo
@client.command(pass_context=True)
async def ddg(ctx,*args):
    """Searches DuckDuckGo"""
    await client.say('https://duckduckgo.com/html?q={}&atb=v40-2a_'.format("+".join(args)))

# Reddit
@client.command(pass_context=True)
async def r(ctx, arg):
    """Link a subreddit - Ex: '!r unixporn'"""
    await client.say("https://reddit.com/r/" + arg)

##################### END WEBSITE SEARCHERS #############################


################################### MEMES #######################################
# CRISPY
@client.command(pass_context=True)
async def crispy(ctx):
    """memes"""

    i = random.randint(0, 6)
    filename = ""
    if i == 0: filename = "res/when-are-soft.jpg"
    elif i == 1: filename = "res/pokemon.jpg"
    elif i == 2: filename = "res/this-is-where.jpg"
    elif i == 3: filename = "res/so-asked-me.gif"
    elif i == 4: filename = "res/varg-flakes.jpg"
    elif i == 5: filename = "res/varg-flakes2.png"
    elif i == 6: filename = "res/cornflakes.gif"

    await client.send_file(ctx.message.channel, filename)


# ITS HAPPENING!
@client.command(pass_context=True)
async def itshappening(ctx):
    """ron paul"""
    await client.say('https://i.imgur.com/7drHiqr.gif')

# RANDOM CAT
@client.command(pass_context=True)
async def cat(ctx):
    """Grabs a random cat picture"""
    r = requests.get("https://random.cat/meow")
    r = str(r.content)
    r = r.replace("b'","")
    r = r.replace("'","")
    r = r.replace("\\","")
    url = json.loads(r)["file"]
    await client.say(url)

# RANDOM DOG
@client.command(pass_context=True)
async def dog(ctx):
    """Because dogs are cute too"""
    r = requests.get("https://random.dog/woof")
    r = str(r.content)
    r = r.replace("b'","")
    r = r.replace("'","")
    await client.say("https://random.dog/" + r)

# RANDOM CAGE
@client.command(pass_context=True)
async def cage(ctx):
    """THE ONE TRUE GOD"""
    num = random.randint(0,13)
    if num < 10: num = "0" + str(num)
    url = "http://randomcage.xyz/img/cage" + str(num) + ".jpg"
    await client.say(url)

# COIN FLIP
@client.command(pass_context=True)
async def coinflip(ctx):
    """Flips a coin."""
    if random.randint(0, 1): await client.say('Heads')
    else: await client.say('Tails')

# YEE
# @client.command(pass_context=True)
# async def Yee(ctx):
#     await client.say('https://www.youtube.com/watch?v=q6EoRBvdVPQ')

# Hard-coded Babooshka
# @client.command(pass_context=True)
# async def babooshka(ctx):
#     await client.say('https://www.youtube.com/watch?v=6xckBwPdo1c')

# Hard-coded Where there's a whip, there's a way
# @client.command(pass_context=True)
# async def whip(ctx):
#     await client.say('https://www.youtube.com/watch?v=YdXQJS3Yv0Y')

# Hard-coded Moomin Theme Song
# @client.command(pass_context=True)
# async def moomin(ctx):
#     await client.say('https://www.youtube.com/watch?v=oiZ0eBFTH6k')

# YouTube in Voice-Chat
# @client.command(pass_context=True)
# async def ytvc(ctx, *args):
#     """Plays youtube video in voice-chat"""
#     query = urllib.parse.quote(" ".join(args).lower())

#     url = "https://www.youtube.com/results?search_query=" + query
#     html = urllib.request.urlopen(url).read()
#     soup = BeautifulSoup(html, "html5lib")
#     LINK_URL=""
#     for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}, limit = 1):
#         if "user" not in vid["href"] and "googleads" not in vid["href"]:
#             LINK_URL='https://www.youtube.com' + vid['href']
#             break

#     vc = await client.join_voice_channel(ctx.message.author.voice_channel)
#     player = await vc.create_ytdl_player(LINK_URL)
#     player.start

@client.command(pass_context=True)
async def links(ctx):
    """uploads links log"""
    try:
        await client.send_file(ctx.message.channel, music_links_log)
    except:
        pass

# PING
@client.command(pass_context=True)
async def ping(ctx):
    """pings bot"""
    msg = await client.say('pong')
    await asyncio.sleep(5)
    await client.delete_message(msg)
# PING
@client.command(pass_context=True)
async def p(ctx):
    """pings bot"""
    msg = await client.say('pong')
    await asyncio.sleep(5)
    await client.delete_message(msg)


# PONG... lulz
@client.command(pass_context=True)
async def pong(ctx):
    msg = await client.say('Hey, stop that.')
    await asyncio.sleep(5)
    await client.delete_message(msg)

# RULES
@client.command(pass_context=True)
async def rules(ctx):
    """displays server rules"""
    await client.say("Rule #1: Don't be a dick. \n" + \
                     "Rule #2: See rule #1")
#echo
@client.command(pass_context = True)
async def echo(ctx, *args):
    """(admin) - Ex: '!echo foo' or '!echo channel_name bar'"""
    await admin_echo(ctx, client, diskvlt, args)

# Message
@client.command(pass_context = True)
async def message(ctx, *args):
   await admin_message(ctx, client, args)

# Purge
@client.command(pass_context = True)
async def purge(ctx, *args):
    """(admin) - Ex: '!purge channel user limit'"""
    await admin_purge(ctx, client, diskvlt, args)

# Debug
@client.command(pass_context = True)
async def debug(ctx):
    """(admin) - makes me say goofy stuff"""
    await toggle_debug(ctx, client)

# RESTART
@client.command(pass_context=True)
async def restart(ctx):
    """(admin) - git pulls from varg's repo and restarts his brain"""
    await admin_restart(ctx, client)

@client.event
async def on_message(message):

    wraith = False
    if "wraith" in message.author.name.lower() or \
        "wraith" in message.author.display_name.lower():
        wraith = True
            
    msg = message.clean_content
    msg = msg.replace("'", "")
    msg = msg.replace('"', "")
    msg = msg.replace("`", "")
    msg = msg.replace("$(", "")
    msg = msg.replace("rm", "")

    if wraith:
        system("echo " + msg + " >> ~/wraith_log.txt")

    if message.channel.type != discord.ChannelType.private:
        if 'http://youtube.' in message.clean_content or \
           'https://youtube.' in message.clean_content or \
           'www.youtube.' in message.clean_content or \
           'http://bandcamp.com/' in message.clean_content or \
           'https://bandcamp.com/' in message.clean_content or \
           'www.bandcamp.com/' in message.clean_content:
            if message.channel.name == "black_metal" or \
               message.channel.name == "death_metal" or \
               message.channel.name == "doom_drone_sluge" or \
               message.channel.name == "heavy_power_speed_trad" or \
               message.channel.name == "thrash_crossover" or \
               message.channel.name == "prog_avantgarde_djent_symph" or \
               message.channel.name == "punk_grind_core_slam" or \
               message.channel.name == "dungeon_synth":
                system('echo "' + msg + '" >> ' + music_links_log)

    # if someone pm's varg, relay the content to me
    if message.channel.type == discord.ChannelType.private \
       and message.author != client.user \
       and message.author.name != "mitch" \
       and message.author.name != "Botty McBotFace":
        for user in client.get_all_members():
            try:
                if user.name == "mitch":
                    await client.send_message(user, message.author.mention \
                        + "\n" + message.clean_content)
                    return
            except:
                continue

    # if this is a file with no text, do nothing
    try:
        if len(message.clean_content) == 0: return
    except:
        return

    if message.clean_content[0] == "!":
         await client.send_typing(message.channel)

    # check if user is allowed to use commands
    try:
        if await is_banned(message.author.display_name) or \
                await is_banned(message.author.name):
            return
        else:
            await client.process_commands(message)
    except:
        if await is_banned(message.author.name):
            return
        else:
            await client.process_commands(message)

    await check_hate_speech(diskvlt, message, client)

    text = message.clean_content.lower()

    cmd = text.split(" ")[0]
    if cmd == ".fm" or cmd == ".fmyt" or cmd == "!fm" or cmd == "!fmyt":
        await client.send_message(message.channel, message.author.mention + \
                " Who do you think I am, UB3RB0T?")

    elif cmd[0] == "." and ("trans" in cmd or 'yt' in cmd or 'bc' in cmd or \
        'metal' in cmd or 'ddg' in cmd or 'google' in cmd or 'lyric' in \
        cmd or 'wiki' in cmd or 'members' in cmd or 'rules' in cmd):
        await client.send_message(message.channel, message.author.mention \
                                  + " Wrong prefix, dummy.")

    elif "goodnight" in text or "good night" in text \
            or "going to sleep" in text:
        await client.add_reaction(message, "👋")

    elif "good morning" in text or "hello everyone" in text or \
            "good evening" in text or "sup fuckers" in text:
        if random.randint(0,1) == 0:
            await client.add_reaction(message, wavefenriz)
        else:
            await client.add_reaction(message, wavedog)


    elif "emoji" in text and "movie" in text:
        await client.add_reaction(message, banned)

    like_detection = [
        "rock", "i like", "i love", "is good", "is great", "is awesome", \
        "is the best", "is amazing", "is fantastic", "are great", "are good", \
        "are the best", "are amazing", "are fantastic", "are awesome", \
        "i fucking love", "the great", "is war metal", "is black metal" , \
        "my favorite", "my personal favorite", "!yt sabaton"
    ]

    sucks_detection = [
        "sucks", "blows", "is shit", "is bad", "garbage", "is garbage", "equals bad", \
        "are posers", "is for posers", "is for hipsters", "is trash", \
        "is terrible", "is boring", "are dull", "are boring", "are shit", \
        "are bad", "are garbage", "are trash", "are terrible", \
        "i fucking hate", "is fucking garbage", "is fucking trash", "is stupid", \
        "uninteresting"

    ]

    i_like_list = [
        "whitechapel", "slipknot", "babymetal", "baby metal", "sabaton", \
        "deathcore", "metalcore", "prog metal", "prog", "progmetal", \
        "sunbather", "svnbather", "soggy cereal", "hawaiian pizza"
    ]

    i_dont_like_list = [
        "summmoning", "beverast", "burzum", "black metal", "death metal",
        "wolves in throne room", "nargaroth", "french bm", "atmoblack", \
        "atmosphblack", "atmosph black", "panopticon", "filosofem", "drudkh", \
        "manowar", "2nd wave sucks", "usbm sucks", "2nd wave black metal", \
        "2nd wave bm", "cascadian", "wolves in the throne room", "wittr", \
        "crispy cereal", "crispy cornflakes", "3rd wave", "linux sucks", \
        "ds sucks", "dungeon synth", "summoning", "war metal"
    ]

    singular_ban_list = [
        "baby metal", "babymetal", "baby_metal", "slipknot", "sunbather", \
        "svnbather", "atmoshit"
    ]

    for string in like_detection:
        if string in text:
            for word in i_like_list:
                    if word in text:
                        await client.add_reaction(message, banned)
                        return

    for string in sucks_detection:
        if string in text:
            for word in i_dont_like_list:
                if word in text:
                    await client.add_reaction(message, banned)
                    return

    for string in singular_ban_list:
        if string in text:
            await client.add_reaction(message, banned)
            return

    if "MANOWAR" in message.clean_content:
        await client.add_reaction(message, "🇲")
        await client.add_reaction(message, "🇦")
        await client.add_reaction(message, "🇳")
        await client.add_reaction(message, "🇴")
        await client.add_reaction(message, "🇼")
        await client.add_reaction(message, "🅰")
        await client.add_reaction(message, "🇷")

    elif "amon amarth" in text:
        if "war metal" in text or "viking metal" in text:
            await client.add_reaction(message, banned)

    elif "sabaton" in text and "war metal" in text:
        if "not" not in text:
            await client.add_reaction(message, banned)

    elif "agalloch" in text and "is not" in text and "metal" in text:
        await client.add_reaction(message, banned)

    elif "lamp" in text or "lampening" in text or "lamped" in text \
            or ("let" in text and "find" in text and "out" in text):
        await client.add_reaction(message, varglaugh)

    elif "varg" in text and ("best" in text or "much better" in text or
            "i love" in text or "adorable" in text):
        await client.add_reaction(message, blush_varg)

    elif "bugs" in text and not "katebugs" in text:
        await client.add_reaction(message, "🐛")

    elif "23 times" in text:
        await client.add_reaction(message, varg)

    elif "shut the fuck up" in text or "fuck you" in text:
        await client.add_reaction(message, salt)

    elif "shut up varg" in text or "stfu varg" in text or "shutup varg" \
            in text or ("varg" in text and "sucks" in text) or \
            ("varg is" in text and ("dumb" in text or "stupid" in text)):
        await client.add_reaction(message, vargdisapproves)

    elif "ah!" in text:
        await client.add_reaction(message, ah)

    elif "reeeee" in text:
        await client.add_reaction(message, bornagain)

    elif text.count("devin") >= 9:
        await client.send_message(message.channel, "*It's over nine Townsend!*")

    elif "gumby" in text:
        await client.add_reaction(message, "😱")
        await client.add_reaction(message, banned)

    # because some people shill their bands non stop
    # for name in allowed_users:
        # if message.author.name.lower() == name.lower():
            # return

    # if "my band" in text or "my project" in text \
    # or "project of mine" in text or "my merch" in text \
    # or "my bandcamp" in text:
    #     await client.add_reaction(message, "🇸")
    #     await client.add_reaction(message, "🇹")
    #     await client.add_reaction(message, "🇫")
    #     await client.add_reaction(message, "🇺")

@client.command()
async def bookmark(ctx):
    """Varg will pm you any message reacted with the :bookmark: emoji!"""
    pass

@client.command()
async def pin(ctx):
    """Varg will send any message reacted with :pushpin: to #pin_board!"""
    pass

client.run(sys.argv[1])
