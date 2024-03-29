import discord
from discord.ext import commands
import pandas as pd
import functools

from googleapiclient import discovery
from google.oauth2 import service_account
import os

# TODO comment code properly
schedule = None
_business = None
_physics = None
_calculus =None 
_statics = None
_design = None
_chemistry = None
_materials = None
_lin_alg = None
_programming = None
values_input = None
service = None
current_week = None
pd.set_option("display.max_colwidth", None)
pd.set_option("display.max_seq_items", 100000)
pd.set_option("display.html.table_schema", True)

SCOPES = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/spreadsheets"
        ]

# here enter the id of your google sheet
SPREADSHEET_ID = '1oQDgT7eO0zSD0EBQUZ7h7DzIM-84Slw91XDT7xFmzQc'


def get_googleSheet(range_name):
    # Authenticate with Google
    secrets_file = os.path.join(os.getcwd(), "client_secret.json")
    credentials = service_account.Credentials.from_service_account_file(secrets_file, scopes=SCOPES)
    service = discovery.build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=range_name).execute()
    values_input = result_input.get('values', [])

    if not values_input:
        print('No data found.')
    df = pd.DataFrame(values_input[1:], columns=values_input[0])
    df.to_excel('current_schedule.xlsx')
    return df

#df= pd.DataFrame(values_input[1:], columns=values_input[0])






def read_schedule(self, week):
    global current_week
    current_week = week
    get_googleSheet(f'Week {current_week}!A1:AA1000')
    global schedule
    global _business
    global _physics
    global _calculus
    global _statics
    global _design
    global _chemistry
    global _materials
    global _lin_alg
    global _programming
    
    
    schedule = pd.read_excel("current_schedule.xlsx", sheet_name="Sheet1",keep_default_na=False, na_values=['\u200b'])
    #print(schedule)
    _business = schedule["Business"]
    _physics = schedule["Physics"]
    _calculus = schedule['Calculus']
    _statics = schedule["Statics"]
    _design = schedule["Design"]
    _chemistry = schedule["Chemistry"]
    _materials = schedule["Materials"]
    _lin_alg = schedule["Linear Algebra"]
    _programming = schedule["Programming"]
    # TODO need to redo the way messages are formatting as currently they are relying on embeds as a crutch and its not really that flexible and kinda looks ugly 
    #_programming = pd.Series(dtype="string")
    #for x in range(schedule["Programming"].size):
    #    _programming.at[x] = schedule.at[x,"Programming"].strip()
    #   print(_programming.at[x])
    
    
    #print(_programming.to_string(index = False))
    

def get_week():
    global current_week
    bruh = pd.read_excel("currentWeek.xlsx", sheet_name="Sheet1",keep_default_na=False, na_values=['_'])
    current_week = bruh.at[0,"Current week"]
    print(f'current week: {current_week}')

      
