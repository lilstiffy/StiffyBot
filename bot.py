import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from events import *
from commands import *

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Initialise client & bot
intents = discord.Intents.all()
client = discord.Client(
    intents=intents
)
bot = commands.Bot(command_prefix='$', intents=intents)
eventHandler = EventHandler(client=client)
commandHandler = CommandHandler(client=client)

# -- DEFINED EVENTS --
@client.event
async def on_ready():
    print("We are successfully connected to Discord!")

@client.event
async def on_message(message):
    await eventHandler.m_on_message(message)

@client.event
async def on_member_join(member):
    await eventHandler.m_on_member_join(member)

# -- DEFINED COMMANDS --
@bot.command(name="test")
async def test(ctx):
    await commandHandler.m_test(ctx)

@bot.command(name='say')
async def send_message(ctx, arg): 
    await commandHandler.m_send_message(ctx, arg)
    
@bot.command(name='käftengrogge')
async def quiet_grogge(ctx, arg):
    await commandHandler.m_quiet_rogge(ctx, arg)

# Launch the client
client.run(TOKEN)