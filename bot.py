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
    """Ask the magic 8ball a question"""
    eight_ball_responses = [
        "Det är säkert",
        "Det är absolut så",
        "Utan tvekan",
        "Ja, definitivt",
        "Du kan lita på det",
        "Som jag ser det, ja",
        "Mycket troligt",
        "Ja, absolut",
        "Svarar inte nu, försök igen senare",
        "Fråga mig senare",
        "Kan inte förutsäga nu",
        "Koncentrera dig och fråga igen",
        "Svarar inte",
        "Det ser inte så jätteljust ut",
        "Mycket tvivelaktigt",
        "Nej",
        "Mitt svar är nej",
        "Mycket osannolikt",
        "Definitivt inte",
        "Svaret är tveksamt",
        "Spåren pekar inte på det",
        "Tvivlar starkt",
        "Nej, det kommer inte att hända",
        "Inte en chans",
        "Glöm det",
        "Bra fråga, svårt att säga",
        "Jag vet inte, försök igen",
        "Kan inte svara nu",
        "Fråga mig senare, jag är upptagen",
        "Det är bättre du inte vet det nu"
    ]
    await interraction.response.send_message(f":crystal_ball: {fråga}\n:8ball: {random.choice(eight_ball_responses)}")


@bot.tree.command(name="russian_roulette")
async def russian_roulette(interraction: discord.Interaction):
    """Play russian roulette"""
    if random.randint(1, 6) == 1:
        # Timeout user for 5 minutes
        await interraction.response.send_message(f"{interraction.user.mention} :skull_crossbones: :boom: :gun:")
        import datetime
        duration = datetime.timedelta(minutes=5)
        await interraction.user.timeout(duration, reason="Du är död i 5 minuter")
    else:
        # User survives
        await interraction.response.send_message(f"{interraction.user.mention} :man: Klick! :gun:\n")


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

@bot.tree.command(name="roll")
async def roll(interaction: discord.Interaction, dice: str):
    """Rulla en tärning: d4, d6, d8, d10, d12, d20"""

    # Define the supported dice
    valid_dice = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20']

    # Check if the specified dice is valid
    if dice not in valid_dice:
        await interaction.response.send_message("Ogiltig tärning :game_die:. Typer som stöds: d4, d6, d8, d10, d12, d20")
        return

    # Roll the specified dice
    result = random.randint(1, int(dice[1:]))

    # Send the result to the channel
    await interaction.response.send_message(f"{interaction.user.mention} Rullade en {dice} :game_die:: {result}")

# Launch the client
bot.run(TOKEN)
