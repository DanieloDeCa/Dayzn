import json
import os
import platform
import random
import sys
import requests
import aiohttp
import discord
from itertools import cycle
from discord.ext import commands
import urllib.parse, urllib.request, re, json, requests, webbrowser, aiohttp, asyncio, functools, logging

from cogs.economy import getbankdata, openaccount

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

languages = {
    'hu'    : 'Hungarian, Hungary',
    'nl'    : 'Dutch, Netherlands',
    'no'    : 'Norwegian, Norway',
    'pl'    : 'Polish, Poland',
    'pt-BR' : 'Portuguese, Brazilian, Brazil',
    'ro'    : 'Romanian, Romania',
    'fi'    : 'Finnish, Finland',
    'sv-SE' : 'Swedish, Sweden',
    'vi'    : 'Vietnamese, Vietnam',
    'tr'    : 'Turkish, Turkey',
    'cs'    : 'Czech, Czechia, Czech Republic',
    'el'    : 'Greek, Greece',
    'bg'    : 'Bulgarian, Bulgaria',
    'ru'    : 'Russian, Russia',
    'uk'    : 'Ukranian, Ukraine',
    'th'    : 'Thai, Thailand',
    'zh-CN' : 'Chinese, China',
    'ja'    : 'Japanese',
    'zh-TW' : 'Chinese, Taiwan',
    'ko'    : 'Korean, Korea'
}

locales = [ 
    "da", "de",
    "en-GB", "en-US",
    "es-ES", "fr",
    "hr", "it",
    "lt", "hu",
    "nl", "no",
    "pl", "pt-BR",
    "ro", "fi",
    "sv-SE", "vi",
    "tr", "cs",
    "el", "bg",
    "ru", "uk",
    "th", "zh-CN",
    "ja", "zh-TW",
    "ko"
]

class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, ctx):
        """
        Bot info.
        """
        embed = discord.Embed(
            description="Blackyy",
            color=0x42F56C
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Developer:",
            value="2k2Cat#4905",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"{config['prefix']}",
            inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, ctx):
        """
        Check if the bot is alive.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x42F56C
        )
        await ctx.send(embed=embed)

    @commands.command(name="upgrade")
    async def multiplier(self, context, levels=1):
        """
        Upgrade for 1500000$
        """
        await openaccount(context.author)

        users = await getbankdata()
        user = context.author
        efg = (1500000*levels)*users[str(user.id)]["multiplier"]
        if users[str(user.id)]["wallet"] < efg:
            await context.send(f"You don't have {efg}$", mention_author=False)
            return
    
        if users[str(user.id)]["multiplier"]+levels > 100:
            await context.reply(f"Your level can't be higher than 100", mention_author=False)
            return
        multi = users[str(user.id)]["multiplier"] + levels
        users[str(user.id)]["multiplier"] += levels
        users[str(user.id)]["wallet"] -= efg
        
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)

        await context.reply(f"Your level has been upgraded to {multi}", mention_author=False)

    @commands.command(name="description")
    async def description(self, context, *, text):
        """
        Set a description for 50000$
        """
        await openaccount(context.author)
        users = await getbankdata()
        user = context.author
        if users[str(user.id)]["wallet"] < 50000:
            await context.reply(f"You don't have 500000$", mention_author=False)
            return
    
        if len(text) > 24:
            await context.reply(f"Your description can't be higher than 24 letters", mention_author=False)
            return
        users[str(user.id)]["description"] = "| " + text
        
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)
 
        await context.reply(f"Your description has been set to `{text}`", mention_author=False)
    @commands.command(name="invite")
    async def invite(self, ctx):
        """
        Get the invite link of the bot to be able to invite it
        """
        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&permissions=8&scope=bot).",
            color=0x42F56C 
        )
        try:
            await ctx.author.send(embed=embed)
            await ctx.reply("I sent you a private message", mention_author=False)
        except discord.Forbidden:
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="poll")
    async def poll(self, ctx, *, title):
        """
        Create a poll where members can vote.
        """
        embed = discord.Embed(
            title=f"{title}",
            color=0x42F56C
        )
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")

    @commands.command(name="8ball")
    async def eight_ball(self, ctx, *, question):
        """
        Ask any question to the bot.
        """
        answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
                   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
                   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
                   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
                   'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{answers[random.randint(0, len(answers))]}",
            color=0x42F56C
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="bitcoin")
    async def bitcoin(self, ctx):
        """
        Get the current price of bitcoin.
        """
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json")
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title="Info",
                description=f"Current bitcoin price is: ${response['bpi']['USD']['rate']}",
                color=0x42F56C
            )
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="avatar")
    @commands.guild_only()
    async def avatar(self, ctx, *, user: discord.Member = None):
        """Get the avatar of a member"""
        user = user or ctx.author
        await ctx.reply(user.avatar, mention_author=False)

def setup(bot):
    bot.add_cog(general(bot))