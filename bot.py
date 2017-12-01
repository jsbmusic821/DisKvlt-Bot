import discord
from discord.ext import commands
from discord import Permissions
import logging
import asyncio
import random
import re
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

from banned import is_banned

client = commands.Bot(description="Hi, I'm DisKvlt's bot! Beep, bop, boop...",\
                      command_prefix='!');

# server
diskvlt = ""

#emojis
def create_emoji(_name, _id): return discord.Emoji(name=_name, id=_id, server=diskvlt)
varg = create_emoji("varg","355715543828791296")
vargdisapproves = create_emoji("vargdisapproves","355715540410695690")
varglaugh = create_emoji("varglaugh", "355715534333149184")
banned = create_emoji("banned", "345751228082421760")
fenriz = create_emoji("fenriz", "355715536149151754")
wavefenriz = create_emoji("wavefenriz", "355715539160662021")
wavedog = create_emoji("wavedog", "364142370935013378")
ah = create_emoji("ah", "366843615860883476")
bornagain = create_emoji("bornagain", "338080634646036480")
brutal = create_emoji("brutal", "355715521410498560")
dead = create_emoji("dead", "355715555774431232")
salt = create_emoji("salt", "345758525781442560")
bookmark = "\U0001f516"
pushpin = "\U0001f4cc"

@client.event
async def on_ready(): 
    global diskvlt
    for server in client.servers:
            if server.name.lower() == "diskvlt":
                diskvlt = server
    print("~~~~~~~~~~~~ bot has started... ~~~~~~~~~~~~")

       
@client.command()
async def bookmark(ctx):
    """Varg will pm you any message reacted with the :bookmark: emoji!"""
    pass

@client.command()
async def pin(ctx):
    """Varg will send any message reacted with :pushpin: to #pin_board!"""
    pass

# BOOKMARK
@client.event
async def on_reaction_add(reaction, user):
    
    try: print("\n" + "Emoji reaction added - User: " + user.name)
    except: pass

    try:
        if reaction.emoji == bookmark:
            # if has attachments, it is an uploaded picture
            try: 
                json = str(reaction.message.attachments[0])
                json = json.split("'")
                try:
                    print("Trying to bookmark file text, if exists")
                    await client.send_message(user, reaction.message.clean_content)
                except: pass
                await client.send_message(user, json[5])
            except:
                # otherwise it is just text/link
                await client.send_message(user, reaction.message.clean_content)
        
        # --------------------------------------------------------- #
        
        elif reaction.emoji == pushpin:
            # the hooligans went and made varg recursive...
            # have to add a check here to make sure its not the pin board itself
            if reaction.message.channel.name == "pin_board": 
                return

            i = 0
            for reaction in reaction.message.reactions:
                if reaction.emoji == pushpin:

                    i += 1
                    # it must have already been pinned
                    if i > 1: 
                        print("\n \n This has already been pinned! \n \n ")
                        return
            
            pin_board = ""
            for channel in diskvlt.channels:
                if channel.name == "pin_board":
                    pin_board = channel

            try: 
                # if has attachments, it is an uploaded picture
                print("Checking to see if this is a file...")
                json = str(reaction.message.attachments[0])
                json = json.split("'")
                try: 
                    print("\n" + "Trying to pin file text if exists: " + \
                        reaction.message.clean_content)

                    # make sure the message hasn't already been pinned
                    for message in client.messages:
                        if message.channel.name == "pin_board":
                            if message.clean_content == reaction.message.clean_content:
                                return
                    await client.send_message(pin_board, reaction.message.clean_content)
                except: pass
                
                # make sure the message hasn't already been pinned
                for message in client.messages:
                    if message.channel.name == "pin_board":
                        if message.clean_content == json[5]:
                            return
            
                print("\n" + "Trying to pin the file: " + json[5])
                await client.send_message(pin_board, json[5])
            except:
                print("Error: Not a file! Attemping to post as just text..")
                # otherwise it is just text/link
                
                # make sure the message hasn't already been pinned
                for message in client.messages:
                    if message.channel.name == "pin_board":
                        if message.clean_content == reaction.message.clean_content:
                            return
                await client.send_message(pin_board, reaction.message.clean_content)
    except: pass

# Remove Reaction
@client.event
async def on_reaction_remove(reaction, user):
    # delete message in #pin_board on removal of pushpin emoji
    if reaction.emoji == pushpin:
        for message in client.messages:
            if message.channel.name == "pin_board":
                if message.clean_content == reaction.message.clean_content:
                    await client.delete_message(message)
                    return
                

