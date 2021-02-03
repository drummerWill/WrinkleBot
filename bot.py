import discord
import os
import redis
from discord.ext import commands, tasks
from yahoo_fin import stock_info as si 
import asyncio
import math
import random
from datetime import date
import datetime

intents = discord.Intents.default()
intents.members = True
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
        msg = "*da_bank (shows Goon Buck leaderboard) \n"
        msg = msg + "*balance (show your balance) \n"
        msg = msg + "*gamble <amount> (gamble the amount in bucks) \n"
        msg = msg + "*pay <@User> <amount> \n"
        msg = msg + "*positions (show your stock positions) \n"
        msg = msg + "*buy <stock> <amount> (buy amount in bucks) \n"
        msg = msg + "*sell <stock> <amount> (sell amount in shares) \n"
        msg = msg + "*stonk <stock> (see stock price) \n"
        msg = msg + "*daily  (get daily login bonus) \n"

        

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
                if (data['GoonBucks'] < dollarAmount):
                    await message.channel.send('Not Enough Money')
                    return
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
            

    if message.content.startswith('*sell'):
        stonk = str(message.content.split()[1])
        sellshares = float(message.content.split()[2])
        if sellshares < 0:
            return
        price = si.get_live_price(stonk)
        if math.isnan(price):
            return
        returnamount = sellshares*price
        if math.isnan(returnamount):
            return
        if (r.exists(message.author.name)):
            data = eval(r.get(message.author.name).decode("utf-8"))            
            if('Positions' in data.keys()):
                if (next((item for item in data['Positions'] if item["stock"] == stonk), None)):
                        i = next((i for i, item in enumerate(data['Positions']) if item["stock"] == stonk))
                        currentPosition = data['Positions'][i]
                        if (currentPosition['shares'] < sellshares):
                            await message.channel.send('You cant sell that many shares.')
                            return
                        currentPosition['shares'] = currentPosition['shares'] - sellshares
                        data['GoonBucks'] = data['GoonBucks'] + returnamount
                        if (currentPosition['shares'] < .0000000000001):
                            data['Positions'].pop(i)
                        else:
                            data['Positions'][i] = currentPosition
                        r.set(message.author.name, str(data))
                        await message.channel.send(message.author.name + ' sold ' + str(sellshares) + ' shares of ' + stonk + '.')



    if message.content.startswith('*positions'):    
        if (r.exists(message.author.name)):
            msg = ""
            data = eval(r.get(message.author.name).decode("utf-8"))
            if('Positions' in data.keys()):
                for position in data['Positions']:
                    msg = msg + position['stock'] + ': ' + str(position['shares']) + ' shares.' + '\n'
                await message.channel.send(msg)
        return

    if message.content.startswith('*casino'):    
        casino = eval(r.get('casino').decode("utf-8"))
        await message.channel.send("The casino is up a total of <:goonbuck:806019179567251516>" + str(casino))
        return

    if message.content.startswith('*gamble'):
        amount = float(message.content.split()[1]) 
        if amount < 0:
            return
        if (r.exists('casino') == False):
            r.set('casino', str(0)) 
        if (r.exists(message.author.name)):
            data = eval(r.get(message.author.name).decode("utf-8"))
            casino = eval(r.get('casino').decode("utf-8"))
            if('GoonBucks' in data.keys()):
                if data['GoonBucks'] < amount:
                    return
                won = bool(random.getrandbits(1))
                if won:
                    data['GoonBucks'] = data['GoonBucks'] + amount
                    casino = casino - amount
                    await message.channel.send('You Won <:goonbuck:806019179567251516>' + str(amount) + '!!!')

                else:
                    data['GoonBucks'] = data['GoonBucks'] - amount
                    casino = casino + amount
                    await message.channel.send('You Lost <:goonbuck:806019179567251516>' + str(amount) + '...')
                r.set(message.author.name, str(data))
                r.set('casino', str(casino))   
        return

    if message.content.startswith('*daily'):
        if (r.exists(message.author.name)):
            data = eval(r.get(message.author.name).decode("utf-8"))
            if('GoonBucks' in data.keys()):
                if ('LastDaily' in data.keys()):
                    last = data['LastDaily']
                    today = date.today()
                    if (last == today):
                        await message.channel.send('Already Claimed.')
                        return 
                    
                data['LastDaily'] = date.today()
                data['GoonBucks'] = data['GoonBucks'] + 10

                await message.channel.send('Collected Daily Login!')
                r.set(message.author.name, str(data))
                

                
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
                                data['GoonBucks'] = float(data['GoonBucks']) + calculateWage(member)
                            else:
                                data['GoonBucks'] = 20
                        r.set(member.name, str(data))
            print('Looped')
            await asyncio.sleep(30)    

def calculateWage(member):
    wage = .1
    if (member.name == 'Gach'):
        wage = .12
    if (member.voice.self_stream == True):
        wage = wage + .02
    if (member.voice.self_video == True):
        wage = wage + .02
    if (member.is_on_mobile()):
        wage = .05
    
    return wage




client.loop.create_task(Foo())
client.run(token) 