import discord
import os
import redis
from discord.ext import commands, tasks
from yahoo_fin import stock_info as si 
import asyncio
import math

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
    

    if message.content.startswith('*help'):
        msg = ''
        await message.channel.send(msg)


    if message.content.startswith('*smooth'):
        members = message.mentions[0]
        if (message.author.id == members.id):
                return
        hasEntry = r.exists(members.name)
        
        data = {'wrinkles':0, 'smooths':0, 'GoonBucks':0}
        if hasEntry == True:
            data = eval(r.get(members.name).decode("utf-8"))
        
        data['smooths'] = data['smooths'] + 1
        data['GoonBucks'] = data['GoonBucks'] - 1

        r.set(members.name, str(data))
        await message.channel.send('Gave ' + members.name + ' a smooth. He now has ' + str(data['smooths']) + '.')
        return

   



    if message.content.startswith('*wrinkle'):
        members = message.mentions[0]
        if (message.author.id == members.id):
            await message.channel.send('You cant give yourself a wrinkle dumbass.')
            return
        hasEntry = r.exists(members.name)
        
        data = {'wrinkles':0, 'smooths':0, 'GoonBucks':0}
        if hasEntry == True:
            data = eval(r.get(members.name).decode("utf-8"))
        
        data['wrinkles'] = data['wrinkles'] + 1
        data['GoonBucks'] = data['GoonBucks'] + .5

        r.set(members.name, str(data))
        await message.channel.send('Gave ' + members.name + ' a wrinkle. He now has ' + str(data['wrinkles']) + '.')
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


    if message.content.startswith('*stonk'):
        stonk = str(message.content.split()[1])
        price = si.get_live_price(stonk)
        await message.channel.send(price)
        return

    if message.content.startswith('*buy'):
        stonk = str(message.content.split()[1])
        dollarAmount = float(message.content.split()[2])
        if dollarAmount < 0:
            return
        price = si.get_live_price(stonk)
        if math.isnan(price):
            return
        shares = dollarAmount/price
        if math.isnan(shares):
            return
        position = {'stock': stonk, 'shares': shares}
        if (r.exists(message.author.name)):
            data = eval(r.get(message.author.name).decode("utf-8"))
            if ('GoonBucks' in data.keys()):
                data['GoonBucks'] = data['GoonBucks'] - dollarAmount
            
                if('Positions' in data.keys()):
                    if (next((item for item in data['Positions'] if item["stock"] == stonk), None)):
                        i = next((i for i, item in enumerate(data['Positions']) if item["stock"] == stonk))
                        currentPosition = data['Positions'][i]
                        currentPosition['shares'] = currentPosition['shares'] + shares
                        data['Positions'][i] = currentPosition

                    else:
                        data['Positions'].append(position)
                else:
                    data['Positions'] = [position]    
            print(data)
            r.set(message.author.name, str(data))
            await message.channel.send(message.author.name + ' bought ' + str(shares) + ' shares of ' + stonk + '.')
            

    if message.content.startswith('*positions'):    
        if (r.exists(message.author.name)):
            msg = ""
            data = eval(r.get(message.author.name).decode("utf-8"))
            if('Positions' in data.keys()):
                for position in data['Positions']:
                    msg = msg + position['stock'] + ': ' + str(position['shares']) + ' shares.' + '\n'
                await message.channel.send(msg)
        return


    # if message.content.startswith('*great_reset'):
    #     members = await message.guild.fetch_members(limit=150).flatten()
    #     res = []
    #     for member in members:
    #         if (r.exists(member.name)) and member.bot == False:
    #             data = eval(r.get(member.name).decode("utf-8"))
    #             data['GoonBucks'] = 20
    #             r.set(member.name, str(data))

    #     return



    if message.content.startswith('*tax'):
        if (message.author.name == 'Nobuzerker' or message.author.name == 'Yertle' or message.author.name == 'William'):
            amount = float(message.content.split()[2])
            if (amount < 0):
                return
            members = message.mentions[0]
            hasEntry = r.exists(members.name)
        

            data = {'wrinkles':0, 'smooths':0, 'GoonBucks':20}
            if hasEntry == True:
                data = eval(r.get(members.name).decode("utf-8"))
            
            data['GoonBucks'] =data['GoonBucks'] - amount
            
        
            r.set(members.name, str(data))
            await message.channel.send('Taxed ' + members.name + ' <:goonbuck:806019179567251516> ' + str(round(amount, 2)) + '.')
            return


    if message.content.startswith('*da_bank'):
        members = await message.guild.fetch_members(limit=150).flatten()
        res = []
        for member in members:
            if (r.exists(member.name)) and member.bot == False:
                data = eval(r.get(member.name).decode("utf-8"))
                if 'GoonBucks' in data.keys():
                    res.append({'name': member.name, 'bucks' : data['GoonBucks']})
        
        sortedres = sorted(res, key = lambda i: i['bucks'])
        sortedres.reverse()
        msg = ''
        for res in sortedres:
            msg += res['name'] + ' <:goonbuck:806019179567251516> ' + str(round(res['bucks'], 2)) + '\n'
        await message.channel.send(msg)
        return



    if message.content.startswith('*balance'):
            print('Requested')
            hasEntry = r.exists(message.author.name)
            if hasEntry == True:
                data = eval(r.get(message.author.name).decode("utf-8"))
                await message.channel.send('You have <:goonbuck:806019179567251516> ' + str(round(data['GoonBucks'],2)) + '.')



    if message.content.startswith('*bailout'):
        if (message.author.name == 'Nobuzerker' or message.author.name == 'Yertle' or message.author.name == 'William'):
            amount = float(message.content.split()[2])
            if (amount < 0):
                return
            members = message.mentions[0]
            hasEntry = r.exists(members.name)
        

            data = {'wrinkles':0, 'smooths':0, 'GoonBucks':20}
            if hasEntry == True:
                data = eval(r.get(members.name).decode("utf-8"))
            
            data['GoonBucks'] =data['GoonBucks'] + amount
            
        
            r.set(members.name, str(data))
            await message.channel.send('Bailed out ' + members.name + ' <:goonbuck:806019179567251516> ' + str(round(amount, 2)) + '.')
            return


    if message.content.startswith('*pay'):
        amount = float(message.content.split()[2])
        if (amount < 0):
            return
        members = message.mentions[0]
        if (message.author.id == members.id):
                return
        hasEntry = r.exists(members.name)
        
        senderHasEntry = r.exists(message.author.name)
        if senderHasEntry == False:
            return
        senderData = eval(r.get(message.author.name).decode("utf-8"))
        if (senderData['GoonBucks'] < amount):
            await message.channel.send('You dont have enough money')
            return
        

        data = {'wrinkles':0, 'smooths':0, 'GoonBucks':20}
        if hasEntry == True:
            data = eval(r.get(members.name).decode("utf-8"))
        
        data['GoonBucks'] =data['GoonBucks'] + amount
        senderData['GoonBucks'] = senderData['GoonBucks'] - amount
        
        
        r.set(message.author.name, str(senderData))

        r.set(members.name, str(data))
        await message.channel.send('Paid ' + members.name + ' <:goonbuck:806019179567251516> ' + str(round(amount, 2)) + '.')
        return


    


async def Foo():
        await client.wait_until_ready()
        while(True):
            guildid = 251058760779431936
            guild = client.get_guild(guildid)
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
                                data['GoonBucks'] = float(data['GoonBucks']) + calculateWage(member.name)
                            else:
                                data['GoonBucks'] = 20
                        r.set(member.name, str(data))
            print('Looped')
            await asyncio.sleep(30)    

def calculateWage(name):
    if (name== "YoungBumi"):
        return .1
    return .1 




client.loop.create_task(Foo())
client.run(token) 