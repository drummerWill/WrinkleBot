import random


gachas = {}
gachas['1a'] =  {'name': 'Antman David', 'image': 'pics/3 stars/antdavid.png'}
gachas['2a'] =  {'name': 'Deep Banana Jacob', 'image': 'pics/3 stars/bananajacob.png'}

bettergachas = {}
bettergachas['1b'] = {'name': 'ACAB Adrian', 'image': 'pics/4 stars/acabadrian.png'}
bestgachas = {}
bettergachas['1c'] = {'name': 'Ellie with Sword', 'image': 'pics/5 stars/ellie with sword.png'}



allgachas = [gachas, bettergachas, bestgachas]

def displaycount(user, userdata):
    msg = ''
     # gacha = userdata['gacha']
    # gachalist = gacha['gachalist']
    

  
    #find the correct dictionary to look for 

    gachalist= userdata['gacha']['gachalist']

    for gachaitem in gachalist:
        dicttosearch = {}
        if 'a' in gachaitem['id']:
            dicttosearch = gachas 
        if 'a' in gachaitem['id']:
            dicttosearch = bettergachas 
        if 'a' in gachaitem['id']:
            dicttosearch = bestgachas 
        gacharich = dicttosearch[gachaitem['id']]
        indivmsg = gacharich['name'] + ', ' + str(gachaitem['amount']) + '\n'
        msg += indivmsg
    return msg

# lowtier = 0 
# midtier = 0
# hightier = 0
# for i in range(1000000):
#     selectedgachalist = random.choices(allgachas, weights=(90, 9.5, .5), k=1)[0]
    
#     if selectedgachalist['type'] == 'lowtier':
#         lowtier += 1
#     if selectedgachalist['type'] == 'midtier':
#         midtier += 1
#     if selectedgachalist['type'] == 'hightier':
#         hightier += 1    
   

# print(lowtier)
# print(midtier)
# print(hightier)

def roll(user, userdata):

    
    # gacha = userdata['gacha']
    # gachalist = gacha['gachalist']
    

    #find the correct dictionary to look for 

    selectedgachalist = random.choices(allgachas, weights=(90, 9.5, .5), k=1)[0]
    gachaid = random.choice(list(selectedgachalist.keys()))
    recievedGacha = selectedgachalist[gachaid]
    reward = 'you got ' + recievedGacha['name']

    amount = 1
    if (next((item for item in userdata['gacha']['gachalist'] if item["id"] == gachaid), None)):
        i = next((i for i, item in enumerate(userdata['gacha']['gachalist']) if item["id"] == gachaid))
        amount = userdata['gacha']['gachalist'][i]['amount'] + 1
        userdata['gacha']['gachalist'][i] ={'amount': amount, 'id':gachaid}
    else:
        userdata['gacha']['gachalist'].append({'amount': amount, 'id':gachaid})
    # for card in gachalist:
    #     amount = card['amount']
    #     gachaItem = gachas[card['id']]
        
    print(userdata)

    return recievedGacha, userdata


