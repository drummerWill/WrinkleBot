import re

def runProcessing(myDict, name, option):
       if option == "emoji":
             return countEmoji(myDict, name)


def countEmoji(channel, name):
    for user in channel.items():
        for msg in user[1]:
            emojis =  [x.group() for x in re.finditer(r'(<a?)?:\w+:(\d{18}>)', msg.content)]
            print(emojis)
    return ""