#!/usr/bin/env python3
#
# http://github.com/mitchweaver/bin
#
# get songs from a given 'band - album'
# from metal-archives.com
#

import requests
import re
import urllib
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

async def error_msg(client):
    await client.say("Error: I can't find it?")

async def find_album_url(band, album, client):
    try:
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
    except:
        await error_msg(client)

async def find_songs(url, client):
    try:
        def tag_visible(element):
            if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                return False
            if isinstance(element, Comment):
                return False
            return True

        def text_from_html(body):
            soup = BeautifulSoup(body, 'html.parser')
            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts)  
            lines = []
            for line in visible_texts:
                lines.append(line)
            return lines

        html = urllib.request.urlopen(url).read()


        songs = []
        found = False
        for line in text_from_html(html):
            if 'Complete lineup' in line:
                break
            if '(loading lyrics...)' in line or 'Show lyrics' in line or \
                    'Single-sided' in line or 'Double-sided' in line or \
                    line == '\n' or line == ' ' or line == 'instrumental' or \
                    'ompilation' in line or 'Side A' in line or 'Side B' in line:
                continue
            line = line.strip()
            if len(line) > 0:
                if found:
                    songs.append(line)
                elif 'Additional notes' in line:
                    found = True
                    continue

        # delete last item in list, (the total time)
        del songs[-1]


        count = 0
        output = []
        while count < len(songs):
            if ':' in songs[count]:
                output.append(' (')
            output.append(songs[count])
            count += 1
            if (count % 3) == 0:
                output.append(')\n')
            elif (count % 3) == 1:
                output.append(' ')

        if output is not None and len(output) > 0:
            await client.say('```' + ''.join(output) + '```')
        else:
            await error_msg(client)

    except:
        await error_msg(client)

async def get_songs(ctx, client, args):
    try:
        arr = '{}'.format(" ".join(args)).split(' - ')
        url = await find_album_url(arr[0], arr[1], client)
    except:
        await error_message(client)
        return

    await find_songs(url, client)
