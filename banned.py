# These users are banned from using commands:
banned_users = [

    "asdf"

]

async def is_banned(name):
    for user in banned_users:
        if name == user:
            return True
    return False

# adds the :banned: emoji to a message
async def ban(message):
    await client.add_reaction(message, "<:banned:345751228082421760>")

