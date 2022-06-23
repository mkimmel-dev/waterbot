import discord
import discmessage as dmess
import json


client = discord.Client()

@client.event
async def on_ready():
    print('logged in')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content == '!status':
        await message.channel.send('should be fine')

    elif str(message.content).startswith('!') and message.content != '!status':
        await message.channel.send(dmess.parse(message))



file1 = open('key.txt', 'r')
TOKEN = file1.readline()
file1.close()

client.run(TOKEN)