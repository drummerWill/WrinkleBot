import random


gachas = {}
gachas['1a'] =  {'name': 'William', 'link': 'kdfjgddfgjkkjdfg'}
gachas['2a'] =  {'name': 'Dean', 'link': 'dfgkjh345dfgkjh'}


def displaycount(user, userdata):
    msg = ''
     # gacha = userdata['gacha']
    # gachalist = gacha['gachalist']
    

    #find the correct dictionary to look for 

    gachalist= userdata['gacha']['gachalist']

    for gachaitem in gachalist:
        gacharich = gachas[gachaitem['id']]
        indivmsg = gacharich['name'] + ', ' + str(gachaitem['amount']) + '\n'
        msg += indivmsg
    return msg





def roll(user, userdata):

    
    # gacha = userdata['gacha']
    # gachalist = gacha['gachalist']
    

    #find the correct dictionary to look for 


    gachaid = random.choice(list(gachas.keys()))
    recievedGacha = gachas[gachaid]
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

    return reward, userdata


