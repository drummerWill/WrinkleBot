gachas = {}
gachas[1] =  {'name': 'William', 'link': 'kdfjgddfgjkkjdfg'}
gachas[2] =  {'name': 'Dean', 'link': 'dfgkjh345dfgkjh'}


def roll(user, userdata):
    gacha = userdata['gacha']
    gachalist = gacha['gachalist']
    reward = 'you did it'
    gachaid = 1
    userdata['gacha']['gachalist'].append({'amount': 1, 'id':gachaid})
    # for card in gachalist:
    #     amount = card['amount']
    #     gachaItem = gachas[card['id']]
        
    print(userdata)

    return reward, userdata


