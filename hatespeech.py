from emojis import *

# hate speech checks to wake up the mods... /pol/ trolls...
async def check_hate_speech(diskvlt, message, client):
    try:
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
        except:
            pass

        for word in words:
            if word in message.clean_content.lower():
                nick = ""

                try:
                    nick = message.author.mention
                    if "invalid user" in nick.lower():
                        raise Failed
                except:
                    nick = message.author.name

                for channel in diskvlt.channels:
                    if channel.name == "admin_chat":
                        await client.send_message(channel, \
                                "Report: " + nick + ' - "' \
                                + message.clean_content + '"' \
                                + " - in channel [#" + message.channel.name + "]")
                        break
                await client.say(vargdisapproves)
                await client.add_reaction(message, banned)
                return True
        return False
    except:
        pass
