from datetime import datetime
from emojis import pushpin_emoji
import requests

async def on_pushpin(reaction, user, client, diskvlt):
    print("Reaction was pushpin!")

    # try:
    if reaction.message.clean_content is None:
        print("Content is none!")
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
    # This isn't working...
    # For whatever reason, the length of reactions.message.reactions
    # is always 1, no matter how many reactions there really are.
    # i = 0
    # for reaction in reaction.message.reactions:
    #     if reaction.emoji == pushpin_emoji:
    #         i += 1
    # if i > 1:
    #     print("\n \n This has already been pinned! \n \n ")
    #     return
    #
    #
    #     -  -  - Instead of the above, this is a hacky workaround - - -
    async for _message in client.logs_from(pin_board, limit=100):
        if _message.embeds is None or len(_message.embeds) == 0:
            if reaction.message.author.name.lower() in _message.clean_content.lower():
                if reaction.message.content.lower() in _message.clean_content.lower():
                    print("Already pinned!")
                    return
    #-------------------------------------------------------


    try:
        # make sure the message hasn't already been pinned
        for message in client.messages:
            if message.channel == pin_board:
                if reaction.message.clean_content.lower() \
                in message.clean_content.lower():
                    if reaction.message.author.mention \
                    in message.clean_content:
                        return
    except:
        pass

    # date stamp
    date = datetime.now().strftime('%a %d %b %y')

    try:
        # if has attachments, it is an uploaded picture
        json = str(reaction.message.attachments[0]).split("'")


        file = open('/tmp/image1.png', 'wb')
        file.write(requests.get(json[5]).content)
        file.close()

        # if the user also posted text with this message, post it
        # for some reason discord uploads have some weird 1 character long
        # text. Not sure what it is, it's not a \n or " "
        text = "From " + reaction.message.author.mention \
                + "  ~  " + date + reaction.message.clean_content
        if len(reaction.message.clean_content) > 1:
            text = "From " + reaction.message.author.mention  + "  ~  " \
                    + date + "\n" \
                    + '```' + reaction.message.clean_content + '```'

        # Post the file
        try: await client.send_file(pin_board, "/tmp/image1.png", content=text)
        except: pass
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
    # except:
        # pass


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
