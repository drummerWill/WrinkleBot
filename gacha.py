import random


gachas = {}
# gachas['1a'] =  {'name': 'William', 'link': 'kdfjgddfgjkkjdfg'}
# gachas['2a'] =  {'name': 'Dean', 'link': 'dfgkjh345dfgkjh'}
gachas['3a'] =  {'name': 'Andrew', 'link': 'dfgkjh345dfgkjh', 'image': 'https://imgur.com/a/x1N18Sx.png'}

bettergachas = {}
bettergachas['1b'] = {'name': 'Andrew but better', 'link': 'dfgkjh345dfgkjh', 'image': 'https://imgur.com/a/x1N18Sx.png'}
bestgachas = {}
bettergachas['1c'] = {'name': 'Andrew but best', 'link': 'dfgkjh345dfgkjh', 'image': 'https://imgur.com/a/x1N18Sx.png'}



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


