import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

# Loads environment info from a .env file
# as if it were an official environment var
load_dotenv()

# Set up intents. Use default since this bot
# is mostly going to be self-hosted and not 
# large, meaning intents matter somewhat less.
intents = discord.Intents.default()
intents.message_content = True

# Create bot.
# Command prefix is unlikely to be used with the advent of 
# slash commands.
bot = commands.Bot(command_prefix="::", intents=intents)

# Simple test command to test out token.
@bot.command()
async def respond(ctx: commands.Context):
    await ctx.channel.send("Response.")

# Run bot using token.
bot.run(os.getenv("TOKEN"))