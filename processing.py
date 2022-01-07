import re

def runProcessing(myDict, name, option, ids):
       if option == "emoji":
             return countEmoji(myDict, name, ids)


def countEmoji(channel, name, ids):
    alldics = []
    for user in channel.items():
        userdict = {}
        for msg in user[1]:
            emojis =  [x.group() for x in re.finditer(r'(<a?)?:\w+:(\d{18}>)', msg.content)]
            for emoji in emojis:
                emojiId = emoji[-19][-1]
                print(emojiId)
                if emojiId in ids:
                    if emoji in userdict:
                        userdict[emoji] =  userdict[emoji] + 1
                    else: 
                        userdict[emoji] = + 1
        alldics.append(userdict)
            
    return alldics