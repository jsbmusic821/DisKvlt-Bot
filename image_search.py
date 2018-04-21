from bs4 import BeautifulSoup
import urllib
import re
from emojis import *
from globals import *
import asyncio

async def search_for_image(ctx, client, args):
    # because people are idiots
    words = [
        "porn", "naked", "botfly", "bot fly", "tits", "shit", "penis", "cock", \
        "dick", "nude", "hitler"
    ]
    tmp_query = "".join(args)
    for word in words:
        if word in tmp_query:
            await client.add_reaction(ctx.message, vargdisapproves)
            await client.send_message(ctx.message.channel, \
                ctx.message.author.mention + " You've been temporarily " \
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

    wraith = False
    for role in ctx.message.author.roles:
        if role.name.lower() == "wraithvomit":
            wraith = True

    if not wraith:
        await client.send_file(ctx.message.channel, "/tmp/image.png")
    else:
        sleep_time = 20
        msg = await client.send_file(ctx.message.channel, "/tmp/image.png")
        await asyncio.sleep(sleep_time)
        await client.delete_message(msg)
