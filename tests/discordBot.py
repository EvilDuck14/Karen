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

@bot.command()
async def eval(ctx, *arr):
    inputString = "".join(str(x) for x in arr)
    output = evaluate(inputString, limitLength=True)
    try:
        await ctx.send(output)
    except Exception as e:
        print(e)

@bot.command()
async def evaln(ctx, *arr):
    inputString = "".join(str(x) for x in arr)
    output = evaluate(inputString, printWarnings=False, limitLength=True)
    try:
        await ctx.send(output)
    except Exception as e:
        print(e)

@bot.command()
async def evald(ctx, *arr):
    inputString = "".join(str(x) for x in arr)
    output = evaluate(inputString, timeFromDamage=True, limitLength=True)
    try:
        await ctx.send(output)
    except Exception as e:
        print(e)

@bot.command()
async def evaldn(ctx, *arr):
    inputString = "".join(str(x) for x in arr)
    output = evaluate(inputString, timeFromDamage=True, printWarnings=False, limitLength=True)
    try:
        await ctx.send(output)
    except Exception as e:
        print(e)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        await bot.tree.sync()
        print("synced successfully")
    except Exception as e:
        print(e)

bot.run(BOT_TOKEN)