# Server Welcome
@client.event
async def on_member_join(member):
    i = 0
    for member in diskvlt.members: i += 1

    fmt = '**𝖂𝖊𝖑𝖈𝖔𝖒𝖊 𝖙𝖔 𝖙𝖍𝖊 𝖘𝖊𝖗𝖛𝖊𝖗 {0.mention}!**'
    await client.send_message(diskvlt, fmt.format(member, diskvlt) + "\n" + \
                "There are now **" + str(i) + "** members in the server!")
    
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

@client.command(pass_context=True)
async def image(ctx, *args):
    """Downloads the first image from google images and uploads it as a file"""
    
    # because people are idiots
    words = [
        "porn", "naked", "botfly", "bot fly", "tits", "shit", "penis", "cock", \
        "dick", "nude", "baby", "hitler"
    ]
    tmp_query = "".join(args)
    for word in words:
        if word in tmp_query:
            await client.add_reaction(ctx.message, vargdisapproves)
            break
            await client.send_message(ctx.message.channel, \
                ctx.message.author.mention + "You've been temporarily " \
                + "disabled from using commands. ")
            banned_users.append(ctx.message.author.name)
            return

    def get_soup(url,header):
        return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)), "html5lib")

    url="https://www.google.com/search?safe=active&tbm=isch&q=" + "+".join(args)
    header = {'User-Agent': 'Mozilla/5.0'} 
    image_url = [a['src'] for a in get_soup(url, header).find_all("img", \
                            {"src": re.compile("gstatic.com")}, limit=1)][0]

    file = open("/tmp/image.png", 'wb')
    file.write(urllib.request.urlopen(image_url).read())
    file.close() 
    
    await client.send_file(ctx.message.channel, "/tmp/image.png")


# JOINED
@client.command()
async def joined(member : discord.Member):
    """Datestamp of user join - Ex: '!joined mitch'"""
    await client.say('{0.name} joined in {0.joined_at}'.format(member))

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

    query = urllib.parse.quote(" ".join(args).lower())
    
    if "emoji" in query:
        return

    url = "https://www.youtube.com/results?search_query=" + query
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html5lib")
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        if "user" not in vid["href"] and "googleads" not in vid["href"]:
            await client.say('https://www.youtube.com' + vid['href'])
            break

