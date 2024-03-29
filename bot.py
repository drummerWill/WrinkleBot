import discord
import os
import redis
from discord.ext import commands, tasks
from yahoo_fin import stock_info as si 
import asyncio
import math
import re
import random
from datetime import date
import datetime
from processing import runProcessing, combineDics
from gacha import displayRoster, getStats, roll, displaycount, showImage, calculateLuck, reroll, getUnique, chunks


cache = {}

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

    if message.content.startswith('*channelemoji'):
        await run(message, "channel")
        return

    if message.content.startswith('*emoji'):
        await run(message, "personal")
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
           msgs = displaycount(message.author.name, data)
           for msg in msgs:
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
           if (message.author.name == 'Gachary' or message.author.name == 'Pancakes Baby 46'):
                return
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
            if (message.author.id != williamId):
                return
            numtick = message.content.split()[1]
            guildid = 251058760779431936
            mentions = []
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
                                mentions.append(member.mention)
                                data['tickets'] =  data['tickets'] + int(numtick)
                        r.set(member.name, str(data))
            mentionsmsg = ' '.join(mentions)
            await message.channel.send(mentionsmsg)
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
                    if (member.name != 'Gachary' and member.name != 'Pancakes Baby 46'):
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

    if message.content.startswith('*stats'):
        members = await message.guild.fetch_members(limit=150).flatten()
        res = []
        for member in members:
            if (r.exists(member.name)) and member.bot == False:
                data = eval(r.get(member.name).decode("utf-8"))
                if 'gacha' in data.keys():
                    stats = getStats(data)
                    if (member.name != 'Gachary' and member.name != 'Pancakes Baby 46'):
                        res.append({'name': member.name, 'stats' : stats})
        

        listlistids = []
        for result in res:
            listlistids.append(result['stats']['ids'])
        
        flatList = [item for sublist in listlistids for item in sublist]

        for result in res:
            result['stats']['unique'] = getUnique(result['stats'], flatList)

        sortedres = sorted(res, key = lambda i: i['stats']['total'])
        sortedres.reverse()
        msg = 'name: total goons, (3 stars | 4 stars | 5 stars) | Unique cards'+ '\n'
        for res in sortedres:
            msg += res['name'] + ': ' + str(res['stats']['total']) + ', ' + '(' + str(res['stats']['threestars']) + ' | ' + str(res['stats']['fourstars']) + ' | ' +str(res['stats']['fivestars']) +  ')'  + ' | ' + str(res['stats']['unique']) + '\n'
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

async def run(originalMessage, selection):
    emojis = originalMessage.channel.guild.emojis
    ids = []
    for emoji in emojis:
        ids.append(emoji.id)
    print(ids)
    print('RECIEVED REQUEST')
    words = re.sub("[^\w-]", " ",  originalMessage.content).split()
    channelSelct = words[1]
    #optionSelect = words[2]
    nameSelect = False
    nameForSelect = ""
    dateRange = ""
    if (len(words) == 3):
        dateOptions = ["day", "month", "year", "week"]
        thirdWord = words[2]
        if thirdWord in dateOptions:
            dateSelect = True
            dateRange = words[2]
            
 
    if selection == "personal":
        nameSelect = False
    if selection == "personal":
        nameForSelect = originalMessage.author.name
        nameSelect = True

    channels = filter((lambda c: str(c.type) == "text" and c.name == channelSelct), originalMessage.channel.guild.channels)
    channel = next(channels)
    channelDict = {}
    channelMessages = []
    print('GETTING MESSAGES')
    cachedMessages = cache.get(channel.id, [])
    if len(cachedMessages) > 0:
        channelMessages = cachedMessages
    else:
        channelMessages = await channel.history(limit=None).flatten()
        cache.update({channel.id: channelMessages})


    print('RECIEVED MESSAGES')
    toDate = getToDate(dateRange)
    print(nameForSelect)
    for message in channelMessages:
        if message.author.bot == False and message.created_at > toDate:
            userMsgs = channelDict.get(message.author.name, [])
            userMsgs.append(message)
            if nameSelect:
                if nameForSelect == message.author.name:
                    channelDict.update({message.author.name: userMsgs})
            else:
                channelDict.update({message.author.name: userMsgs})            
    print('SAVING IMAGE')
    dicts = runProcessing(channelDict, channel.name, ids)
    print(dicts)
    finaldics = combineDics(dicts)
    print(finaldics)
    items = list(finaldics.items())
    items.sort(key = lambda x: x[1])
    items.reverse()
    print(items)
    # sortedstuff = {k: v for k, v in sorted(finaldics.items(), key=lambda item: item[1])}
    # print(sortedstuff)
    msg = ""
    i = 1
    # for key, value in sortedstuff:
    #     msg += str(i) + '. ' + key + ' (' + str(value) + ')'
    #     i = i  + 1 
    msgs = []
    for pair in items:
        msgs.append(str(i) + '. ' + pair[0] + ' (' + str(pair[1]) + ') \n')
        i = i  + 1 
    finals = []
    mychunks = chunks(msgs, 30)
    for chunk in mychunks:
        finals.append(''.join(chunk))
    for final in finals:
        await originalMessage.channel.send(final)



def getToDate(selc):
    currentTime = datetime.datetime.utcnow()
    if selc == "day":
        return currentTime - datetime.timedelta(days=1)
    if selc == "month":
        return currentTime - datetime.timedelta(days=31)
    if selc == "year":
        return currentTime - datetime.timedelta(days=365)
    if selc == "week":
        return currentTime - datetime.timedelta(days=7)
    return datetime.datetime(1999, 5, 17)




client.loop.create_task(Foo())
client.run(token) 