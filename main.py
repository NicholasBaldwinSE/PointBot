import discord
import os
import re

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
bot.points_cache = {}

# Regex used to determine accumulation/decumulation.
POINT_REGEX = re.compile(r"(\+|-)?(\d+)")

# Simple point accumulation/decumulation.
@bot.command()
async def point(ctx: commands.Context, modifier: str, user: discord.Member):
    if ctx.guild.id not in bot.points_cache:
        bot.points_cache[ctx.guild.id] = {}
    
    if user.id not in bot.points_cache[ctx.guild.id]:
        bot.points_cache[ctx.guild.id][user.id] = 0

    if (match := POINT_REGEX.match(modifier)):
        state = match.group(1)
        num = int(match.group(2)) # If this isn't an int, there's a problem. Should almost always be one.

        # We only need to check one state. If it's a + or no character, then nothing changes.
        if state == "-":
            num *= -1
    
        bot.points_cache[ctx.guild.id][user.id] += num

    await ctx.send(f"User {user.name} has {bot.points_cache[ctx.guild.id][user.id]} points.")

# Run bot using token.
bot.run(os.getenv("TOKEN"))