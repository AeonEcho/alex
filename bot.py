import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix=".")

@client.command(brief="Load Cog")
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded module {extension}')

@client.command(brief="Unload Cog")
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded module {extension}')

@client.command(brief="Reload Cog")
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Reloaded module {extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('NTI2OTcwMjk5MTA4MDMyNTE0.XCGpVQ.WVrrVkKL2xSoHpaWqcK3oAmLmtQ')