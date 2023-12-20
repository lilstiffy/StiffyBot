import os
import discord
import random

from openai import AsyncOpenAI

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

# Initialise OpenAI
openAiClient = AsyncOpenAI(api_key=os.getenv('OPEN_AI_TOKEN'))


# -- ChatGPT functions --
async def chat_with_gpt(input_text):
    try:
        response = await openAiClient.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": input_text}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Ett fel inträffade: {str(e)}"


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
    await ctx.send("Felaktig användning av kommando")


@bot.event
async def on_member_join(member):
    await member.send(f"Välkommen till servern {member.name}!")


@bot.event
async def on_member_remove(member):
    await member.send(f"Vi ses {member.name}!")


# -- DEFINED COMMANDS --
@bot.tree.command(name="ping")
async def ping(interraction: discord.Interaction):
    """Pinga boten"""
    await interraction.response.send_message(f"{interraction.user.mention} :white_check_mark:", ephemeral=True)


@bot.tree.command(name="say")
@app_commands.describe(thing_to_say="What to say")
async def say(interraction: discord.Interaction, thing_to_say: str):
    """Få boten att säga något"""
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
    embed.set_author(
        name="8ball",
        icon_url="https://github.com/lilstiffy/StiffyBot/blob/master/assets/8ball.png?raw=true"
    )

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


@bot.tree.command(name="chatgpt")
async def gpt(interraction: discord.Interaction, *, gpt_input: str):
    """Ställ GPT-3.5 en fråga"""
    await interraction.response.defer()
    gpt_response = await chat_with_gpt(gpt_input)

    embed = discord.Embed(
        description=f"{interraction.user.mention} frågade GPT-3.5:",
        color=discord.Color.from_rgb(128, 170, 158)
    )

    embed.set_author(
        name="GPT-3.5",
        icon_url="https://github.com/lilstiffy/StiffyBot/blob/master/assets/chatgpt.png?raw=true"
    )

    embed.add_field(name="", value=gpt_input, inline=False)
    embed.add_field(name="Svar", value=gpt_response, inline=False)

    await interraction.followup.send(embed=embed)

# Launch the client
bot.run(TOKEN)
