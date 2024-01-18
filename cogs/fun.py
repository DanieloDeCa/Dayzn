import asyncio
import json
import os
import random
import sys

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from typing import List
from bs4 import BeautifulSoup

import os
from typing import Union
import requests

from cogs.economy import getbankdata, openaccount

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

from PIL import Image

COLORS = {
    (0, 0, 0): "⬛",
    (0, 0, 255): "🟦",
    (255, 0, 0): "🟥",
    (255, 255, 0): "🟨",
    (190, 100, 80):  "🟫",
    (255, 165, 0): "🟧",
    (160, 140, 210): "🟪",
    (255, 255, 255): "⬜",
    (0, 255, 0): "🟩",
}

def euclidean_distance(c1, c2):
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    d = ((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2) ** 0.5
    return d

def find_closest_emoji(color):
    c = sorted(list(COLORS), key=lambda k: euclidean_distance(color, k))
    return COLORS[c[0]]

def emojify_image(img, size=14):
    WIDTH, HEIGHT = (size, size)
    small_img = img.resize((WIDTH, HEIGHT), Image.NEAREST)

    emoji = ""
    small_img = small_img.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            emoji += find_closest_emoji(small_img[x, y])
        emoji += "\n"
    return emoji

class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="megaping")
    @commands.cooldown(1, 1000, BucketType.user)
    async def megaping(self, ctx, member: discord.Member=None, times=100):
        """ Pings a member many times """
        if times > 200:
            await ctx.send(f"I can't ping a member more than 200 times")
            return
        for i in range(times):
            await ctx.send(f"{member.mention}")

    @commands.command(aliases=['meow'])
    async def cat(self, ctx):
        """ Get a cat image """
        req = requests.get('https://api.thecatapi.com/v1/images/search')
        if req.status_code != 200:
            await ctx.reply("Couldn't get a meow", mention_author=False)
            print("Could not get a meow")
        catlink = json.loads(req.text)[0]
        rngcat = catlink["url"]
        em = discord.Embed(description="", color=0x42F56C )
        em.set_image(url=rngcat)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=['woof'])
    async def dog(self, ctx):
        """ Get a dog image """
        req = requests.get('http://random.dog/')
        if req.status_code != 200:
            await ctx.reply("Couldn't get a woof", mention_author=False)
            print("Could not get a woof")
        doglink = BeautifulSoup(req.text, 'html.parser')
        rngdog = 'http://random.dog/' + doglink.img['src']
        em = discord.Embed(description="", color=0x42F56C)
        em.set_image(url=rngdog)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(name="fact")
    async def dailyfact(self, context):
        """
        Get a fact.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0x42F56C )
                    context.reply(embed=embed, mention_author=False)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xD63840
                    )
                    context.reply(embed=embed, mention_author=False)

    @commands.command(name="emojify")
    async def emojify(self, context, url: Union[discord.Member, str], size: int = 32):
        """
        Emojifies a image
        """
        if not isinstance(url, str):
            url = context.author.avatar

        def get_emojified_image():
            r = requests.get(url, stream=True)
            image = Image.open(r.raw).convert("RGB")
            res = emojify_image(image, size)

            if size > 14:
                res = f"{res}"
            return res

        result = await self.bot.loop.run_in_executor(None, get_emojified_image)
        await context.reply(result, mention_author=False)

    @commands.command(aliases=["cf"])
    async def coinflip(self, ctx, bet_on: str, amount: int):
        """
        Does a coinflip with a bet
        """
        user = ctx.author
        await openaccount(user)

        bet_on = "heads" if "h" in bet_on.lower() else "tails"
        if not 500 <= amount <= 5000:
            return await ctx.reply("You can only bet amount between 500 and 5000", mention_author=False)

        reward = round(amount / 2)
        users = await getbankdata()
        if users[str(user.id)]["wallet"] < amount:
            return await ctx.reply("You don't have enough money", mention_author=False)

        coin = ["heads", "tails"]
        result = random.choice(coin)
        to = users[str(user.id)]["multiplier"]

        if result != bet_on:
            users[str("1093406970393931847")]["wallet"] += amount
            users[str(user.id)]["wallet"] -= amount
            with open("currency.json","w") as f:
                json.dump(users,f, indent=4)
            return await ctx.reply(f"I got {result}, You lost {amount}", mention_author=False)

        users[str(user.id)]["wallet"] += reward*to
        users[str(user.id)]["1093406970393931847"] -= reward*to
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)
        return await ctx.reply(f"You got {result}, I lost {reward*to}", mention_author=False)

    @commands.command(name="slots")
    async def slots(self, ctx: commands.Context, amount: int):
        """
        Play slots and win money
        """
                
        user = ctx.author
        await openaccount(user)
        if not 1000 <= amount <= 10000:
            return await ctx.reply("You can only bet amount between 1000 and 10000", mention_author=False)

        users = await getbankdata()
        if users[str(user.id)]["wallet"] < amount:
            return await ctx.reply(f"You don't have {amount}$", mention_author=False)

        slot1 = ["💝", "🎉", "💎", "💵", "💰", "🚀", "🍿"]
        slot2 = ["💝", "🎉", "💎", "💵", "💰", "🚀", "🍿"]
        slot3 = ["💝", "🎉", "💎", "💵", "💰", "🚀", "🍿"]
        sep = " | "

        em = discord.Embed(
            description=f"\n"
                        f"| {sep.join(slot1[:3])} |\n"
                        f"| {sep.join(slot2[:3])} | 📍\n"
                        f"| {sep.join(slot3[:3])} |\n"
                        f""
        )
        msg = await ctx.reply(content="spinning the slot", embed=em, mention_author=False)
        await asyncio.sleep(3)

        total = len(slot1)
        if total % 2 == 0:
            mid = total / 2
        else:
            mid = (total + 1) // 2

        random.shuffle(slot1)
        random.shuffle(slot2)
        random.shuffle(slot3)
        result: List[List[str]] = []
        for x in range(total):
            result.append([slot1[x], slot2[x], slot3[x]])

        em = discord.Embed(
            description=f"\n"
                        f"| {sep.join(result[mid - 1])} |\n"
                        f"| {sep.join(result[mid])} | 📍\n"
                        f"| {sep.join(result[mid + 1])} |\n"
                        f""
        )

        slot = result[mid]
        s1 = slot[0]
        s2 = slot[1]
        s3 = slot[2]
        to = users[str(user.id)]["multiplier"]
        if s1 == s2 == s3:
            reward = round(amount / 2)
            users[str(user.id)]["wallet"] += (amount + reward)
            content = f"{user.mention} Jackpot! you won {round((amount + reward)*to):,}$"
        elif s1 == s2 or s2 == s3 or s1 == s3:
            reward = round(amount / 4)
            users[str(user.id)]["wallet"] += (amount + reward)
            content = f"{user.mention} GG! you only won {round((amount + reward)*to):,}$"
        else:
            users[str(user.id)]["wallet"] =- amount
            content = f"{user.mention} You lost {amount}$"

        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)

        return await msg.edit(content=content, embed=em)

    @commands.command(name="dice")
    async def dice(self, ctx, amount: int, dice: int):
        """
        Roll the dice and win money
        """
        user = ctx.author
        await openaccount(user)

        rdice = [1, 2, 3, 4, 5, 6]
        if dice not in rdice:
            return await ctx.reply("Enter a number of dice(1 - 6)", mention_author=False)

        if not 1000 <= amount <= 5000:
            return await ctx.reply("You can only bet between 1000 and 5000", mention_author=False)

        users = await getbankdata()
        if users[str(user.id)]["wallet"] < amount:
            return await ctx.reply("You don't have enough money", mention_author=False)

        result = await ctx.reply(f"rolling the dice...", mention_author=False)
        await asyncio.sleep(2)

        rand_num = random.choice(rdice)
        if rand_num != dice:
            users[str(user.id)]["wallet"] -= round(amount)
            users[str("1093406970393931847")]["wallet"] += round(amount)
            return await result.edit(f"Got {rand_num}, you lost {round(amount):,}$ 🍃")

        reward = round(amount / 2)
        users[str(user.id)]["wallet"] += reward
        users[str("1093406970393931847")]["wallet"] -= reward
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)
        await result.edit(f"Got {rand_num}, you won {(amount + reward):,}$ 🎉",)

    @commands.command(aliases=["roul"])
    async def roulette(self, ctx, colour: str):
        """ Colours roulette """
        colour_table = ["blue", "red", "green", "yellow"]
        if not colour:
            pretty_colours = ", ".join(colour_table)
            return await ctx.reply(f"Please pick a colour from: {pretty_colours}", mention_author=False)

        user = ctx.author
        await openaccount(user)
        users = await getbankdata()
        if users[str(user.id)]["wallet"] < 500:
            return await ctx.reply("You must have 500$ in order to play", mention_author=False)

        colour = colour.lower()
        if colour not in colour_table:
            return await ctx.reply("give a correct color", mention_author=False)

        chosen_color = random.choice(colour_table)
        msg = await ctx.reply("spinning...", mention_author=False)
        await asyncio.sleep(2)
        result = f"Result: {chosen_color.upper()}"

        reward = random.randint(10,500)

        if chosen_color == colour:
            users[str(user.id)]["wallet"] += reward
            users[str("1093406970393931847")]["wallet"] -= reward
            return await msg.edit(content=f"{result}\nYou won {reward:,}$ 🎉")
        
        users[str(user.id)]["wallet"] -= reward
        users[str("1093406970393931847")]["wallet"] += reward
        await msg.edit(content=f"> {result}\nYou lost {reward:,}$")
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)

    @commands.command(name="F")
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"for **{text}** " if text else ""
        await ctx.reply(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}", mention_author=False)

    @commands.command(name="rate")
    async def rate(self, ctx, *, text: commands.clean_content):
        """ Rates what you desire """
        rate_amount = random.randint(0, 100)
        await ctx.reply(f"I'd rate `{text}` a **{round(rate_amount)} / 100**", mention_author=False)

def setup(bot):
    bot.add_cog(Fun(bot))