# Discogs command
@client.command(pass_context=True)
async def discogs(ctx,*args):
    """Search Discogs.com"""
    await client.say('https://www.discogs.com/search?q=' \
                     + '{}'.format(args.replace(' ', '+')) \
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
    i = random.randint(0, 4)
    if i == 0: await client.say('https://i.imgur.com/YVfXE7W.gif')
    elif i == 1: await client.say('https://i.imgur.com/2SRtfz5.jpg')
    elif i == 2: await client.say('https://i.imgur.com/TiESUTE.jpg')
    elif i == 3: await client.say('https://i.imgur.com/V1qfPgl.jpg')
    elif i == 4: await client.say('https://i.imgur.com/PzLJRka.jpg')

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
    i = random.randint(0, 29)
    if i == 0:
        await asyncio.sleep(3)
        await client.say("MEOW.")
    elif i == 1:
        await asyncio.sleep(3)
        await client.say("I love cats.")
    elif i == 2:
        await asyncio.sleep(3)
        await client.say("*purr...*")

# RANDOM DOG
@client.command(pass_context=True)
async def dog(ctx):
    """Because dogs are cute too"""
    r = requests.get("https://random.dog/woof")
    r = str(r.content)
    r = r.replace("b'","")
    r = r.replace("'","")
    await client.say("https://random.dog/" + r)
    if random.randint(0,29) == 0:
        await client.say("cats are better...")

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
############################## END MEMES #######################################

# PING
@client.command(pass_context=True)
async def ping(ctx):
    """pings bot"""
    msg = await client.say('pong')
    await asyncio.sleep(10)
    await client.delete_message(msg)
# PONG... lulz
@client.command(pass_context=True)
async def pong(ctx):
    msg = await client.say('Hey, stop that.')
    await asyncio.sleep(10)
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

    if ctx.message.author.name == "mitch" or \
       ctx.message.author.top_role.name.lower() == "admin":
      
        for channel in diskvlt.channels:
            if channel.name.lower() == args[0].lower():
                await client.send_message(channel, " ".join(args[1:]))
                return
        
        await client.say(" ".join(args))
    else: await client.say("http://e.lvme.me/xmeh35.jpg")

# Message
@client.command(pass_context = True)
async def message(ctx, *args):
    """(admin) - Ex: '!message user foo'"""
    if ctx.message.author.name == "mitch" or \
       ctx.message.author.top_role.name.lower() == "admin":

        for user in client.get_all_members():
            if user.name.lower() == args[0] or user.nick.lower() == args[0]:
                await client.send_message(user, " ".join(args[1:]))
    else: await client.say("http://e.lvme.me/xmeh35.jpg")


# RESTART
# @client.command(pass_context=True)
# async def restart(ctx):
#     try:
#         print(ctx.message.author.top_role.name)
#         if ctx.message.author.top_role.name == "Admin":
#             message = await client.say("restarting...")
#             system("cd ~/DisKvlt-Bot && git pull --force && \
#                 python3.6 ~/DisKvlt-Bot/bot.py " + sys.argv[1] + "&")
#             sleep(3)
#             await client.delete_message(message)
#             await client.say("Varg has restarted. *Let's find out!*")
#             exit()
#         else: await client.say("http://e.lvme.me/xmeh35.jpg")
#     except: pass

# hate speech checks to wake up the mods... /pol/ trolls...
async def check_hate_speech(message):
    words = [
       "nigger", "faggot", "jews", "heil hitler", "1488", "libtard", "cuck", \
        "build the wall", "kike"
    ]
  
    try:
        role = message.author.top_role
        if role is not None:
            r_name = role.name.lower()
            if r_name == "bot" or r_name == "mod" or r_name == "admin":
                return
    except: pass
 
    for word in words:
        if word in message.clean_content.lower():
            nick = ""

            try: nick = message.author.nick
            except: nick = message.author.name

            for channel in diskvlt.channels:
                if channel.name == "admin_chat":
                    await client.send_message(channel, \
                            "Report: " + nick + ' - "' \
                            + message.clean_content + '"'\
                            " - in channel [#" + message.channel.name + "]")
                    break
            await client.add_reaction(message,vargdisapproves)
            break
            await client.add_reaction(message, banned)
            return True
    return False

@client.event
async def on_message(message):

    # if this is a file with no text, do nothing
    try: 
        if len(message.clean_content) == 0: return
    except: 
        return
   
    # check if user is allowed to use commands
    if await is_banned(message.author.name): return
    else:await client.process_commands(message)

    await check_hate_speech(message)

    text = message.clean_content.lower()

    cmd = text.split(" ")[0]
    if cmd == ".fm" or cmd == ".fmyt" or cmd == "!fm" or cmd == "!fmyt":
        await client.send_message(message.channel, message.author.mention + " Who do you think I am, UB3RB0T?")

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


    if "emoji" in text and "movie" in text:
        await client.add_reaction(message, banned)

    # these users won't get shill-checked
    allowed_users = [
        "mitch", "cyril", "stupid-frenchie", "wraithvomit", "metalhexe", \
        "vaterhexe", "fallenempire", "fallen-empire", "fallen_empire", \
        "raukolith", "arsbo", "joutsi666", "plundermaster", "thepowerglove"
    ]

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
        "i fucking hate", "is fucking garbage", "is fucking trash", "is stupid"
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
        "ds sucks", "dungeon synth", "summoning"
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
            or ("varg" in text and "bot" in text and "best" in text) or \
            ("let" in text and "find" in text and "out" in text):
        await client.add_reaction(message, varglaugh)

    elif "23 times" in text:
        await client.add_reaction(message, varg)

    elif "shut the fuck up" in text or "fuck you" in text:
        await client.add_reaction(message, salt)

    elif "shut up varg" in text or "stfu varg" in text or "shutup varg" \
            in text or ("varg" in text and "sucks" in text):
        await client.add_reaction(message, vargdisapproves)

    elif "ah!" in text:
        await client.add_reaction(message, ah)

    elif text != "brutal" and "brutal" in text:
        await client.add_reaction(message, brutal)

    elif "reee" in text:
        await client.add_reaction(message, bornagain)

    elif "kvlt af" in text:
        await client.add_reaction(message, dead)
    
    elif text.count("devin") >= 9:
        await client.send_message(message.channel, "*It's over nine Townsend!*")

    elif "gumby-urienndgmequo" in text:
        await client.add_reaction(message, "😱")
        await client.add_reaction(message, banned) 
   
    # because some people shill their bands non stop
    for name in allowed_users:
        if message.author.name.lower() == name.lower():
            return

    if "my band" in text or "my project" in text \
    or "project of mine" in text or "my merch" in text \
    or "my bandcamp" in text:
        await client.add_reaction(message, "🇸")
        await client.add_reaction(message, "🇹")
        await client.add_reaction(message, "🇫")
        await client.add_reaction(message, "🇺")




client.run(sys.argv[1])
