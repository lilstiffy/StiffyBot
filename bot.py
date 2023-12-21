import os
import random
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import chatgpt.discord_gpt as chatgpt

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
    await ctx.send("Incorrect usage of command. Please try again.")


@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}!")


@bot.event
async def on_member_remove(member):
    await member.send(f"See you {member.name}!")


# -- DEFINED COMMANDS --
@bot.tree.command(name="ping")
async def ping(interraction: discord.Interaction):
    """Ping the bot"""
    await interraction.response.send_message(f"{interraction.user.mention} :white_check_mark:", ephemeral=True)


@bot.tree.command(name="8ball")
@app_commands.describe(fråga="Din fråga")
async def eight_ball(interraction: discord.Interaction, fråga: str):
    """Ask the magic 8ball a question"""
    with open("assets/8ball_responses.txt", "r") as f:
        eight_ball_responses = f.read().splitlines()

    embed = discord.Embed(
        description=f"{interraction.user.mention} asked the 8ball:",
        color=discord.Color.purple()
    )
    embed.set_author(
        name="8ball",
        icon_url="https://github.com/lilstiffy/StiffyBot/blob/master/assets/8ball.png?raw=true"
    )

    embed.add_field(name="", value=fråga, inline=False)
    embed.add_field(name="The answer is", value=random.choice(eight_ball_responses), inline=False)

    await interraction.response.send_message(embed=embed)


@bot.tree.command(name="russian_roulette")
async def russian_roulette(interraction: discord.Interaction):
    """Play a round of russian roulette"""
    did_shoot = random.randint(1, 6) == 1

    embed = discord.Embed(
        title="Russian roulette",
        description=f"{interraction.user.mention} played a round of russian roulette",
        color=discord.Color.red() if did_shoot else discord.Color.green()
    )

    if did_shoot:
        import datetime
        await interraction.user.timeout(datetime.timedelta(minutes=5), reason="You died playing russian roulette ☠️")

    embed.add_field(name="Outcome", value="Shot himself ☠️" if did_shoot else "Survived 🎉")

    await interraction.response.send_message(embed=embed)


@bot.tree.command(name="chatgpt")
async def gpt(interraction: discord.Interaction, *, query: str):
    """Ask ChatGPT a question"""
    await interraction.response.defer()
    gpt_response = await chatgpt.chat_with_gpt(query)

    embed = discord.Embed(
        description=f"{interraction.user.mention}",
        color=discord.Color.from_rgb(128, 170, 158)
    )

    embed.set_author(
        name="ChatGPT",
        icon_url="https://github.com/lilstiffy/StiffyBot/blob/master/assets/chatgpt.png?raw=true"
    )

    trimmed_response = gpt_response[:1020] + "..." if len(gpt_response) > 1020 else gpt_response

    embed.add_field(name="", value=query, inline=False)
    embed.add_field(name="Response", value=trimmed_response, inline=False)

    await interraction.followup.send(embed=embed)


@bot.tree.command(name="roll")
async def roll(interaction: discord.Interaction, dice: str, count: int = 1):
    """Roll dices: d4, d6, d8, d10, d12, d20"""

    # Define the supported dice
    valid_dice = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20']

    # Check if the specified dice is valid
    if dice not in valid_dice:
        await interaction.response.send_message("Invalid dice :game_die:. Supported dice: d4, d6, d8, d10, d12, d20")
        return

    # Roll the specified dice n times
    result = random.randint(1, int(dice[1:])) * count

    embed = discord.Embed(
        description=f"{interaction.user.mention} rolled a {dice} :game_die:",
        color=discord.Color.from_rgb(128, 170, 158)
    )

    embed.set_author(
        name="Dice roll",
        icon_url="https://github.com/lilstiffy/StiffyBot/blob/master/assets/purple_d20.png?raw=true"
    )
    embed.add_field(name="Roll", value=result, inline=False)

    # Send the result to the channel
    await interaction.response.send_message(f"{interaction.user.mention} rolled a {dice} :game_die:: {result}")

# Launch the client
bot.run(TOKEN)
