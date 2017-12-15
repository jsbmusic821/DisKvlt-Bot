from datetime import datetime
import requests

async def on_bookmark(reaction, user, client):
    print("Reaction was bookmark!")

    # date stamp
    date = datetime.now().strftime('%a %d %b %y')

    # if has attachments, it is an uploaded picture
    try: 
        json = str(reaction.message.attachments[0])
        json = json.split("'")
        
        file = open('/tmp/image2.png', 'wb')
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
        
        try: await client.send_file(user, "/tmp/image2.png", content=text)
        except: pass
    
    except:
        # otherwise it is just text/link
        await client.send_message(user, "From " \
            + reaction.message.author.mention + 
            "  -  " + date + "\n" + "```" \
            + reaction.message.clean_content + "```")

