import discord
import os

client = discord.Client() 
token = os.getenv("DISCORD_BOT_TOKEN")

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



client.run(token) 