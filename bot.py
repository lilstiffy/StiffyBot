import os
import random
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import chatgpt.discord_gpt as chatgpt
import urbandictionary.urban_dictionary as ud

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
        for command in synced:
            print(f"Synced command: {command}")
        print(f"Synced: {len(synced)} command(s)\n______________________")
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
    print(f"Pinged by {interraction.user.name} ({interraction.user.id})")
    await interraction.response.send_message(f"{interraction.user.mention} :white_check_mark:", ephemeral=True)


@bot.tree.command(name="8ball")
@app_commands.describe(question="Din fråga")
async def eight_ball(interraction: discord.Interaction, question: str):
    """Ask the magic 8ball a question"""
    print(f"8ball command called by {interraction.user.name} ({interraction.user.id})")

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

    embed.add_field(name="", value=question, inline=False)
    embed.add_field(name="The answer is", value=random.choice(eight_ball_responses), inline=False)

    await interraction.response.send_message(embed=embed)


@bot.tree.command(name="russian_roulette")
async def russian_roulette(interraction: discord.Interaction):
    """Play a round of russian roulette"""
    print(f"Russian roulette command called by {interraction.user.name} ({interraction.user.id})")

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
    print(f"ChatGPT command called by {interraction.user.name} ({interraction.user.id})")

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


@bot.tree.command(name="urban")
async def urban(interraction: discord.Interaction, *, term: str):
    """Search for a term on Urban Dictionary"""
    print(f"Urban Dictionary command called by {interraction.user.name} ({interraction.user.id})")

    await interraction.response.defer()
    ud_response = await ud.request_term(term)

    try:
        entry = ud_response['list'][0]

        embed = discord.Embed(
            color=discord.Color.from_rgb(86, 170, 232)
        )

        embed.set_author(
            name="Urban Dictionary",
            icon_url="https://github.com/lilstiffy/StiffyBot/blob/master/assets/urban_dictionary.png?raw=true"
        )

        embed.add_field(name="Term", value=entry['word'], inline=False)
        embed.add_field(name="Definition", value=entry['definition'], inline=False)
        embed.add_field(name="Example", value=entry['example'], inline=False)

        await interraction.followup.send(embed=embed)
    except Exception as e:
        print(e)

        embed = discord.Embed(
            color=discord.Color.from_rgb(86, 170, 232)
        )

        embed.set_author(
            name="Urban Dictionary",
            icon_url="https://github.com/lilstiffy/StiffyBot/blob/master/assets/urban_dictionary.png?raw=true"
        )

        embed.add_field(name="Term", value=term, inline=False)
        if ud.API_KEY is None:
            embed.add_field(name="Error", value="Missing API key", inline=False)
        else:
            embed.add_field(name="Error", value="No definition found", inline=False)

        await interraction.followup.send(embed=embed)


@bot.tree.command(name="roll")
async def roll(interaction: discord.Interaction, dice: str, count: int = 1):
    """Roll dices: d4, d6, d8, d10, d12, d20"""
    print(f"Roll command called by {interaction.user.name} ({interaction.user.id})")

    # Define the supported dice
    valid_dice = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20']

    # Check if the specified dice is valid
    if dice not in valid_dice:
        await interaction.response.send_message("Invalid dice :game_die:. Supported dice: d4, d6, d8, d10, d12, d20")
        return

    # Roll the specified dice n times
    result = random.randint(1, int(dice[1:])) * count

    embed = discord.Embed(
        description=f"{interaction.user.mention} rolled {dice} :game_die:",
        color=discord.Color.purple()
    )

    embed.set_author(
        name="Dice roll",
        icon_url="https://github.com/lilstiffy/StiffyBot/blob/master/assets/purple_d20.png?raw=true"
    )

    embed.add_field(name="Count", value=count)
    embed.add_field(name="Roll", value=result)

    # Send the result to the channel
    await interaction.response.send_message(embed=embed)

# Launch the client
bot.run(TOKEN)
