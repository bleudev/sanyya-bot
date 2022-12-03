class namespace: pass
def guild_emoji(name, id):
    return '<:{}:{}>'.format(name, id)

class emoji(namespace):
    beta = guild_emoji('viewsbeta', '1048515776119840808')
