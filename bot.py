import os
import discord
import random
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Initialise client & bot
intents = discord.Intents.all()

# Initialise client
client = discord.Client(
    intents=intents
)

# Initialise bot
bot = commands.Bot(command_prefix='!', intents=intents.all())


# -- DEFINED EVENTS --
@bot.event
async def on_ready():
    print("Bot up and running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced: {len(synced)} command(s)")
    except Exception as e:
        print(f"Could not sync commands: {e}")


@bot.event
async def on_slash_command_error(ctx, error):
    print(error)
    await ctx.send("Bror du använder commandsen fel")


@bot.event
async def on_member_join(member):
    await member.send(f"Välkommen till servern {member.name}!")


@bot.event
async def on_member_remove(member):
    await member.send(f"Vi ses {member.name}!")


# -- DEFINED COMMANDS --
@bot.tree.command(name="ping")
async def ping(interraction: discord.Interaction):
    """Ping the bot"""
    await interraction.response.send_message(f"{interraction.user.mention} :white_check_mark:", ephemeral=True)


@bot.tree.command(name="say")
@app_commands.describe(thing_to_say="What to say")
async def say(interraction: discord.Interaction, thing_to_say: str):
    """Make the bot say something"""
    await interraction.response.send_message(f"{interraction.user.mention} {thing_to_say}")


@bot.tree.command(name="8ball")
@app_commands.describe(fråga="Din fråga")
async def eight_ball(interraction: discord.Interaction, fråga: str):
    """Fråga magiska 8ball en fråga"""
    with open("8ball_responses.txt", "r") as f:
        eight_ball_responses = f.read().splitlines()

    embed = discord.Embed(
        description=f"{interraction.user.mention} frågade 8ball:",
        color=discord.Color.purple()
    )
    embed.set_author(name="8ball", icon_url="https://github.com/lilstiffy/StiffyBot/blob/master/8ball.png?raw=true")

    embed.add_field(name="", value=fråga, inline=False)
    embed.add_field(name="Svaret är", value=random.choice(eight_ball_responses), inline=False)

    await interraction.response.send_message(embed=embed)


@bot.tree.command(name="russian_roulette")
async def russian_roulette(interraction: discord.Interaction):
    """Spela en runda rysk roulette"""
    did_shoot = random.randint(1, 6) == 1

    embed = discord.Embed(
        title="Rysk roulette",
        description=f"{interraction.user.mention} spelade en runda rysk roulette",
        color=discord.Color.red() if did_shoot else discord.Color.green()
    )

    embed.add_field(name="Resultat", value="Sköt sig själv ☠️" if did_shoot else "Överlevde rundan 🎉")

    await interraction.response.send_message(embed=embed)


@bot.tree.command(name="balle")
async def balle(interraction: discord.Interaction):
    """Hur stor balle har du?"""
    length = random.randint(6, 25)
    if 6 <= length <= 11:
        emoji = ":worm:"
    elif 12 <= length <= 16:
        emoji = ":test_tube:"
    elif 17 <= length <= 21:
        emoji = ":snake:"
    else:
        emoji = ":eggplant:"

    await interraction.response.send_message(f"{interraction.user.mention} har {length} cm balle {emoji}")

# Launch the client
bot.run(TOKEN)
