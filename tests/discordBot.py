import discord
from discord.ext import commands

from karen.evaluate import evaluate

from karen import hiddenData # delete - used for environment variables
BOT_TOKEN = hiddenData.BOT_TOKEN # your token here

intents = discord.Intents.none()
intents.guild_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command()
async def eval(ctx, *arr):
    inputString = "".join(str(x) for x in arr)
    output = evaluate(inputString)
    await ctx.send(output)

bot.run(BOT_TOKEN)