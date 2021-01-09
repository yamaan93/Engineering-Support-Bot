import discord
from discord.ext import commands
import random
import pandas as pd
import os



intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '%', intents = intents)





    
    
    





@client.event
async def on_member_join(member):
    print(f'{member} has joined a server' )

@client.event
async def on_member_remove(member):
    print(f'{member} has left')

@client.command()
async def load (ctx, extention):
    client.load_extension(f'cogs.{extention}')
    await ctx.send(f'{extention} was loaded')

@client.command()
async def unload (ctx, extention):
    client.unload_extension(f'cogs.{extention}')
    await ctx.send(f'{extention} was unloaded')
    
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def reloadCogs(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
    print('cogs reloaded!')
    await ctx.send('Cogs Reloaded!')
            


    

Token = open("botkey.txt","r") #haha security, yall thought you could steal my bot key XD

client.run(Token.read())

