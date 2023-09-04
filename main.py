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
async def point(ctx: commands.Context, modifier: str, user: discord.Member, name: str):
    if ctx.guild.id not in bot.points_cache:
        bot.points_cache[ctx.guild.id] = {}
    
    if name not in bot.points_cache[ctx.guild.id]:
        await ctx.send(f"Point type {name} does not exist.")
        return

    if user.id not in bot.points_cache[ctx.guild.id][name]:
        bot.points_cache[ctx.guild.id][name][user.id] = 0

    if (match := POINT_REGEX.match(modifier)):
        state = match.group(1)
        num = int(match.group(2)) # If this isn't an int, there's a problem. Should almost always be one.

        # We only need to check one state. If it's a + or no character, then nothing changes.
        if state == "-":
            num *= -1
    
        bot.points_cache[ctx.guild.id][name][user.id] += num

    await ctx.send(f"User {user.name} has {bot.points_cache[ctx.guild.id][name][user.id]} {name} points.")

@bot.command()
async def addpoint(ctx: commands.Context, name: str):
    # Adds a type of point to the server's list.
    if ctx.guild.id not in bot.points_cache:
        bot.points_cache[ctx.guild.id] = {}
    
    # Limit each server to 3 different kinds of points.
    if len(bot.points_cache[ctx.guild.id]) == 3:
        await ctx.send("Reached cap of 3 different types of points. Either rename or delete a type.")
        return

    bot.points_cache[ctx.guild.id][name] = {}

    await ctx.send(f"Created point type {name}.")

@bot.command()
async def delpoint(ctx: commands.Context, name: str):
    # Removes a type of point from the server's list.
    if ctx.guild.id not in bot.points_cache:
        return

    # Check if no point types exist.
    if len(bot.points_cache[ctx.guild.id]) == 0:
        await ctx.send("Cannot remove point type, no point types exist.")
        return

    # Check if specific point type doesn't exist.
    if name not in bot.points_cache[ctx.guild.id]:
        await ctx.send(f"Cannot remove point type {name}, does not exist.")
        return

    del bot.points_cache[ctx.guild.id][name]

    await ctx.send(f"Deleted point type {name}.")

@bot.command()
async def renamepoint(ctx: commands.Context, name: str, newname: str):
    # Renames a type of point.
    if ctx.guild.id not in bot.points_cache:
        return

    if name not in bot.points_cache[ctx.guild.id]:
        await ctx.send(f"Cannot rename point type {name}. Does not exist.")
        return

    # This effectively renames the point. Note, it is not very
    # efficient and probably won't translate well to Redis/SQL.
    # Will need a better system for storing point names such as 
    # an internal ID system.
    bot.points_cache[ctx.guild.id][newname] = bot.points_cache[ctx.guild.id].pop(name)

    await ctx.send(f"Renamed point type {name} to {newname}.")

# Run bot using token.
bot.run(os.getenv("TOKEN"))