import discord
import os
import redis

client = discord.Client() 
token = os.getenv("DISCORD_BOT_TOKEN")
r = redis.from_url(os.environ.get("REDISTOGO_URL"))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('*smoothlist'):
        await message.channel.send('')
        return

    if message.content.startswith('*wrinklelist'):
        await message.channel.send('')
        return

    if message.content.startswith('*smooth'):
        members = message.mentions[0]
        await message.channel.send('Gave ' + members.name + ' a smooth.')
        return

    if message.content.startswith('*wrinkle'):
        members = message.mentions[0]
        hasEntry = r.exists(members.name)
        data = {'wrinkles':0, 'smooths':0}
        if hasEntry == True:
            data = eval(r.get(members.name).decode("utf-8"))
        
        data['wrinkles'] = data['wrinkles'] + 1

        r.set(members.name, str(data))
        await message.channel.send('Gave ' + members.name + ' a wrinkle.')
        return


client.run(token) 