import discord
client = discord.Client() 

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$plot'):
        await run(message)
        return

    # if message.content.startswith('$skrap'):
    #     newMsg = rr(message.content)
    #     await message.channel.send(newMsg)
    #     return

async def run(originalMessage):
    print('')



client.run('Nzk4MzM3NjYzMzk2NDc4OTg3.X_zj4w.ekOiD40f6uzQt6ITrlq7wDab8CE') 