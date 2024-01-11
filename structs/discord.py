import os, discord, time, numpy
import random
import json
from discord.ext import tasks, commands
from discord.ui import Select, View
from structs import handler
from discord.ext.commands import MemberConverter
from discord.utils import get
intents=discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True
converter = MemberConverter()
client = commands.Bot(command_prefix=".", intents=intents)
readyNames = []
channel = None
test = "test 123"

with open("userList.json", "r") as p:
    userList = json.load(p)
    print(userList)

async def on_register(identifier):
    global channel
    if channel != None:
        await channel.send(identifier+" just connected.")
    pass

async def on_unregister(identifier):
    global channel
    if channel != None:
        await channel.send(identifier+" closed connection with the websocket.")

@client.event
async def on_message(message):
    global channel
    user = message.author
    username = str(user)
    print(message.content)
    if message.content[0] != "!": return
    args = message.content[1:].split(" ")
    if args[0] == "ready":
        found = False
        for uid in readyNames:
            if user == uid:
                found = True
        if found == False:
            readyNames.append(user)
            await message.channel.send("You have been added to the queue.  There are now " + str(len(readyNames)) + " players in the queue. The game will start once 4 players are in the queue")
            if len(readyNames) == 4:
                numpNames = numpy.array(readyNames)
                numpy.random.shuffle(numpNames)
                ct, t = numpNames[:2], numpNames[2:]
                await message.channel.send("Queue is full. A gamelink will be sent to your dms and your match will be starting shortly")
                select = Select(placeholder="Choose a map", options = [discord.SelectOption(label="Nuke", emoji="<:nuke:983836453765267527>"), discord.SelectOption(label="Cache", emoji="<:cache:983836509188788286>"), discord.SelectOption(label="Dust 4", emoji="<:dust:983616462314950716>"), discord.SelectOption(label="Train", emoji="<:trainmap:983616667743584287>"), discord.SelectOption(label="Vertigo", emoji="<:vertigo:983616804519813170>"), discord.SelectOption(label="Inferno", emoji="<:inferno:983616571777908776>")])
                async def my_callback(interaction):
                    await interaction.response.send_message("Please join the game. The map will be set to " + select.values[0])
                    print(select.values[0])
                    if select.values[0] == "Train":
                        mapName = "de_train"
                    elif select.values[0] == "Dust 4":
                        mapName = "de_dustIV"
                    elif select.values[0] == "Vertigo":
                        mapName = "de_vertigo"
                    elif select.values[0] == "Inferno":
                        mapName = "de_inferno"
                    for v in handler.all_triggers:
                        if v[0] == "MAPn@EFY-P67524DgcG":
                            print("passing "+"trigger/"+v[0]+"/"+mapName)
                            await v[2].send("trigger/"+v[0]+"/"+mapName)
                select.callback = my_callback
                view = View()
                view.add_item(select)
                await t[random.randint(0,1)].send("You have been randomly selected as the team captain for the terrorists. Please select a map", view=view)
                for uid in readyNames:
                    if uid in ct:
                        await uid.send("Your match is ready. You have been placed on the Counter Terrorists team. The match will automatically start in 45 seconds. Please join at: https://www.roblox.com/games/301549746?privateServerLinkCode=51999550178938971881541951072304 and join the Counter Terrorist team. Faulure to do say may result in a warning or temporary ban.")
                    else:
                        await uid.send("Your match is ready. You have been placed on the Terrorists team. The match will automatically start in 45 seconds. Please join at: https://www.roblox.com/games/301549746?privateServerLinkCode=51999550178938971881541951072304 and join the Terrorist team. Faulure to do say may result in a warning or temporary ban.")
        else:
            await message.channel.send("You are already in the queue.")
    elif args[0] == "queue":
        await message.channel.send("There are currently "  + str(len(readyNames)) + " in the queue")
        embed = discord.Embed(
            title = user.name,
            description = user.name + "'s elo has been adjusted after winning a match.",
            colour = discord.Colour.blue()
        )
        embed.set_footer(text='Please open a support ticket if you think a mistake has been made in the adjustment of your elo.')
        embed.add_field(name='Elo Adjustments', value =' 150 --> 180', inline=False)
        #Use embed.set_thumbnail(url='') to add in the image representing the level of the user after elo adjusments. Gotta wait for xander to finish the images before implementing this.
        await message.channel.send(embed=embed)
    elif args[0] == "here":
        handler.channel = message.channel
        channel = message.channel
        await message.channel.send("This channel has been designated to display messages from the websocket.")
    if len(args) > 0:
        for v in handler.all_triggers:
            if v[0] == args[0]:
                print("passing "+"trigger/"+v[0]+"/"+" ".join(args[1:]))
                await v[2].send("trigger/"+v[0]+"/"+" ".join(args[1:]))
    pass

    


@client.event
async def on_ready():   
    print('Discord bot ready')
