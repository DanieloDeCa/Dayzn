import json
import os
import sys
import time
import discord
from discord.ext import commands
from cogs.economy import openaccount

intents = discord.Intents.default()
intents.members = True

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

class staff(discord.Client, commands.Cog, name="staff"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say", aliases=["echo"])
    async def say(self, context, *, args):
            """
            The bot will say anything you want.
            """
            await context.message.delete()
            await context.send(args)

    @commands.command(name="embed")
    async def embed(self, context, *, args):
            """
            The bot will say anything you want, but within embeds.
            """
            embed = discord.Embed(
                description=args,
                color=0x42F56C
            )
            await context.send(embed=embed)

def setup(bot):
    bot.add_cog(staff(bot))