class scheduleCommands(commands.Cog):
    
    def __init__(self,client):
        get_week()
        self.client = client
    
    
    #events
    @commands.Cog.listener()
    async def on_ready(self):
        #read_schedule(self)
        print('bot is ready')
    
    
    @commands.command()
    @commands.has_role('Leaders')
    async def weekly(self,ctx, week_number):
        await ctx.channel.purge(limit =1)
        read_schedule(self, week_number)
        embed=discord.Embed(title=f'Week: {current_week}', color=0x9a6dbe)
        #embed.set_thumbnail(url="https://images.vexels.com/media/users/3/157931/isolated/preview/604a0cadf94914c7ee6c6e552e9b4487-curved-check-mark-circle-icon-by-vexels.png")
        embed.add_field(name="Business:", value=f'{_business[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name="\u200b", value=f'{_business[5:90].to_string(index=False)}', inline=False)
        embed.add_field(name="Physics:", value=f'{_physics[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_physics[5:90].to_string(index=False)}', inline=False)
        embed.add_field(name="Calculus:", value=f'{_calculus[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_calculus[5:90].to_string(index=False)}', inline=False)
        embed.add_field(name="Statics:", value=f'{_statics[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_statics[5:90].to_string(index=False)}', inline=False)
        embed.add_field(name="Design:", value=f'{_design[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_design[5:25].to_string(index=False)}', inline=False)
        embed.add_field(name="Chemistry:", value=f'{_chemistry[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_chemistry[5:90].to_string(index=False)}', inline=False)
        embed.add_field(name="Materials:", value=f'{_materials[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_materials[5:90].to_string(index=False)}', inline=False)
        embed.add_field(name="Linear Algebra:", value=f'{_lin_alg[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_lin_alg[5:90].to_string(index=False)}', inline=False)
        embed.add_field(name="Programming:", value=f'{_programming[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_programming[5:90].to_string(index=False)}', inline=False)
        await ctx.send(embed=embed)
        #await ctx.send(f'here is what you need to get done:\n```{schedule.to_string(index=False)}```')
        
    @commands.command()
    @commands.has_role('Leaders')
    async def setWeek(self,ctx,week):
        global current_week
        current_week = week  
        d =  {'Current week': [current_week]} #creating a dictionary to make into a data frame to make into an excel file so  that
        df = pd.DataFrame(data= d) #i can make it an excel file to read from so that the week will be stored even if the bot is turned off
        df.to_excel('currentWeek.xlsx')
    
    @commands.command()
    async def statics(self,ctx):
        global current_week
        if current_week ==None:
            await ctx.send('ERROR: Week not set')
        read_schedule(self,current_week)
        embed=discord.Embed(title="", color=0x9a6dbe)
        embed.add_field(name="Here's what you got to do:", value=f'{_statics[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_statics[5:90].to_string(index=False)}', inline=False)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def business(self,ctx):
        global current_week
        if current_week ==None:
            await ctx.send('ERROR: Week not set')
        read_schedule(self,current_week)
        embed=discord.Embed(title="", color=0x9a6dbe)
        embed.add_field(name="Here's what you got to do:", value=f'{_business[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_business[5:90].to_string(index=False)}', inline=False)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def physics(self,ctx):
        global current_week
        if current_week ==None:
            await ctx.send('ERROR: Week not set')
        read_schedule(self,current_week)
        embed=discord.Embed(title="", color=0x9a6dbe)
        embed.add_field(name="Here's what you got to do:", value=f'{_physics[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_physics[5:90].to_string(index=False)}', inline=False)
        await ctx.send(embed=embed)    
    @commands.command()
    async def calculus(self,ctx):
        global current_week
        if current_week ==None:
            await ctx.send('ERROR: Week not set')
        read_schedule(self,current_week)
        embed=discord.Embed(title="", color=0x9a6dbe)
        embed.add_field(name="Here's what you got to do:", value=f'{_calculus[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_calculus[5:90].to_string(index=False)}', inline=False)
        await ctx.send(embed=embed)  
    @commands.command()
    async def design(self,ctx):
        global current_week
        if current_week ==None:
            await ctx.send('ERROR: Week not set')
        read_schedule(self,current_week)
        embed=discord.Embed(title="", color=0x9a6dbe)
        embed.add_field(name="Here's what you got to do:", value=f'{_design[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_design[5:25].to_string(index=False)}', inline=False)
        #embed.add_field(name='\u200b', value=f'{_design[26:27].to_string(index=False)}', inline=False)
        
        await ctx.send(embed=embed)  
    @commands.command()
    async def chemistry(self,ctx):
        global current_week
        if current_week ==None:
            await ctx.send('ERROR: Week not set')
        read_schedule(self,current_week)
        embed=discord.Embed(title="", color=0x9a6dbe)
        embed.add_field(name="Here's what you got to do:", value=f'{_chemistry[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name="\u200b", value=f'{_chemistry[5:90].to_string(index=False)}', inline=False)
        await ctx.send(embed=embed)  
        
    @commands.command()
    async def materials(self,ctx):
        global current_week
        if current_week ==None:
            await ctx.send('ERROR: Week not set')
        read_schedule(self,current_week)
        embed=discord.Embed(title="", color=0x9a6dbe)
        embed.add_field(name="Here's what you got to do:", value=f'{_materials[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_materials[5:90].to_string(index=False)}', inline=False)
        await ctx.send(embed=embed)  
        
    @commands.command()
    async def lin(self,ctx):
        global current_week
        if current_week ==None:
            await ctx.send('ERROR: Week not set')
        read_schedule(self,current_week)
        embed=discord.Embed(title="", color=0x9a6dbe)
        embed.add_field(name="Here's what you got to do:", value=f'{_lin_alg[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_lin_alg[5:90].to_string(index=False)}', inline=False)
        await ctx.send(embed=embed)  
    @commands.command()
    async def programming(self,ctx):
        global current_week
        if current_week ==None:
            await ctx.send('ERROR: Week not set')
        read_schedule(self,current_week)
        embed=discord.Embed(title="", color=0x9a6dbe)
        embed.add_field(name="Here's what you got to do:", value=f'{_programming[0:5].to_string(index=False)}', inline=False)
        embed.add_field(name='\u200b', value=f'{_programming[5:90].to_string(index=False)}', inline=False)
        #for x in range(_programming.size):
        #    if _programming[x] != "" and _programming[x] != "NOTES:":
        #        await ctx.send(f'```{_programming[x]}```')
        #    if _programming[x] != "" and _programming[x] == "NOTES:":
        #        await ctx.send(f'{_programming[x]}')
        await ctx.send(embed=embed)  
    @commands.command()
    async def read(self,ctx):
        read_schedule(self)
        
        
def setup(client):
    client.add_cog(scheduleCommands(client))
    
