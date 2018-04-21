#!/usr/bin/env python3
#
# http://github.com/mitchweaver/bin
#
# get the location of a given band from metal-archives
#

from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

async def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    lines = []
    for line in visible_texts:
        lines.append(line)
    return lines

async def parse(url, client):
    try:
        html = urllib.request.urlopen(url).read()

        location = []
        found_count = 0
        for line in await text_from_html(html):
            if len(line.strip()) < 2: continue
            if 'Country of origin:' in line:
                location.append(line)
                found_count = 1
            elif found_count > 0:
                location.append(line)
                found_count += 1
            if found_count == 4:
                break

        await client.say('```' + location[0] + ' ' + location[1] + "\n" + \
                        location[2] + ' ' + location[3] + '```')
    except:
        await client.say("Can't find it?")

async def get_location(ctx, client, args):
    await parse("https://www.metal-archives.com/bands/" + "_".join(args).lower(), client)
