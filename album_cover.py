#!/usr/bin/env python3
#
# http://github.com/mitchweaver/bin
#
# get a given album cover from metal-archives.com
#

from bs4 import BeautifulSoup

import requests
import sys
import re
import urllib

async def find_album_url(band, album):

    def get_soup(url):
        data  = requests.get(url).text
        return BeautifulSoup(data, "html5lib")

    url = 'https://www.metal-archives.com/bands/' + band.lower()
    soup = get_soup(url)

    for link in soup.find_all('a'):
        strlink = str(link)
        # scrape the band page for the discography link
        # we need to do this because MA hides it behind an ID#
        if 'iscography' in strlink and 'omplete' in strlink:
            # sed out the href garbage
            url = strlink.replace('<a href="', '').replace('"><span>Complete discography</span></a>', '')
            # scrape the album page
            for link in get_soup(url).find_all('a'):
                # sed out the reviews
                if not 'reviews' in str(link):
                    # look for the album
                    if album.lower() in str(link).lower():
                        urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/.*."', str(link))
                        return(urls[0].replace('"', ''))

async def error_message(client):
    await client.say("error: can't find it?")

async def get_album_cover(ctx, client, args):
    try:
        arr = '{}'.format(" ".join(args)).split(' - ')
        url = await find_album_url(arr[0], arr[1])
    except:
        await error_message(client)
        return
        
    try:
        def get_soup(url,header):
            return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)), "html5lib")

        header = {'User-Agent': 'Mozilla/5.0'}
        image_urls = [a['src'] for a in get_soup(url, header).find_all("img")]

        image = urllib.request.urlopen(image_urls[1]).read()

        file = open("/tmp/cover.jpg", 'wb')
        file.write(image)
        file.close()

        await client.send_file(ctx.message.channel, "/tmp/cover.jpg")

    except:
        await error_message(client)
        return
