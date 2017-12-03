# These users are banned from using commands:
banned_users = [

    "asdf"

]

async def is_banned(name):
    for user in banned_users:
        if name == user:
            return True
    return False
