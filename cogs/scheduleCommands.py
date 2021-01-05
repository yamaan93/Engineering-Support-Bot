import discord
from discord.ext import commands
import pandas as pd
from tabulate import tabulate
import functools

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1oQDgT7eO0zSD0EBQUZ7h7DzIM-84Slw91XDT7xFmzQc'
SAMPLE_RANGE_NAME = 'A1:AA1000'

def main():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    if not values_input: # and not values_expansion:
        print('No data found.')

main()

df=pd.DataFrame(values_input[1:], columns=values_input[0])

FLOAT_COLUMNS = ('Floats',)
BOOLEAN_COLUMNS = ('Booleans',)

def left_justified(df):
    formatters = {}

    # Pass a custom pattern to format(), based on
    # type of data
    for li in list(df.columns):
        if li in FLOAT_COLUMNS:
           form = "{{!s:<5}}".format()
        elif li in BOOLEAN_COLUMNS:
            form = "{{!s:<8}}".format()
        else:
            max = df[li].str.len().max()
            form = "{{:<{}s}}".format(max)
        formatters[li] = functools.partial(str.format, form)

    return df.to_string(formatters=formatters, index=False)
def read_schedule(self):
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
    
    
    schedule = pd.read_excel("test.xlsx", sheet_name="Sheet1",keep_default_na=False, na_values=['_'])
    _business = schedule["Business"]
    _physics = schedule["Physics"]
    _calculus = schedule['Calculus']
    _statics = schedule["Statics"]
    _design = schedule["Design"]
    _chemistry = schedule["Chemistry"]
    _materials = schedule["Materials"]
    _lin_alg = schedule["Linear Algebra"]
    _programming = schedule["Programming"]
    
    print(schedule)
    
class scheduleCommands(commands.Cog):
    
    def __init__(self,client):
        self.client = client
    
    
    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is ready')
    
    
    @commands.command()
    async def weekly(self,ctx):
        read_schedule(self)
        embed=discord.Embed(title="Week 42069", color=0x9a6dbe)
        embed.add_field(name="Business:", value=f'{_business[0:9].to_string(index=False)}', inline=True)
        embed.add_field(name="Physics:", value=f'{_physics[0:9].to_string(index=False)}', inline=True)
        embed.add_field(name="Calculus:", value=f'{_calculus[0:9].to_string(index=False)}', inline=True)
        embed.add_field(name="Statics:", value=f'{_statics[0:9].to_string(index=False)}', inline=True)
        embed.add_field(name="Design:", value=f'{_design[0:9].to_string(index=False)}', inline=True)
        embed.add_field(name="Chemistry:", value=f'{_chemistry[0:9].to_string(index=False)}', inline=True)
        embed.add_field(name="Materials:", value=f'{_materials[0:9].to_string(index=False)}', inline=True)
        embed.add_field(name="Linear Algebra:", value=f'{_lin_alg[0:9].to_string(index=False)}', inline=True)
        embed.add_field(name="Programming:", value=f'{_programming[0:9].to_string(index=False)}', inline=True)
        await ctx.send(embed=embed)
        #await ctx.send(f'here is what you need to get done:\n```{schedule.to_string(index=False)}```')
        
        
    @commands.command()
    async def statics(self,ctx):
        read_schedule(self)
        embed=discord.Embed(title="", color=0x9a6dbe)
        embed.add_field(name="Here's what you got to do:", value=f'{_statics[0:9].to_string(index=False)}', inline=True)
        await ctx.send(embed=embed)
        #await ctx.send(f'here is what you need to get done:\n```{schedule.to_string(index=False)}```')
    
    @commands.command()
    async def read(self,ctx):
        read_schedule(self)
        
        
def setup(client):
    client.add_cog(scheduleCommands(client))
    
