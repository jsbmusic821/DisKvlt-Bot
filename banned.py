from globals import banned_users

async def is_banned(name):
    for user in banned_users:
        if name == user:
            return True
    return False
