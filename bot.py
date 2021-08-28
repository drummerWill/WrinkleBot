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
from gacha import displayRoster, roll, displaycount, showImage, calculateLuck, reroll

williamId = 87614986049814528

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents) 
token = os.getenv("DISCORD_BOT_TOKEN")
r = redis.from_url(os.environ.get("REDISTOGO_URL"))
#write some stuff
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
        msg = msg + "*biggamble <amount> (make a big gamble) \n"
        msg = msg + "*pay <@User> <amount> \n"
        msg = msg + "*positions (show your stock positions) \n"
        msg = msg + "*buy <stock> <amount> (buy amount in bucks) \n"
        msg = msg + "*sell <stock> <amount> (sell amount in shares) \n"
        msg = msg + "*stonk <stock> (see stock price) \n"
        msg = msg + "*daily  (get daily login bonus) \n"
        msg = msg + "*casino  (how much is the casino up with gambles) \n"
        

        await message.channel.send(msg)


    if message.content.startswith('*gacha'):
        msg = "*roll (roll for a goon card) \n"
        msg = msg + "*ticket  (get daily tickets) \n"
        msg = msg + "*inventory  (display your goons (text)) \n"
        msg = msg + "*roster  (display your goons (combined image)) \n"
        msg = msg + "*show <card>  (display a specific goon) \n"
        msg = msg + "*purchaseticket  (buys a ticket for 250 goonbucks) \n"
    
        await message.channel.send(msg)



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
        
        data = {'wrinkles':0, 'smooths':0, 'GoonBucks':0}
        if hasEntry == True:
            data = eval(r.get(members.name).decode("utf-8"))
        
        data['smooths'] = data['smooths'] + 1
        data['GoonBucks'] = data['GoonBucks'] - 1

        r.set(members.name, str(data))
        await message.channel.send('Gave ' + members.name + ' a smooth. They now have ' + str(data['smooths']) + '.')
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
        await message.channel.send('Gave ' + members.name + ' a wrinkle. They now have ' + str(data['wrinkles']) + '.')
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
        if amount < 1:
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


    if message.content.startswith('*biggamble'):
        amount = float(message.content.split()[1]) 
        if amount < 1:
            return
        if (r.exists('casino') == False):
            r.set('casino', str(0)) 
        if (r.exists(message.author.name)):
            data = eval(r.get(message.author.name).decode("utf-8"))
            casino = eval(r.get('casino').decode("utf-8"))
            if('GoonBucks' in data.keys()):
                if data['GoonBucks'] < amount:
                    return
                won = random.random() < .25
                if won:
                    data['GoonBucks'] = data['GoonBucks'] + 2*amount
                    casino = casino - 2*amount
                    await message.channel.send('You Won <:goonbuck:806019179567251516>' + str(2*amount) + '!!!')

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
    

    if message.content.startswith('*purchaseticket'):
        if (r.exists(message.author.name)):
            data = eval(r.get(message.author.name).decode("utf-8"))
            if('GoonBucks' in data.keys()):
                if ('tickets' in data.keys()):
                    if data['GoonBucks'] < 250:
                        return
                    if ('LastTicket' in data.keys()):
                        last = data['LastTicket']
                        today = date.today()
                        if (last == today):
                            numpurchased = data['NumPurchased'] 
                            if numpurchased > 5:
                                await message.channel.send('Already Hit Limit.')
                                return 
                            data['NumPurchased'] = numpurchased + 1
                            data['GoonBucks'] = data['GoonBucks'] - 250
                            data['tickets'] = data['tickets'] + 1
                        else:
                            data['NumPurchased'] = 1
                            data['LastTicket'] = date.today()
                            data['GoonBucks'] = data['GoonBucks'] - 250
                            data['tickets'] = data['tickets'] + 1

                    else:
                        data['LastTicket'] = date.today()
                        data['NumPurchased'] = 1
                        data['GoonBucks'] = data['GoonBucks'] - 250
                        data['tickets'] = data['tickets'] + 1

                    await message.channel.send('Bought Ticket!')
                    r.set(message.author.name, str(data))
                

                
        return




    if message.content.startswith('*gift'):
        print(message.author.id)
        if (message.author.id == williamId):
            amount = float(message.content.split()[2])
            if (amount < 0):
                return
            members = message.mentions[0]
            hasEntry = r.exists(members.name)
        

            data = {'wrinkles':0, 'smooths':0, 'GoonBucks':20}
            if hasEntry == True:
                data = eval(r.get(members.name).decode("utf-8"))
            
            data['tickets'] =data['tickets'] + int(amount)
            
        
            r.set(members.name, str(data))
            await message.channel.send('Gave ' + members.name + ' tickets: ' + str(amount) + '.')
            return


    if message.content.startswith('*day1'):
        if (r.exists(message.author.name)):
            data = eval(r.get(message.author.name).decode("utf-8"))
            if('tickets' in data.keys()):
                if ('dayone' in data.keys()):
                    await message.channel.send('Already Claimed.')
                    return 
                    
                data['dayone'] = date.today()
                data['tickets'] = data['tickets'] + 5

                await message.channel.send('Collected day 1 bonus!')
                r.set(message.author.name, str(data))
                

                
        return

    
    if message.content.startswith('*ticket'):
        if (r.exists(message.author.name)):
            data = eval(r.get(message.author.name).decode("utf-8"))
            if ('gacha' not in data.keys()):
                data['gacha'] = {'gachalist':[]}

            if ('tickets' in data.keys()):
                last = data['LastPull']
                today = date.today()
                if (last == today):
                    await message.channel.send('Already Claimed. You have ' + str(data['tickets']))
                    return 
            if ('tickets' not in data.keys()):
                data['tickets'] = 0    
            data['LastPull'] = date.today()
            data['tickets'] = data['tickets'] + 3

            await message.channel.send('Collected Daily Tickets!')
            r.set(message.author.name, str(data))
                

                
        return
    
    if message.content.startswith('*inventory'):
        if (r.exists(message.author.name)):
           data = eval(r.get(message.author.name).decode("utf-8"))
           if ('gacha' not in data.keys()):
               return
           msg = displaycount(message.author.name, data)
           await message.channel.send(msg)
        return

    if message.content.startswith('*roster'):
        if (r.exists(message.author.name)):
           data = eval(r.get(message.author.name).decode("utf-8"))
           if ('gacha' not in data.keys()):
               return
           imagepath = displayRoster(message.author.name, data)
           await message.channel.send(file=discord.File(imagepath))

        return

    if message.content.startswith('*show'):
        if (r.exists(message.author.name)):
           data = eval(r.get(message.author.name).decode("utf-8"))
           if ('gacha' not in data.keys()):
               return
           name = message.content[6:]
           imagepath = showImage(message.author.name, data, name)
           await message.channel.send(file=discord.File(imagepath))
        return

    if message.content.startswith('*reroll'):
        if (r.exists(message.author.name)):
           data = eval(r.get(message.author.name).decode("utf-8"))
           if ('gacha' not in data.keys()):
               return
           name = message.content[8:]
           worked, newdata = reroll(message.author.name, data, name)
           if worked:
                r.set(message.author.name, str(newdata))
                await message.channel.send('You traded for a ticket!')
           else:
                await message.channel.send('No.')
        return




    if message.content.startswith('*roll'):
        if (r.exists(message.author.name)):
        #    if message.author.name !='William':
        #         return 
           data = eval(r.get(message.author.name).decode("utf-8"))
           if (data['tickets'] == 0):
              await message.channel.send('Out of tickets.')
              return
           if ('gacha' not in data.keys()):
               data['gacha'] = {'gachalist':[]}
           data['tickets'] = data['tickets'] - 1
           recieved, userdata = roll(message.author.name, data)
           r.set(message.author.name, str(userdata))
           reward = message.author.name + ' got ' + recieved['name'] + '!'
           await message.channel.send(reward)
           imglink = recieved['image']
           await message.channel.send(file=discord.File(imglink))
        
        return






    if message.content.startswith('*stimmy'):
        if (r.exists(message.author.name)):
            data = eval(r.get(message.author.name).decode("utf-8"))
            if('GoonBucks' in data.keys()):
                if ('stimmy' in data.keys()):
                    await message.channel.send('Already Claimed.')
                    return 
                    
                data['stimmy'] = date.today()
                data['GoonBucks'] = data['GoonBucks'] + 1200

                await message.channel.send('Collected Stimmy!')
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
        if (message.author.id == williamId):
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


    if message.content.startswith('*promo'):
            if (message.author.id == williamId):
                return
            numtick = message.content.split()[1]
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
                            if ('tickets' in data.keys()):
                                data['tickets'] =  data['tickets'] + int(numtick)
                        r.set(member.name, str(data))
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

    if message.content.startswith('*luck'):
        members = await message.guild.fetch_members(limit=150).flatten()
        res = []
        for member in members:
            if (r.exists(member.name)) and member.bot == False:
                data = eval(r.get(member.name).decode("utf-8"))
                if 'gacha' in data.keys():
                    luck = calculateLuck(data)
                    res.append({'name': member.name, 'luck' : luck})
        
        sortedres = sorted(res, key = lambda i: i['luck'])
        sortedres.reverse()
        msg = ''
        currentNum = 1
        for res in sortedres:
            msg += str(currentNum) + '. ' + res['name'] + '\n'
            currentNum = currentNum + 1
        await message.channel.send(msg)
        return

    if message.content.startswith('*balance'):
            print('Requested')
            hasEntry = r.exists(message.author.name)
            if hasEntry == True:
                data = eval(r.get(message.author.name).decode("utf-8"))
                await message.channel.send('You have <:goonbuck:806019179567251516> ' + str(round(data['GoonBucks'],2)) + '.')



    if message.content.startswith('*bailout'):
        if (message.author.id == williamId):
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


    
#stuff

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