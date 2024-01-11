from structs import discord, websocket
import asyncio

__TOKEN = "<TOKEN>"

asyncio.get_event_loop().create_task(discord.client.start(__TOKEN))
websocket.init()
asyncio.get_event_loop().run_forever()
