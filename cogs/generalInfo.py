import discord
from discord.ext import commands
import pandas as pd
import functools



class generalInfo(commands.Cog):
    
    def __init__(self,client):
        self.client = client
    
    
    @commands.command()
    async def textbooks(self,ctx):
        await ctx.send('**Mandatory purchase list** \n It seems there is a *lot* of questions on what exactly you need to buy so I thought I would simplify it for you guys and put the links for all the mandatory purchases in their cheapest forms.  \n Purchase List: \n Physics code bundle: \n  ```- https://bookstore.uwo.ca/product/cebcodeid33819 ``` \nPhysics Lab Book: \n```  - https://bookstore.uwo.ca/product/88000099137```\nBusiness E-Book:\n ```-https://bookstore.uwo.ca/product/cebebookid9687792 ``` \nchemistry Pearson Mastering \n```-https://bookstore.uwo.ca/product/cebcodeid30214``` \n chemistry lab manual \n ```-https://www.vitalsource.com/en-ca/products/chemistry-1302a-b-discovering-chemical-energetics-department-of-chemistry-v9781533925688``` \n Calculus Pearson Mastering \n ```-https://bookstore.uwo.ca/product/cebcodeid23905``` \n Statics Mastering \n ```https://bookstore.uwo.ca/product/cebcodeid23237``` ')
    @commands.command()
    @commands.has_role('Leaders')   
    async def beefCounter(self,ctx):
        beef = pd.read_excel("beef.xlsx",sheet_name="Sheet1",keep_default_na=False, na_values=['\u200b'])
        print(beef["participant 1"][0])
        embed=discord.Embed(title="Beef Counter", description="track da beef")
        embed.set_thumbnail(url="https://cdn.britannica.com/68/143268-050-917048EA/Beef-loin.jpg")
        for x in range(beef["counter"].size):
            embed.add_field(name=f'Round{beef["counter"][x]}', value=f'{beef["participant 1"][x]} VS {beef["participant 2"][x]}', inline=False)
            
        await ctx.send(embed=embed)
def setup(client):
    client.add_cog(generalInfo(client))