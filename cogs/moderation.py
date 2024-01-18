import json
import os
import platform
import random
import sys
import time

import discord
from discord import Permissions
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from cogs.economy import getbankdata, getcrypto, openaccount, opencrypto, ub

intents = discord.Intents.all()
intents.members = False

bot = Bot(command_prefix=".", intents=intents)

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

class moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', pass_context=True)
    @commands.has_permissions(administrator=True)
    async def kick(self, context, member: discord.Member, *, reason="Not specified"):
        """
        Kick a member out of the server.
        """
    
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Error!",
                description="User has Admin permissions.",
                color=0xD63840
            )
            await context.send(embed=embed)
        else:
            try:
                await member.kick(reason=reason)
                embed = discord.Embed(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{context.message.author}**!",
                    color=0x42F56C
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await context.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{context.message.author}**!\nReason: {reason}"
                    )
                except:
                    pass
            except:
                embed = discord.Embed(
                    title="Error!",
                    color=0xD63840
                )
                await context.message.channel.send(embed=embed)

    @commands.command(name="nick")
    @commands.has_permissions(administrator=True)
    async def nick(self, context, member: discord.Member, *, nickname=None):
        """
        Change the nickname of a member on the server
        """
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0x42F56C
            )
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Error!",
                color=0xD63840
            )
            await context.message.channel.send(embed=embed)

    @commands.command(aliases = ["addbal"])
    @commands.has_permissions(administrator=True)
    async def addmoney(self, context, mber: discord.Member, amount: int):
        """
        Adds money to a member
        """

        if not mber:
            mber = context.author

        await openaccount(mber)
        users = await getbankdata()
        user = mber

        users[str(user.id)]["wallet"] += amount
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)

        await context.send(f"Added ${amount} to {mber.display_name}!")

    @commands.command(name = "addbadge")
    @commands.has_permissions(administrator=True)
    async def addbadge(self, context, mber: discord.Member, badge: str):
        """
        Adds a badge to a member
        """

        if not mber:
            mber = context.author

        await openaccount(mber)
        users = await getbankdata()
        user = mber

        users[str(user.id)]["badge"] += badge
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)

        await context.send(f"Added the badge `{badge}` to {mber.display_name}!")

    @commands.command(aliases = ["removebal"])
    @commands.has_permissions(administrator=True)
    async def removemoney(self, context, mber: discord
    .Member, amount: int):
        """
        Removes money from a member
        """

        if not mber:
            mber = context.author

        await openaccount(mber)
        users = await getbankdata()
        user = mber

        users[str(user.id)]["wallet"] -= amount
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)

        await context.send(f"Removed ${amount} from {mber.display_name}!")

    @commands.command(aliases = ["setbal"])
    @commands.has_permissions(administrator=True)
    async def setmoney(self, context, mber: discord.Member, amount: int):
        """
        Sets money of a member
        """

        if not mber:
            mber = context.author

        await openaccount(mber)
        users = await getbankdata()
        user = mber

        users[str(user.id)]["wallet"] = amount
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)

        await context.send(f"Setted {mber.display_name} bal to {amount}!")

    @commands.command(aliases = ["setbankbal"])
    @commands.has_permissions(administrator=True)
    async def setbankmoney(self, context, mber: discord.Member, amount: int):
        """
        Sets bank money of a member
        """

        if not mber:
            mber = context.author

        await openaccount(mber)
        users = await getbankdata()
        user = mber

        users[str(user.id)]["bank"] = amount
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)

        await context.send(f"Setted {mber.display_name} bal to {amount}!")

    @commands.command(name = "setbitcoin")
    @commands.has_permissions(administrator=True)
    async def setbitcoin(self, context, mber: discord.Member, amount: int):
        """
        Sets bitcoin of a member
        """
        
        if not mber:
            mber = context.author

        await openaccount(mber)
        users = await getbankdata()
        user = mber

        users[str(user.id)]["bitcoin"] = amount
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)

        await context.send(f"Setted {mber.display_name} bitcoin to {amount}!")

    @commands.command(name = "setbitcoinval")
    @commands.has_permissions(administrator=True)
    async def setbitcoinval(self, context, amount: int):
        """
        Sets bitcoin sell
        """

        await opencrypto("bitcoin", amount)
        a = await getcrypto()
        a[str("bitcoin")]["value"] = amount
        with open("crypto.json", "w") as f:
           json.dump(a, f, indent=4)
        await context.send(f"Setted bitcoin to {amount}!")

    @commands.command(name = "setethval")
    @commands.has_permissions(administrator=True)
    async def setethval(self, context, amount: int):
        """
        Sets eth sell
        """

        await opencrypto("eth", amount)
        a = await getcrypto()
        a[str("eth")]["value"] = amount
        with open("crypto.json", "w") as f:
           json.dump(a, f, indent=4)
        await context.send(f"Setted eth to {amount}!")

    @commands.command(name = "seteth")
    @commands.has_permissions(administrator=True)
    async def seteth(self, context, mber: discord.Member, amount: int):
        """
        Sets ethereum of a member
        """

        if not mber:
            mber = context.author

        await openaccount(mber)
        users = await getbankdata()
        user = mber

        users[str(user.id)]["eth"] = amount
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)

        await context.send(f"Setted {mber.display_name} ethereum to {amount}!")

    @commands.command(name="ban")
    @commands.has_permissions(administrator=True)
    async def ban(self, context, member: discord.Member, *, reason="Not specified"):
        """
        Bans a user from the server.
        """

        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="Error!",
                    description="User has Admin permissions.",
                    color=0xD63840
                )
                await context.send(embed=embed)
            else:
                await member.ban(reason=reason)
                embed = discord.Embed(
                    title="User Banned!",
                    description=f"**{member}** was banned by **{context.message.author}**!",
                    color=0x42F56C
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await context.send(embed=embed)
                await member.send(f"You were banned by **{context.message.author}**!\nReason: {reason}")
        except:
            embed = discord.Embed(
                title="Error!",
                color=0xD63840
            )
            await context.send(embed=embed)

    @commands.command(name="warn")
    @commands.has_permissions(administrator=True)
    async def warn(self, context, member: discord.Member, *, reason="Not specified"):
        """
        Warns a user in his private messages.
        """

        embed = discord.Embed(
            title="User Warned!",
            description=f"**{member}** was warned by **{context.message.author}**!",
            color=0x42F56C
        )
        embed.add_field(
            name="Reason:",
            value=reason
        )

        await openaccount(context.author)

        users = await getbankdata()
        user = context.author

        await context.send(embed=embed)

        if (users[str(user.id)]["kick"] == 3):
            await member.send(f"You are banned\nReason: too many warnings")
            users[str(user.id)]["kick"] = 0
            return;

        users[str(user.id)]["kick"] += 1
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)
        try:
            await member.send(f"You were warned by **{context.message.author}**!\nReason: {reason}")
        except:
            pass

    @commands.command(name="purge")
    @commands.has_permissions(administrator=True)
    async def purge(self, context, amount):
        """
        Delete a number of messages.
        """
        
        try:
            amount = int(amount)
        except:
            embed = discord.Embed(
                title="Error!",
                description=f"{amount} is not a valid number.",
                color=0xD63840
            )
            await context.send(embed=embed)
            return
        if amount < 1:
            embed = discord.Embed(
                title="Error!",
                description=f"{amount} is not a valid number.",
                color=0xD63840
            )
            await context.send(embed=embed)
            return
        await context.message.channel.purge(limit=amount)

def setup(bot):
    bot.add_cog(moderation(bot))
