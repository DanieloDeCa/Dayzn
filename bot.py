import json
import os
import random
import sys
import random
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from cogs.economy import getcrypto, opencrypto

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class MyHelp(commands.HelpCommand):
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error, color=discord.Color.red())
        channel = self.get_destination()
        await channel.send(embed=embed)
    def get_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_group_help(self, group):
        embed = discord.Embed(title=self.get_command_signature(group), description=group.help, color=discord.Color.blurple())

        if filtered_commands := await self.filter_commands(group.commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "No Help Message Found... ")

        await self.get_destination().send(embed=embed)
    async def send_cog_help(self, cog):
        embed = discord.Embed(title=cog.qualified_name or "No Category", description=cog.description, color=discord.Color.blurple())

        if cog.qualified_name == "staff" or cog.qualified_name == "moderation":
            return
        if filtered_commands := await self.filter_commands(cog.get_commands()):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "No Help Message Found... ")

        await self.get_destination().send(embed=embed)
    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command), color=discord.Color.blurple())
        if command.help:
            embed.description = command.help
        channel = self.get_destination()
        await channel.send(embed=embed)
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=discord.Color.blurple())

        for cog, commands in mapping.items():
           filtered = await self.filter_commands(commands, sort=True)
           command_signatures = [self.get_command_signature(c) for c in filtered]

           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                if cog_name == "moderation" or cog_name == "staff" or cog_name == "No Category":
                    continue
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)


bot = Bot(command_prefix=config["prefix"], intents=intents, help_command=MyHelp())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Created on {bot.user.created_at}")
    print(f"Guilds: {len(bot.guilds)}")
    status_task.start()
    update_task.start()

@tasks.loop(minutes=0.3)
async def status_task():
    statuses = [f"{config['prefix']}help", "2k2Cat#4905"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

import aiohttp

@tasks.loop(minutes=10)
async def update_task():
    bamt = 0
    eamt = 0
    mamt = 0
    async with aiohttp.ClientSession() as session:
        raw_response = await session.get(
                    "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
                )
        response = await raw_response.text()
        response = json.loads(response)
        r = response["bpi"]["USD"]["rate"].replace(",", "")
        bamt = round(float(r))

        raw_responsee = await session.get(
                    "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD"
                )
        responsee = await raw_responsee.text()
        responsee = json.loads(responsee)
        re = responsee["USD"]
        eamt = round(float(re))

        await opencrypto("bitcoin", bamt)
        await opencrypto("eth", eamt)
        a = await getcrypto()
        a[str("bitcoin")]["value"] = bamt
        a[str("eth")]["value"] = eamt
        with open("crypto.json", "w") as f:
            json.dump(a, f, indent=4)
        bot.reload_extension("cogs.economy")
        print(f"successfully reloaded economy cog - btc: {bamt:,}; eth: {eamt:,};")

if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

@bot.command(name="reload")
async def reload(context):
    if not context.author.id in config["owners"]:
        return
    bot.reload_extension("cogs.economy")
    await context.reply("successfully reloaded crypto values", mention_author=False)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(
        f"{executedCommand} by {ctx.message.author}")

@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="You are on a cooldown!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xD63840
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission " + ", ".join(
                error.missing_perms) + " to execute this command!",
            color=0xD63840
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            color=0xD63840
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        await context.send(f'Syntax error')
    raise error

bot.run(config["token"])