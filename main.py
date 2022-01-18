#general imports I almost always need for bots
import discord #pycord
import os #for token
import keep_alive #keep alive file
from replit import db #database
import requests #for rate limit checker
import random #random numbers
import asyncio #for asyncio functions
import json #to write to json
from discord.ext import commands #for commands
from discord.commands import SlashCommandGroup, Option, permissions #slash commands, options, permissions
from datetime import datetime, timedelta #time and ping command
import math #for math

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

guild_ids = [] #enter your guild ID's here for instant use instead of waiting for global slash registration

#api limit checker | use 'kill 1' in the shell if you get limited
r = requests.head(url="https://discord.com/api/v1")
try:
  print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
except:
  print("No rate limit")


#<-----------------------COMMANDS----------------------->
@bot.slash_command(description="Show the bot's uptime",guild_ids=guild_ids)
async def ping(ctx):
  embed = discord.Embed(color=0x00FF00, title="**Pong!**", description=f"{bot.user.name} has been online for {datetime.now()-onlineTime}!")
  await ctx.respond(embed=embed)
  
#<-----------------------EVENTS----------------------->
@bot.event
async def on_ready():
  print(f"{bot.user.name} Online.")
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your income"))
  #set onlineTime for /ping commands 
  global onlineTime
  onlineTime = datetime.now()
  #loop through guild and check them in db
  for guild in bot.guilds:
    checkGuild(guild)

  #persistance
  #bot.add_view(helpClass())
  
@bot.event
async def on_guild_join(guild):
  checkGuild(guild)

@bot.event
async def on_message(message):
  checkGuild(message.guild)
  #dump data into a .json file for easy readability
  DUMP = True
  if DUMP:
    data2 = {}
    count = 0
    for key in db.keys():
      data2[str(key)] = db[str(key)]
      count += 1

    #ensure you have a 'database.json' file created
    with open("database.json", 'w') as f:
      json.dump(str(data2), f)
  
#<-----------------------FUNCTIONS----------------------->
#used to reset the database for a guild
def resetDB(guild):
  db[str(guild.id)] = {} #this is where you set up your db format

#check if a guild is in the db
def checkGuild(guild):
  if guild != None:
    if str(guild.id) not in db:
      resetDB(guild)

#simple error message, passes ctx from commands
async def error(ctx, code):
  embed = discord.Embed(color=0xFF0000, description= f"❌ {code}")
  await ctx.respond(embed=embed, ephemeral=True)

#simple confirmation message, passes ctx from commands
async def confirm(ctx, code, eph): 
  embed = discord.Embed(color=0x00FF00, description= f"✅ {code}")
  await ctx.respond(embed=embed, ephemeral=eph)

#bot
keep_alive.keep_alive()  #keep the bot alive
bot.run(os.environ.get("TOKEN"))  #secret variable named 'TOKEN'