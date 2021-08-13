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



bettergachas = {}
bettergachas['1b'] = {'name': 'ACAB Adrian', 'image': 'pics/4 stars/acabadrian.png'}
bettergachas['2b'] = {'name': 'Ghost Huddy', 'image': 'pics/4 stars/ghosthuddy.png'}
bettergachas['3b'] = {'name': 'Howdy Logan', 'image': 'pics/4 stars/howdylogan.png'}
bettergachas['4b'] = {'name': 'Hype Bundy', 'image': 'pics/4 stars/hypebundy.png'}
bettergachas['5b'] = {'name': 'Nothin Personnel Pan', 'image': 'pics/4 stars/nppan.png'}
bettergachas['6b'] = {'name': 'Smexy Andy', 'image': 'pics/4 stars/smexyandy.png'}




bestgachas = {}
bestgachas['1c'] = {'name': 'Big Boss Bongos', 'image': 'pics/5 stars/bbbongos.png'}
bestgachas['2c'] = {'name': 'Ellie with Sword', 'image': 'pics/5 stars/ellie with sword.png'}
bestgachas['3c'] = {'name': 'Gpain', 'image': 'pics/5 stars/gpain.png'}
bestgachas['4c'] = {'name': 'Sad Chef Adrian', 'image': 'pics/5 stars/sadadrian.png'}



allgachas = [gachas, bettergachas, bestgachas]



def displaycount(user, userdata):
    msg = ''
     # gacha = userdata['gacha']
    # gachalist = gacha['gachalist']
    

  
    #find the correct dictionary to look for 

    gachalist= userdata['gacha']['gachalist']

    for gachaitem in gachalist:
        star = ''
        dicttosearch = {}
        if 'a' in gachaitem['id']:
            dicttosearch = gachas
            star = '3*' 
        if 'b' in gachaitem['id']:
            dicttosearch = bettergachas 
            star = '4*'
        if 'c' in gachaitem['id']:
            dicttosearch = bestgachas 
            star = '5*'
        gacharich = dicttosearch[gachaitem['id']]
        indivmsg = gacharich['name'] + ', ' + star + ', ' + str(gachaitem['amount']) + '\n'
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


