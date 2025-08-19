import discord
from discord.ext import commands

from karen.evaluate import evaluate
from karen.getCombo import *

import random

import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN") # save your bot token as an environment variable or paste it here

intents = discord.Intents.default()
intents.guild_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

@bot.command()
async def eval(ctx, *arr):
    inputString = " ".join(str(x) for x in arr)
    output = evaluate(inputString, simpleMode=True)
    embed = discord.Embed(title="", description="\n".join(output.split("\n")[0:5]), color=discord.Color(0x8C7FFF))
    embed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar)
    try:
        await ctx.send(embed=embed)
        if "```" in output:
            warningsEmbed = discord.Embed(title="", description="\n".join(output.split("\n")[5:])[3:-3].replace("WARNING:", "**WARNING:**"), color=discord.Color(0xB73A00))
            await ctx.send(embed=warningsEmbed)
    except Exception as e:
        print(e)

@bot.command()
async def evala(ctx, *arr):
    inputString = " ".join(str(x) for x in arr)
    output = evaluate(inputString)
    embed = discord.Embed(title="", description="\n".join(output.split("\n")[0:5]), color=discord.Color(0x604FFF))
    embed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar)
    try:
        await ctx.send(embed=embed)
        if "```" in output:
            warningsEmbed = discord.Embed(title="", description="\n".join(output.split("\n")[5:])[3:-3].replace("WARNING:", "**WARNING:**"), color=discord.Color(0xB73A00))
            await ctx.send(embed=warningsEmbed)
    except Exception as e:
        print(e)

@bot.command()
async def evaln(ctx, *arr):
    inputString = " ".join(str(x) for x in arr)
    output = evaluate(inputString, printWarnings=False)
    embed = discord.Embed(title="", description="\n".join(output.split("\n")[0:5]), color=discord.Color(0x604FFF))
    embed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar)
    try:
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)

@bot.command()
async def combo(ctx, *arr):
    inputString = " ".join(str(x) for x in arr)
    output = getCombo(inputString, simpleMode=True)
    embed = discord.Embed(title="", description="\n".join(output.split("\n")[0:5]), color=discord.Color(0x0094FF))
    embed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar)
    if "```" in output:
        embed = discord.Embed(title="", description=output[3:-3].replace("ERROR:", "**ERROR:**"), color=discord.Color(0xB73A00))
    try:
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)

@bot.command()
async def combos(ctx, *arr):
    output = listCombos()
    embed = discord.Embed(title="Karen Combo List", description=output, color=discord.Color(0x0094FF))
    embed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar)
    try:
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)

@bot.command()
async def help(ctx, *arr):
    command = "none" if len(arr) == 0 else arr[0]
    embed = discord.Embed(title="Karen Help Desk", description="", color=discord.Color(0x77C6FF))
    embed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar)

    if command.lower() in ["eval", "!eval"]:
        embed.add_field(name="!eval [combo sequence]", value="The *evaluate* command takes a combo sequence as input, and evaluates the minimum time taken to execute the combo, as well as the damage dealt. This command automatically corrects common input mistakes - for more complete control, use \"!evala\".", inline=False)
        embed.add_field(name="", value="Examples of combo sequences include \"tGu\", \"t goht upper\", or \"tracer > get over here targeting > uppercut\" (these are all equivalent). For a more complete description of combo notation, [see the documentation](https://github.com/EvilDuck14/Karen/).", inline=False )

    elif command.lower() in ["evala", "!evala"]:
        embed.add_field(name="!evala [combo sequence]", value="The *evaluate (advanced)* command takes a combo sequence as input, and evaluates the minimum range of times taken to execute the combo (accounting for projectile travel times), as well as the damage dealt. Unlike \"!eval\", this command doesn't correct common mistakes if the sequence is possible in-game (such as \"usG\" being input instead of \"uwG\").", inline=False)

    elif command.lower() in ["evaln", "!evaln"]:
        embed.add_field(name="!evaln [combo sequence]", value="The *evaluate (no warnings)* command is equivalent to \"!evala\", but doesn't output any warnings.", inline=False)
    
    elif command.lower() in ["combo", "!combo"]:
        embed.add_field(name="!combo [combo name]", value="The *combo* command runs \"!evala\" on a combo given its name. For a list of all documented combo names, use \"!combos\".", inline=False)

    elif command.lower() in ["combos", "!combos"]:
        embed.add_field(name="!combos", value="The *combos* command prints a list of all documented combos, as well as their short-form notations. These are the labels added when a known command is evaluated, and these names can be passed into the \"!combo\" command.", inline=False)

    elif command.lower() in ["help", "!help"]:
        descriptions = [ "The *help* command displays a detailed description of a given command. If no command is given, it instead lists all commands, giving brief descriptions." ] * 10 + [
            "Come on... you can figure this one out.",
            "The fact that you've made it here tells me you already know what this one does.",
            "Look at you go. You nailed it.",
            "You can use this to explain to someone what a command does when you don't want to explain it yourself.",
            "Are you looking for an easter egg? Well, you found it.",
        ]
        embed.add_field(name="!help [command]", value=random.choice(descriptions), inline=False)

    else:
        embed.add_field(name="!eval [combo sequence]", value="Evaluates the time taken & damage dealt by a given combo.", inline=False)
        embed.add_field(name="!evala [combo sequence]", value="\"Advanced\" version of \"!eval\".", inline=False)
        embed.add_field(name="!evaln [combo sequence]", value="\"No warnings\" version of \"!evala\".", inline=False)
        embed.add_field(name="!combo [combo name]", value="Runs evaluation of a given combo.", inline=False)
        embed.add_field(name="!combos", value="Displays a list of all documented combos.", inline=False)
        embed.add_field(name="!help [command]", value="Explains the given command in greater detail.", inline=False)

    try:
        await ctx.send(embed=embed)
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