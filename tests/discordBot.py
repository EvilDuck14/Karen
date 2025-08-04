import discord
from discord.ext import commands
#from discord import app_commands

from karen.evaluate import evaluate

from karen import hiddenData # delete - used for environment variables
BOT_TOKEN = hiddenData.BOT_TOKEN # your token here

intents = discord.Intents.default()
intents.guild_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=1401751994477056010)

# @bot.tree.command(name="eval", description="evaluates given combo", guild=GUILD_ID)
# async def eval(interaction: discord.Interaction, combo: str):
#     output = evaluate(combo)
#     try:
#         await interaction.response.send_message(output)
#     except Exception as e:
#         print(e)

# @bot.tree.command(name="evaln", description="evaluates given combo with no errors shown", guild=GUILD_ID)
# async def evaln(interaction: discord.Interaction, combo: str):
#     output = evaluate(combo, printWarnings=False)
#     try:
#         await interaction.response.send_message(output)
#     except Exception as e:
#         print(e)

@bot.command()
async def eval(ctx, *arr):
    inputString = "".join(str(x) for x in arr)
    output = evaluate(inputString)
    try:
        await ctx.send(output)
    except Exception as e:
        print(e)

@bot.command()
async def evaln(ctx, *arr):
    inputString = "".join(str(x) for x in arr)
    output = evaluate(inputString, printWarnings=False)
    try:
        await ctx.send(output)
    except Exception as e:
        print(e)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        await bot.tree.sync(guild=GUILD_ID)
        print("synced commands")
    except Exception as e:
        print(e)

bot.run(BOT_TOKEN)