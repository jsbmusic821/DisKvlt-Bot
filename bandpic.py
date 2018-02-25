from bs4 import BeautifulSoup
import requests
import urllib
import re
import asyncio

async def get_band_pic(ctx, client, args):
    try:
        url = ("https://www.metal-archives.com/bands/" + "_".join(args)).lower()

        def get_soup(url,header):
            return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)), "html5lib")

        header = {'User-Agent': 'Mozilla/5.0'}
        image_urls = [a['src'] for a in get_soup(url, header).find_all("img")]

        image = urllib.request.urlopen(image_urls[2]).read()

        file = open("/tmp/image_band_pic.png", 'wb')
        file.write(image)
        file.close()

        await client.send_file(ctx.message.channel, "/tmp/image_band_pic.png")

    except:
        await error_message(client)
