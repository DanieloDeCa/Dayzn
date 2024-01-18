import json
import os
import sys

import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, context, a=0):
        """
        List all commands.
        """
        prefix = config["prefix"]
        if not isinstance(prefix, str):
            prefix = prefix[0]
        embed = discord.Embed(title="Help", description="List of available commands:", color=0x42F56C)

        if a == 0:
            for i in self.bot.cogs:
                if i.lower() == "work":
                    continue

                cog = self.bot.get_cog(i.lower())
                commands = cog.get_commands()
                command_list = [command.name for command in commands]
                command_description = [command.help for command in commands]
                help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))
                embed.add_field(name=i.capitalize(), value=f'{help_text}', inline=False)
                embed.set_footer(text=f"Use .help 1 in order to see the commands for economy")
            await context.send(embed=embed)
        else:
            cog = self.bot.get_cog("work")
            commands = cog.get_commands()
            command_list = [command.name for command in commands]
            command_description = [command.help for command in commands]
            help_text = '\n'.join(f'{prefix}{n}' for n in command_list)
            embed.add_field(name="**Work**", value=f'{help_text}', inline=False)
            embed.set_footer(text=f"Use .help 1 in order to see the other commands")
            await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))