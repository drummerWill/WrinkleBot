import discord
import os
import redis
from discord.ext import commands, tasks, loop
import asyncio

intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
client = discord.Client(intents=intents) 
token = os.getenv("DISCORD_BOT_TOKEN")
r = redis.from_url(os.environ.get("REDISTOGO_URL"))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    

    if message.content.startswith('*wrinklelist'):
        members = await message.guild.fetch_members(limit=150).flatten()
        res = []
        for member in members:
            if (r.exists(member.name)) and member.bot == False:
                data = eval(r.get(member.name).decode("utf-8"))
                res.append({'name': member.name, 'wrinkle' : data['wrinkles']})
        
        sortedres = sorted(res, key = lambda i: i['wrinkle'])
        sortedres.reverse()
        msg = ''
        for person in sortedres:
            msg = msg + person['name'] + ': ' + str(person['wrinkle']) + '\n'
        await message.channel.send(msg)
        return

    if message.content.startswith('*smoothlist'):
        members = await message.guild.fetch_members(limit=150).flatten()
        res = []
        for member in members:
            if (r.exists(member.name)) and member.bot == False:
                data = eval(r.get(member.name).decode("utf-8"))
                res.append({'name': member.name, 'smooth' : data['smooths']})
        
        sortedres = sorted(res, key = lambda i: i['smooth'])
        sortedres.reverse()
        msg = ''
        for res in sortedres:
            msg += res['name'] + ': ' + str(res['smooth']) + '\n'
        await message.channel.send(msg)
        return

    if message.content.startswith('*smooth'):
        members = message.mentions[0]
        if (message.author.id == members.id):
                return
        hasEntry = r.exists(members.name)
        
        data = {'wrinkles':0, 'smooths':0}
        if hasEntry == True:
            data = eval(r.get(members.name).decode("utf-8"))
        
        data['smooths'] = data['smooths'] + 1

        r.set(members.name, str(data))
        await message.channel.send('Gave ' + members.name + ' a smooth. He now has ' + str(data['smooths']) + '.')
        return

    if message.content.startswith('*balance'):
            print('Requested')
            hasEntry = r.exists(message.author.name)
            if hasEntry == True:
                data = eval(r.get(message.author.name).decode("utf-8"))
                await message.channel.send('You have ' + str(data['GoonBucks'] + ' GoonBucks.'))



    if message.content.startswith('*wrinkle'):
        members = message.mentions[0]
        if (message.author.id == members.id):
            await message.channel.send('You cant give yourself a wrinkle dumbass.')
            return
        hasEntry = r.exists(members.name)
        
        data = {'wrinkles':0, 'smooths':0}
        if hasEntry == True:
            data = eval(r.get(members.name).decode("utf-8"))
        
        data['wrinkles'] = data['wrinkles'] + 1

        r.set(members.name, str(data))
        await message.channel.send('Gave ' + members.name + ' a wrinkle. He now has ' + str(data['wrinkles']) + '.')
        return


@loop(seconds=30)
async def Foo():
        await client.wait_until_ready()
        guildid = 251058760779431936
        guild = client.get_guild(guildid)
        print('Search')
        members = await guild.fetch_members(limit=150).flatten()
        goodgoons = []
        for member in members:
            if (member.voice != None and member.voice.self_mute == False and member.voice.self_deaf == False):
                goodgoons.append(member)
        for member in members:
            if ((member.voice != None) and (member.voice.self_mute == False) and (member.voice.self_deaf == False) and (member.voice.mute == False) and (member.voice.deaf == False)):
                if any(goon.voice.channel.id == member.voice.channel.id and goon.id != member.id for goon in goodgoons):
                    hasEntry = r.exists(member.name)
                    data = {'wrinkles':0, 'smooths':0, 'GoonBucks':20}
                    if hasEntry == True:
                        data = eval(r.get(member.name).decode("utf-8"))
                        if ('GoonBucks' in data.keys()):
                            data['GoonBucks'] = float(data['GoonBucks']) + .1
                        else:
                            data['GoonBucks'] = 20
                    r.set(member.name, str(data))
    

Foo.start()
client.run(token) 