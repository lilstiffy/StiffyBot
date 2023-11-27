import discord
from discord import *
from discord.ext import commands
import datetime

# Returns a user instance of Grogge or 
def getRogge(ctx):
    members = ctx.guild.members
    grogge = None
    for member in members:
        if member.name == 'GroggE':
            grogge = member

    return grogge
     
class CommandHandler(): 
    def __init__(self, client):
        self.client = client

    async def m_test(ctx):
        await ctx.send("Testing")
    
    async def m_send_message(ctx, arg):
        guild = ctx.guild
        channel_name = 'allmänt'
        channel = discord.utils.get(guild.channels, name=channel_name)

        if channel:
            # Send a message to the channel
            await channel.send(arg)
        else:
            print(f"Channel with name {channel_name} not found.")

    async def m_quiet_rogge(ctx, arg):
            rogge = getRogge(ctx=ctx)
            if rogge == None:
                pass
            else:
                await rogge.timeout(until=datetime.timedelta(seconds=60), reason='Being GroggE')

