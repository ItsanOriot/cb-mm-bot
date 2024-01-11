import json
all_triggers = []
ct = []
t = []
with open("userList.json", "r") as p:
    userList = json.load(p)
    print(userList)
channel = None
    
async def on_message_received(identifier, user, message):
    args = message.split("/")
    if args[0] == "trigger" and len(args) == 3:
        print("Registering trigger \""+args[1]+"\" for "+identifier)
        user[1][args[1]] = args[2]
        all_triggers.append([args[1],args[2],user[0]])
    elif args[0] == "msg" and channel != None:
        await channel.send(args[1])
    elif args[0] == "ctWin" and channel != None:
        with open("userList.json", "r") as p:
            userList = json.load(p)
        for user in ct:
            uid = user.id
            if uid not in userList:
                userList[uid] = 30
            else:
                userList[uid] += 30
            embed = discord.Embed(
            title = user.name,
            description = user.name + "'s elo has been adjusted after winning a match.",
            colour = discord.Colour.blue()
           )
            embed.set_footer(text='Please open a support ticket if you think a mistake has been made in the adjustment of your elo.')
            embed.add_field(name='Elo Adjustments', value= str(userList[uid]-30) + " --> " + str(userList[uid]), inline=False)
            #Use embed.set_thumbnail(url='') to add in the image representing the level of the user after elo adjusments. Gotta wait for xander to finish the images before implementing this.
            await channel.send(embed=embed)
        for user in t:
            uid = user.id
            if uid not in userList:
                userList[uid] = 0
            elif userList[uid] >= 30:
                userList[uid] -= 30
            else:
                userList[uid] = 0
            await channel.send(userList[uid])
        with open("userList.json", "w") as p:
            json_object = json.dumps(userList, indent = 4)  
            print(json_object) 
            print(p)
            p.write(json_object)
            

async def on_unregister(identifier, *user):
    if user:
        for trigger in all_triggers:
            if trigger[2] == user[0]:
                all_triggers.remove(trigger)
