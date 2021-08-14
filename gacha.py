import random


gachas = {}
gachas['1a'] =  {'name': 'Antman David', 'image': 'pics/3 stars/antdavid.png'}
gachas['2a'] =  {'name': 'Deep Banana Jacob', 'image': 'pics/3 stars/bananajacob.png'}
gachas['3a'] =   {'name': 'Butch Lesbian Willy', 'image': 'pics/3 stars/blwilly.png'}
gachas['4a'] =   {'name': 'Fat Free Andy', 'image': 'pics/3 stars/ffandy.png'}
gachas['5a'] =   {'name': 'French Horn Gach', 'image': 'pics/3 stars/fhorngach.png'}
gachas['6a'] =   {'name': 'Happy Hudson', 'image': 'pics/3 stars/happyhudson.png'}
gachas['7a'] =   {'name': 'MAGA Ellie', 'image': 'pics/3 stars/magaellie.png'}
gachas['8a'] =   {'name': 'OwO Pan', 'image': 'pics/3 stars/owopan.png'}
gachas['9a'] =   {'name': 'Peep Boy Dean', 'image': 'pics/3 stars/pbdean.png'}
gachas['10a'] =   {'name': 'Tactical Sean', 'image': 'pics/3 stars/tacticalsean.png'}
gachas['11a'] =   {'name': 'Medium Rare Josh', 'image': 'pics/3 stars/burntjosh.png'}
gachas['12a'] =   {'name': 'Abusive Logi', 'image': 'pics/3 stars/abulogan.png'}
gachas['13a'] =   {'name': 'Communist Jacob', 'image': 'pics/3 stars/commjacob.png'}
gachas['14a'] =   {'name': 'Communist Logan', 'image': 'pics/3 stars/commlogan.png'}
gachas['15a'] =   {'name': 'Hungry Andy', 'image': 'pics/3 stars/hungryandy.png'}
gachas['16a'] =   {'name': 'Music Man William', 'image': 'pics/3 stars/mmwill.png'}
gachas['17a'] =   {'name': 'Questionable Pirate William', 'image': 'pics/3 stars/pirwill.png'}
gachas['18a'] =   {'name': 'Great Pride William', 'image': 'pics/3 stars/pridewill.png'}
gachas['19a'] =   {'name': 'Scuffed Adrian', 'image': 'pics/3 stars/scuffedadrian.png'}
gachas['20a'] =   {'name': 'Noble Hero Andrew', 'image': 'pics/3 stars/nobleandy.png'}
gachas['21a'] =   {'name': 'Popcorn Ruler William', 'image': 'pics/3 stars/popcornwilly.png'}
gachas['22a'] =   {'name': 'Smooth Poser Andrew', 'image': 'pics/3 stars/posandy.png'}
gachas['23a'] =   {'name': 'Young Bard Dean', 'image': 'pics/3 stars/barddean.png'}
gachas['24a'] =   {'name': 'Sleepless Jared', 'image': 'pics/3 stars/sleepjared.png'}
gachas['25a'] =   {'name': 'Bubble Buddy Jared', 'image': 'pics/3 stars/bubblejared.png'}
gachas['26a'] =   {'name': 'Noir Jared', 'image': 'pics/3 stars/noirjared.png'}
gachas['27a'] =   {'name': 'Rouge Logan', 'image': 'pics/3 stars/rougelogan.png'}
gachas['28a'] =   {'name': 'Bright Night Dean', 'image': 'pics/3 stars/bndean.png'}
gachas['29a'] =   {'name': 'Grunkle Jacob', 'image': 'pics/3 stars/gjacob.png'}
gachas['30a'] =   {'name': 'Luscious Lips Zach', 'image': 'pics/3 stars/llzach.png'}



bettergachas = {}
bettergachas['1b'] = {'name': 'ACAB Adrian', 'image': 'pics/4 stars/acabadrian.png'}
bettergachas['2b'] = {'name': 'Ghost Huddy', 'image': 'pics/4 stars/ghosthuddy.png'}
bettergachas['3b'] = {'name': 'Howdy Logan', 'image': 'pics/4 stars/howdylogan.png'}
bettergachas['4b'] = {'name': 'Hype Bundy', 'image': 'pics/4 stars/hypebundy.png'}
bettergachas['5b'] = {'name': 'Nothin Personnel Pan', 'image': 'pics/4 stars/nppan.png'}
bettergachas['6b'] = {'name': 'Smexy Andy', 'image': 'pics/4 stars/smexyandy.png'}
bettergachas['7b'] = {'name': 'Anime Josh and Adrian', 'image': 'pics/4 stars/animejosh.png'}
bettergachas['8b'] = {'name': 'Communist Jared', 'image': 'pics/4 stars/commjared.png'}
bettergachas['9b'] = {'name': 'Cosplay Dean and Jared', 'image': 'pics/4 stars/cosplay.png'}
bettergachas['10b'] = {'name': 'Immovable Object Logan', 'image': 'pics/4 stars/immlogan.png'}
bettergachas['11b'] = {'name': 'Unstoppable Force David', 'image': 'pics/4 stars/undavid.png'}
bettergachas['12b'] = {'name': 'Lonely Logan', 'image': 'pics/4 stars/lonelylogan.png'}


bestgachas = {}
bestgachas['1c'] = {'name': 'Big Boss Bongos', 'image': 'pics/5 stars/bbbongos.png'}
bestgachas['2c'] = {'name': 'Ellie with Sword', 'image': 'pics/5 stars/ellie with sword.png'}
bestgachas['3c'] = {'name': 'Gpain', 'image': 'pics/5 stars/gpain.png'}
bestgachas['4c'] = {'name': 'Sad Chef Adrian', 'image': 'pics/5 stars/sadadrian.png'}



allgachas = [gachas, bettergachas, bestgachas]



def displaycount(user, userdata):
    threestars = []
    fourstars = []
    fivestars = []
     # gacha = userdata['gacha']
    # gachalist = gacha['gachalist']
    

  
    #find the correct dictionary to look for 

    gachalist= userdata['gacha']['gachalist']

    for gachaitem in gachalist:
        star = ''
        dicttosearch = {}
        if 'a' in gachaitem['id']:
            dicttosearch = gachas
            star = ':star: :star: :star:'
            gacharich = dicttosearch[gachaitem['id']]
            indivmsg = str(gachaitem['amount']) + 'x ' + gacharich['name'] + ' (' + star + ') ' + '\n'
            threestars.append(indivmsg) 
        if 'b' in gachaitem['id']:
            dicttosearch = bettergachas 
            star = ':star: :star: :star: :star:'
            gacharich = dicttosearch[gachaitem['id']]
            indivmsg = str(gachaitem['amount']) + 'x ' + gacharich['name'] + ' (' + star + ') ' + '\n'
            fourstars.append(indivmsg)
        if 'c' in gachaitem['id']:
            dicttosearch = bestgachas 
            star = ':star: :star: :star: :star: :star:'
            gacharich = dicttosearch[gachaitem['id']]
            indivmsg = str(gachaitem['amount']) + 'x ' + gacharich['name'] + ' (' + star + ') ' + '\n'
            fivestars.append(indivmsg)
    msg = ''.join(threestars) + ''.join(fourstars) + ''.join(fivestars)
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

    selectedgachalist = random.choices(allgachas, weights=(95, 4.5, .5), k=1)[0]
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
        

    ## TEMP TO NOT AFFECT DB
    # userdata['gacha']['gachalist'] = []
    # userdata['tickets'] = 0    
    print(userdata)

    return recievedGacha, userdata


