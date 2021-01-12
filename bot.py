import discord
import os
import redis

client = discord.Client() 
token = os.getenv("DISCORD_BOT_TOKEN")
r = redis.from_url(os.environ.get("REDIS_URL"))

r.set('foo', 'bar')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$plot'):
        msg = r.get('foo')
        await message.channel.send(msg)
        return

    # if message.content.startswith('$skrap'):
    #     newMsg = rr(message.content)
    #     await message.channel.send(newMsg)
    #     return

async def run(originalMessage):
    print('')



client.run(token) 