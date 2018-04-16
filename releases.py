from bs4 import BeautifulSoup
import requests
import urllib
import re
import globals
import asyncio

class Line():
    type = ""
    title = ""
    year = ""

    def __init__(self, title, year, type):
        self.type = type
        self.title = title
        self.year = year

    def concat(self):
        line = self.title + " - " + self.year + " - (" \
              + self.type + ")"

        return(line.strip())

async def error_message(client):
        msg = await client.say("Error: I can't find it?")
        await asyncio.sleep(10)
        await client.delete_message(msg)

async def get_releases(ctx, client, args):
    try:
        ID = ""
        url = ("https://www.metal-archives.com/bands/" + "_".join(args)).lower()


        if globals.debug: await client.say("Trying to download: " + url)

        html = urllib.request.urlopen(url).read()

        if globals.debug: await client.say("Page downloaded.")

        soup = BeautifulSoup(html, "html5lib")

        match = re.search(r'\bbandId\b.*', soup.get_text())

        if match is not None:
            tmp = match.group(0).split(" = ")
            tmp = tmp[1][:-1]
            ID = tmp
        else: await error_message(client)



        if globals.debug: await client.say("The band ID is: " + match.group(0).split(" = ")[1][:-1])


        url = "https://www.metal-archives.com/band/discography/id/" \
                + ID + "/tab/all"

        if globals.debug: await client.say("Attempting to scrape page: " + url)

        html = urllib.request.urlopen(url).read()

        if globals.debug: await client.say("HTML scraped --- Attempting to parse text")

        soup = BeautifulSoup(html, "html5lib")
        text = soup.get_text()

        if globals.debug: await client.say("Text parsed! Formatting...")

        raw_lines = (line.strip() for line in text.splitlines())


        lines = []
        # get rid of ratings in lines
        for line in raw_lines:
            if "%" not in line:
                lines.append(line)


        # temps
        title = ""
        year = ""
        type = ""

        formatted_lines = []

        for line in lines:
            # skip whitespace / garble
            if len(line) < 2: continue

            # check if year
            match = re.match(r'.*[1-3][0-9]{3}', line)
            if match is not None:
                year = match.group(0)

            # get type
            elif line == "Compilation": type = line
            # elif line == "Single": type = line
            elif line == "Full-length": type = line
            elif line == "EP": type = line
            elif line == "Demo": type = line
            # elif line == "Boxed set": type = line

            # else this must be our title
            else: title = line

            if title != "" and year != "" and type != "":
                formatted_lines.append(Line(title, year, type))
                title = year = type = ""

        if globals.debug: await client.say("Text formatted! Preparing to print...")

        buffers = []
        buffer = ""
        count = 0
        for line in formatted_lines:
            count += 1
            if len(buffer) == 0: buffer = "```"
            buffer = buffer + line.concat() + "\n"

            if len(buffer) > (1996 - len(buffer)) or count == len(formatted_lines):
                buffer = buffer + "```"
                buffers.append(buffer)
                buffer = ""


        msgs = []
        for buffer in buffers:
            try:
                msg = await client.send_message(ctx.message.channel, buffer)
                msgs.append(msg)
            except:
                await client.say("Error: Couldn't print result. Blame mitch")


        try:
            if globals.debug: await client.say("Starting deletion timer...")
            await asyncio.sleep(140)
            count = 0
            for msg in msgs:
                count += 1
                if globals.debug: await client.say("Deleting message #" + str(count))
                await client.delete_message(msg)
        except:
            await client.say("Error: couldn't delete messages. Pls no spam...")
    except:
        await error_message(client)



