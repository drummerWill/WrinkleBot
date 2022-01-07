def runProcessing(myDict, name, option):
       if option == "emoji":
             return countEmoji(myDict, name)


def countEmoji(channel, name):
    for user in channel.items():
        for msg in user[1]:
            print(msg.content)
    return ""