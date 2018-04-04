from emojis import *
import globals
from globals import *
import asyncio

# ECHO
async def admin_echo(ctx, client, diskvlt, args):
    if ctx.message.author.name == "mitch" or \
       ctx.message.author.top_role.name.lower() == "admin":

        for channel in diskvlt.channels:
            if channel.name.lower() == args[0].lower():
                await client.send_message(channel, " ".join(args[1:]))
                return

        await client.say(" ".join(args))
    else: await client.send_file(ctx.message.channel, "res/no-power.jpg")


# RESTART
async def admin_restart(ctx, client):
    role = ""
    try:
        if ctx.message.author.top_role is not None:
            role = ctx.message.author.top_role.name.lower()
    except:
        role = "everyone"

    if role == "admin":
        await client.say("Varg has restarted. *Let's find out!*")
        exit()
    else: await client.send_file(ctx.message.channel, "res/no-power.jpg")


# MESSAGE
async def admin_message(ctx, client, args):
    """(admin) - Ex: '!message user foo'"""
    try:
        if ctx.message.author.name == "mitch" or \
        ctx.message.author.top_role.name.lower() == "admin":

            for user in client.get_all_members():
                if user.name.lower() == args[0]:
                    await client.send_message(user, " ".join(args[1:]))
                    return
        else: await client.send_file(ctx.message.channel, "res/no-power.jpg")
    except: await client.send_file(ctx.message.channel, "res/no-power.jpg")

# Debug
async def toggle_debug(ctx, client):
    try:
        if ctx.message.author.name == "mitch" or \
            ctx.message.author.top_role.name.lower() == "admin":


            if globals.debug: globals.debug = False
            else: globals.debug = True

            if globals.debug: msg = await client.say("Debugging enabled.")
            else: msg = await client.say("Debugging disabled.")
            await asyncio.sleep(10)
            await client.delete_message(msg)
        else: await client.send_file(ctx.message.channel, "res/no-power.jpg")
    except: await client.send_file(ctx.message.channel, "res/no-power.jpg")



# PURGE
async def admin_purge(ctx, client, diskvlt, args):
    role = ""

    try:
        if ctx.message.author.top_role is not None:
            role = ctx.message.author.top_role.name.lower()
    except:
        role = "everyone"

    if role == "admin" or role == "mod":
        _limit = 0
        # if no limit is provided, assume no limit
        try: _limit = int(args[2])
        except: _limit = 1000

        user = ""
        if args[1].lower() == "bot" or args[1].lower() == "varg":
            user = "botty mcbotface"
        else:
            user = args[1].lower()

        def is_user(m): 
            if args[1].lower() == 'all' or args[1] == '*':
                return True
            else:
                return m.author.name.lower() == user

        async def execute(channel):
            try:
                msg = ""
                deleted = await client.purge_from(channel, limit=_limit, check=is_user)
                if len(deleted) > 0:
                    msg = await client.send_message(channel, "Deleted **" + str(len(deleted)) \
                        + "** messages from channel: " + ctx.message.channel.name)
                    try: await asyncio.sleep(1000)
                    except: pass
                    try: await client.delete_message(msg)
                    except: pass
                else:
                    msg = await client.send_message(channel, "No messages were deleted.")
                    try: await asyncio.sleep(5)
                    except: pass
                    try: await client.delete_message(msg)
                    except: pass
            except:
                msg = await client.say("Error: Did you try to purge too" \
                                 + " too many messages? Or too old?")
                await asyncio.sleep(10)
                await client.delete_message(msg)

        if args[0].lower() == "all" or args[1] == '*':
            for c in diskvlt.channels:
                await execute(c)
        else:
            for c in diskvlt.channels:
                if c.name == args[0].lower():
                    await execute(c)

    else:
        try: await client.send_file(ctx.message.channel, "res/no-power.jpg")
        except: pass
