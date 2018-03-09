from datetime import datetime
from emojis import pushpin_emoji
import requests

async def on_pushpin(reaction, user, client, diskvlt):
    if reaction.message.clean_content is None:
        return

    # the hooligans went and made varg recursive...
    # have to add a check here to make sure its not the pin board itself
    if reaction.message.channel.name.lower() == "pin_board":
        return

    pin_board = ""
    for channel in diskvlt.channels:
        if channel.name.lower() == "pin_board":
            pin_board = channel
            break

    NAME = "<UNKNOWN_USER>"
    if user.nick is not None:
        NAME = user.nick
    elif user.name is not None:
        NAME = user.name

    # ----------- Prevent multiple pinnings -----------------
    if reaction.message.embeds is None or len(reaction.message.embeds) == 0:
        async for _message in client.logs_from(pin_board, limit=40):
            if len(reaction.message.clean_content) > 1:
                if reaction.message.author.name.lower() in _message.clean_content.lower():
                    if reaction.message.clean_content.lower() in _message.clean_content.lower():
                        return
    #-------------------------------------------------------

    # date stamp
    date = datetime.now().strftime('%a %d %b %y')

    try:
        # if has attachments, it is an uploaded picture
        try:
            json = str(reaction.message.attachments[0]).split("'")
        except:
            try:
                json = str(reaction.message.attachments[1]).split("'")
            except:
                json = str(reaction.message.attachments[2]).split("'")

        file = open('/tmp/image2.png', 'wb')
        try:
            image = requests.get(json[5]).content
        except:
            try:
                image = requests.get(json[4]).content
            except:
                try:
                    image = requests.get(json[3]).content
                except:
                    pass

        file.write(image)
        file.close()

        text = "From " + reaction.message.author.mention \
                + "  ~  " + date + reaction.message.clean_content
        if len(reaction.message.clean_content) > 2:
            text = "From " + reaction.message.author.mention \
                + "  ~  " + date + "\n" + '```' + \
                reaction.message.clean_content + '```'

        await client.send_file(pin_board, "/tmp/image2.png", content=text)
    except:
        # if the above failed, its only text -- no file
        try:
            if "http" not in reaction.message.clean_content.lower() \
            and "www" not in reaction.message.clean_content.lower():
                text = "From " + reaction.message.author.mention + "  ~  " \
                        + date + "\n" + \
                        '```' + reaction.message.clean_content + '```'
            else:
                text = "From " + reaction.message.author.mention  + "  ~  " \
                        + date + "\n" \
                        + reaction.message.clean_content

            await client.send_message(pin_board, text)
        except:
            pass

async def remove_pin(reaction, client):
    try:
        for message in client.messages:
            if message.channel.name.lower() == "pin_board":
                if message == reaction.message:
                    try:
                        await client.delete_message(message)
                    except:
                        pass
                    return
    except:
        pass
