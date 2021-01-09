import discord
from discord.ext import commands
import pandas as pd
from tabulate import tabulate
import functools



class generalInfo(commands.Cog):
    
    def __init__(self,client):
        self.client = client
    
    
    @commands.command()
    async def textbooks(self,ctx):
        await ctx.send('test')
        
def setup(client):
    client.add_cog(generalInfo(client))