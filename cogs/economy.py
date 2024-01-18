import asyncio
import json
import os
import sys
import discord
from discord.ext import commands
import random
import json
import os
import random
import sys
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from typing import List, Tuple
from PIL import Image

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

if not os.path.isfile("crypto.json"):
    sys.exit("'crypto.json' not found! Please add it and try again.")
else:
    with open("crypto.json") as file:
        crypto = json.load(file)

intents = discord.Intents.default()
intents.members = True

class Shop(discord.ui.View):
    @discord.ui.select(
        placeholder="Choose which shop to display",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                emoji="🪱", label="Normal", description="Shows the dollar currency shop"
            ),
            discord.SelectOption(
                emoji="<:BTC:1110246895147823114>", label="Crypto", description="Shows the crypto shop"
            ),
            discord.SelectOption(
                emoji="<:meth:1110538413360295986>", label="Black Market", description="Shows the black market"
            ),
        ],
    )
    async def select_callback(self, select, interaction):
        if select.values[0] == "Normal":
            em = discord.Embed(title="Shop", color=0x42F56C)
            for item in mainshop:
                name = item["name"]
                price = item["price"]
                ico = item["icon"]
                em.add_field(name=f"{ico} {name}", value=f"{price:,}$")
                em.set_footer(text="Use .buy <amount> <itemname> in order to buy")
        elif select.values[0] == "Crypto":
            em = discord.Embed(title="Crypto shop", color=0x42F56C)
            for item in btcshop:
                name = item["name"]
                price = item["price"]
                ico = item["icon"]
                em.add_field(name=f"{ico} {name}", value=f"{price}₿")
            for item in ethshop:
                name = item["name"]
                price = item["price"]
                ico = item["icon"]
                em.add_field(name=f"{ico} {name}", value=f"{price}Ξ", inline=False)
        else:
            em = discord.Embed(title="Black Market", color=discord.Color.blurple())
            for item in blackmarket:
                name = item["name"]
                price = item["price"]
                ico = item["icon"]
                em.add_field(name=f"{ico} {name}", value=f"{price}$")
            
        em.set_footer(text="Use .buy <amount> <itemname> in order to buy")
        await interaction.response.edit_message(embed=em, view=self)

mainshop = [
    {
        "name": "Ledger",
        "price": 50,
        "icon": ":ledger:",
    },
    {"name": "Newspaper", "price": 200, "icon": ":newspaper:"},
    {
        "name": "Roll of paper",
        "price": 250,
        "description": "Item",
        "icon": ":roll_of_paper:",
    },
    {"name": "Teddy bear", "price": 300, "icon": ":teddy_bear:"},
    {"name": "Worm", "price": 500, "icon": ":worm:"},
    {
        "name": "Ethereum",
        "price": crypto["eth"]["value"],
        "icon": "<:ETH:1110246747856437402>",
    },
    {"name": "Hut", "price": 500, "icon": ":hut:"},
    {"name": "Fish", "price": 2000, "icon": ":fish:"},
    {
        "name": "Shovel",
        "price": 3500,
        "icon": "<:shovel:1109905081219956808>",
    },
    {
        "name": "Fishing pole",
        "price": 3500,
        "icon": "<:fishingpole:1109905082595672185>",
    },
    {
        "name": "Cryptowallet",
        "price": 4250,
        "icon": "<:Binance:1110235474297106532>",
    },
    {"name": "Oil", "price": 4500, "description": "Item", "icon": ":oil:"},
    {
        "name": "Bitcoin",
        "price": crypto["bitcoin"]["value"],
        "icon": "<:BTC:1110246895147823114>",
    },
    {
        "name": "Padlock",
        "price": 29146,
        "icon": "<:padlock:1109905078019707003>",
    },
    {"name": "House", "price": 30000, "icon": ":house:"},
    {
        "name": "Firewall",
        "price": 35000,
        "icon": ":fire:",
    },
    {
        "name": "Bank",
        "price": 50000,
        "icon": ":bank:",
    },
    {
        "name": "Luxury Mansion",
        "price": 1000000,
        "icon": "<:luxemansion:1110211202799382589>",
    },
    {
        "name": "Exotic Mansion",
        "price": 3500000,
        "icon": "<:ExoticMansion:1110211145719087126>",
    },
]

btcshop = [
    {"name": "Stone Moyai", "price": 200, "icon": ":moyai:"},
    {
        "name": "Hacker",
        "price": 500,
        "icon": ":smirk_cat::computer:",
    },
    {
        "name": "Golden Moyai",
        "price": 250000,
        "icon": "<:goldenmoyai3:1109912461886373988>",
    },
    {
        "name": "Coems",
        "price": 300000,
        "icon": ":money_mouth:",
    },
    {
        "name": "Swastika",
        "price": 42000000,
        "icon": "<:swastika:1109944785021710527>",
    },
]

ethshop = [
]

blackmarket = [
    {
        "name": "Pseudoephedrine",
        "price": 3600,
        "icon": "<:Pseudoephedrine:1110938350405292193>",
    },
    {
        "name": "Red Phosphorus",
        "price": 561,
        "icon": "<:RedPhosphorus:1110940323548500008>",
    },
    {
        "name": "Hydriodic Acid",
        "price": 915,
        "icon": "<:hydriodicacid:1110944194362609725>",
    },
    {
        "name": "Sodium Hydroxide",
        "price": 1543,
        "icon": "<:SodiumHydroxide:1110943550432104530>",
    },
    {
        "name": "Hydrogen Chloride",
        "price": 1943,
        "icon": "<:HydrogenChloride:1110942998474264647>",
    },
    {
        "name": "Meth lab",
        "price": 5000000,
        "icon": "<:methlab:1110950706254467175>",
    },
]

async def buy_item(
    context, member, item_name, amount, shop=mainshop,curr="wallet"
):
    name_ = None
    icon = ":poop:"
    for item in shop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            icon = item["icon"]
            break

    if name_ == None:
        return [False, 1]

    users = await getbankdata()
    cost = price * amount
    user = member

    if cost > users[str(user.id)][curr]:
         return [False, 2]

    if item_name == "worm" or item_name == "fish":
        return [False, 3]

    foundcr = 0
    if users[str(user.id)]["cryptowallet"] == "no":
        foundcr = 1

    if item_name == "bitcoin":
        if foundcr == 1:
            return [False, 5]
        users[str(user.id)][curr] -= cost
        users[str(user.id)]["bitcoin"] += amount

        if not ":coin:" in users[str(user.id)]["badge"]:
            users[str(user.id)]["badge"] += ":coin:"

        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)
        return [True, "Worked"]
    elif item_name == "ethereum":
        if foundcr == 1:
            return [False, 5]
        users[str(user.id)][curr] -= cost
        users[str(user.id)]["eth"] += amount

        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)
        return [True, "Worked"]
    elif item_name == "shovel":
        if not "<:shovel:1109905081219956808>" in users[str(user.id)]["badge"]:
            users[str(user.id)]["badge"] += "<:shovel:1109905081219956808>"
    elif item_name == "cryptowallet":
        if foundcr == 0:
            return [False, 6]
        users[str(user.id)][curr] -= cost
        if not "<:Binance:1110235474297106532>" in users[str(user.id)]["badge"]:
            users[str(user.id)]["badge"] += "<:Binance:1110235474297106532>"
        users[str(user.id)]["cryptowallet"] = "yes"
        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)
        return [True, "Worked"]

    if item_name == "bank":
        for item in users[str(user.id)]["bag"]:
            name = item["item"]

            if name == "bank":
                await context.reply(f"You already have a bank", mention_author=False)
                return

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                users[str(user.id)]["bag"][index]["amount"] += amount
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount, "icon": icon}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount, "icon": icon}
        users[str(user.id)]["bag"] = [obj]

    users[str(user.id)][curr] -= cost

    with open("currency.json", "w") as f:
        json.dump(users, f, indent=4)

    return [True, "Worked"]

async def sell_item(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    users = await getbankdata()
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None and name != "worm":
                price = (0.7 * item["price"]) * users[str(user.id)]["multiplier"]
            elif price == None:
                price = item["price"] * users[str(user.id)]["multiplier"]
            break

    if name_ == None:
        return [False, 1]

    if name_ == "bitcoin" or name_ == "ethereum" or name_ == "cryptowallet" or name_ == "meth":
        return [False, 4]

    cost = round((price * amount) * users[str(user.id)]["multiplier"])

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                if amount < 1:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] -= amount
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    users[str(user.id)]["wallet"] += cost

    with open("currency.json", "w") as f:
        json.dump(users, f, indent=4)

    return [True, "Worked"]

class economy(discord.Client, commands.Cog, name="economy"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="crime")
    @commands.cooldown(1, 3, BucketType.user)
    async def crime(self, context):
        """
        Commit a crime
        """
        crime_array = ["Murder", "Pick Pocket", "Graffiti", "Fraud", "Arson"]
        await openaccount(context.author)
        bal = await ub(context.author)
        users = await getbankdata()
        user = context.author
        bag = users[str(context.author.id)]["bag"]
        methamt = 1
        hasmeth = 0
        index = 0
        purity = 1

        for item in bag:
            if item["item"] == "meth" and item["amount"] > 0:
                methamt = item["amount"]
                purity = item["purity"]
                hasmeth = 1
                break
            index += 1

        if hasmeth == 1:
            crime_array = ["Murder", "Pick Pocket", "Graffiti", "Fraud", "Arson", "Sell meth"]

        random.shuffle(crime_array)

        to = 5000
        risk = random.randint(100, 5000)*users[str(user.id)]["multiplier"]
        if bal[0] < to:
            await context.reply(
                f"You must have {to}$ in order to commit a crime", mention_author=False
            )
            return

        crime_a = crime_array[1]
        crime_b = crime_array[2]
        crime_c = crime_array[3]

        embed = discord.Embed(title="What crime do you want to commit?",
                              description=f"🇦 {crime_a}\n🇧 {crime_b}\n🇨 {crime_c}")
        message = await context.reply(embed=embed, mention_author=False)
        await message.add_reaction("🇦")
        await message.add_reaction("🇧")
        await message.add_reaction("🇨")

        def check(reaction, user):
            return user == context.author and str(reaction.emoji) in ["🇦", "🇧", "🇨"] and reaction.message.id == message.id
        
        reaction, user = await self.bot.wait_for("reaction_add", timeout=15.0, check=check)
        await message.remove_reaction(reaction, user)
        crime = crime_a
        if str(reaction.emoji) == "🇧":
            crime = crime_b
        elif str(reaction.emoji) == "🇨":
            crime = crime_c
        embed = discord.Embed(title=f"Error")
        if crime == "Murder":
            messages = [
                        f"You have successfully murdered an innocent pedestrian and stole `{risk:,}`$",
                        f"You have killed a nearby pedestrian, but you were caught and fined `{risk:,}`$"]
            embed.title=f"{context.author.name} committed murder"
        elif crime == "Pick Pocket":
            messages = [f"You have successfully pick pocketed `{risk:,}`$ from a stranger!", 
                        f"You were caught and fined `{risk:,}`$"]
            embed.title=f"{context.author.name} committed pick pocket"
        elif crime == "Graffiti":
            messages = [
                f"You have successfully vandalized a nearby building and were given `{risk:,}`$ by a kind stranger",
                f"You have vandalized a nearby building, but you were caught and fined `{risk:,}`$"]
            embed.title=f"{context.author.name} committed vandalism"
        elif crime == "Fraud":
            messages = [f"You have successfully lied to an old women and stole`{risk:,}`$",
            f"You accidentally called the police and were fined `{risk:,}`$"]
            embed.title=f"{context.author.name} committed fraud"
        elif crime == "Arson":
            messages = [
                        f"You have successfully burned down a nearby building and escaped with `{risk:,}$`", 
                        f"You burned down a nearby building, but you were caught and fined `{risk:,}`$"]
            embed.title=f"{context.author.name} committed arson"
        elif crime == "Sell meth":
            messages = [
                        f"You have successfully sold meth to Tuco Salamanca and earned `{round((risk*methamt)*purity/2):,}$`",
                        f"You have successfully sold meth to Gus Fring and earned `{round((risk*methamt)*purity/2):,}$`",
                        f"Tuco Salamanca beated you up and stole {risk:,}$ from you, and then he ran away with the meth",
                        f"Gus Fring stole {risk:,}$ from you, and then he ran away with the meth"]
            embed.title=f"{context.author.name} sold meth"
            users[str(user.id)]["bag"][index]["amount"] = 0
        set_message = random.choice(messages)

        if "succ" in set_message:
            if crime == "Sell meth":
                users[str(user.id)]["wallet"] += round((risk*methamt)*purity/4)
            else:
                users[str(user.id)]["wallet"] += risk*methamt*4
            embed.color = discord.Color.green()
            embed.add_field(name=set_message, value="")
        else:
            users[str(user.id)]["wallet"] -= round(risk*users[str(user.id)]["multiplier"])
            embed.color=discord.Color.red()
            embed.add_field(name=set_message, value="")

        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)
        await message.edit(embed=embed)

    @commands.command(name="rob")
    @commands.cooldown(1, 3, BucketType.user)
    async def rob(self, context, member: discord.Member):
        """
        Tries robbing a member
        """

        await openaccount(context.author)
        await openaccount(member)
        bal = await ub(member)
        bal2 = await ub(context.author)
        if bal[0] < 100 or member == context.author:
            await context.reply(f"Not worth it man", mention_author=False)
            return
        elif bal2[0] < 1000:
            await context.reply(
                f"You must have 1000$ in order to rob someone", mention_author=False
            )
            return

        users = await getbankdata()
        user = context.author
        index = 0

        breakchance = random.randint(0, 100)
        try:
            for thing in users[str(member.id)]["bag"]:
                n = thing["item"]
                if n == "padlock" and thing["amount"] > 0:
                    index += 1
                    if breakchance < 80:
                        await context.reply(
                            f"You tried robbing {member.name}, but they've got a lock on their wallet, and you couldn't rob em",
                            mention_author=False,
                        )
                        return
                    else:
                        e = users[str(user.id)]["bag"][index]["amount"]
                        users[str(user.id)]["bag"][index]["amount"] -= 1
                        with open("currency.json", "w") as f:
                            json.dump(users, f)
                        if e == 0:
                            await context.reply(
                                f"You have just broke every padlock on {member.name}'s wallet!",
                                mention_author=False,
                            )
                        else:
                            await context.reply(
                                f"You have just broke a padlock on {member.name}'s wallet, only {e} more to go!",
                                mention_author=False,
                            )
                        return
        except:
            index = 1

        earn = random.randint(0, bal[0])
        earn2 = random.randint(0, bal2[0])
        chance = random.randint(0, 100)

        if chance > 95:
            earn = bal[0]

        if chance > 60:
            users[str(member.id)]["wallet"] -= earn
            users[str(user.id)]["wallet"] += earn
            if earn == bal[0]:
                await context.reply(
                    f"You have robbed everything from {member.name}",
                    mention_author=False,
                )
            else:
                await context.reply(
                    f"You have robbed only {earn:,}$ from {member.name}",
                    mention_author=False,
                )
        else:
            users[str(member.id)]["wallet"] += earn2
            users[str(user.id)]["wallet"] -= earn2
            await context.reply(
                f"You got caught by {member.name}, and you lost {earn2:,}$",
                mention_author=False,
            )

        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)

    @commands.command(name="hack")
    @commands.cooldown(1, 3, BucketType.user)
    async def hack(self, context, member: discord.Member):
        """
        Try hacking into the cryptowallet of a member
        """

        await openaccount(context.author)
        await openaccount(member)
        bal = await ub(member)
        bal2 = await ub(context.author)
        breakchance = random.randint(0, 100)
        try:
            for thing in users[str(member.id)]["bag"]:
                n = thing["item"]
                if n == "firewall" and thing["amount"] > 0:
                    index += 1
                    if breakchance < 80:
                        await context.reply(
                            f"You tried hacking {member.name}, but they've got a firewall on their cryptowallet, and you couldn't hack em",
                            mention_author=False,
                        )
                        return
                    else:
                        val = users[str(user.id)]["bag"][index]["amount"]
                        users[str(user.id)]["bag"][index]["amount"] -= 1
                        with open("currency.json", "w") as f:
                            json.dump(users, f)
                        if val == 0:
                            await context.reply(
                                f"You have just broke every firewall on {member.name}'s cryptowallet!",
                                mention_author=False,
                            )
                        else:
                            await context.reply(
                                f"You have just broke a firewall on {member.name}'s cryptowallet, only {val} more to go!",
                                mention_author=False,
                            )
                        return
        except:
            index = 1

        if bal[2] < 1 or member == context.author:
            await context.reply(f"Not worth it man", mention_author=False)
            return
        elif bal2[2] < 1:
            await context.reply(
                f"You must have a bitcoin in order to hack someone",
                mention_author=False,
            )
            return

        users = await getbankdata()
        user = context.author
        earn = random.randint(0, bal[0])
        chance = random.randint(0, 100)

        if chance > 60:
            users[str(member.id)]["bitcoin"] -= earn
            users[str(user.id)]["bitcoin"] += earn
            if earn == bal[2]:
                await context.reply(
                    f"You have hacked every bitcoin from {member.name}'s cryptowallet 🎉",
                    mention_author=False,
                )
            else:
                await context.reply(
                    f"You have only hacked {earn}₿ from {member.name}'s cryptowallet 🍀",
                    mention_author=False,
                )
        else:
            users[str(member.id)]["bitcoin"] += bal2[2]
            users[str(user.id)]["bitcoin"] = 0
            await context.reply(
                f"You got caught by the cryptowallet admin, and you gave all your bicoin to {member.name} :cry:",
                mention_author=False,
            )

        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)

    @commands.command(name="bankrob")
    @commands.cooldown(1, 3, BucketType.user)
    async def robbank(self, context, member: discord.Member):
        """
        Tries robbing a member's bank
        """

        await openaccount(context.author)
        await openaccount(member)
        bal = await ub(member)
        bal2 = await ub(context.author)
        if bal[1] < 5000 or member.display_name == context.author.display_name:
            await context.reply(f"Not worth it man", mention_author=False)
            return
        if bal2[0] < 5000:
            await context.reply(f"You must have 5000$ in order to rob someone's bank", mention_author=False)
            return

        users = await getbankdata()
        user = context.author
        earn = random.randint(0, bal[1])
        earn2 = random.randint(0, bal2[0])
        breakchance = random.randint(0, 100)
        chance = random.randint(0, 100)

        try:
            for thing in users[str(member.id)]["bag"]:
                n = thing["item"]
                if n == "hacker" and thing["amount"] > 0:
                    index += 1
                    if breakchance < 80:
                        await context.reply(
                            f"You tried robbing {member.name}'s bank but they've got a hacker, and you couldn't rob their bank",
                            mention_author=False,
                        )
                        return
                    else:
                        users[str(user.id)]["bag"][index]["amount"] -= 1
                        with open("currency.json", "w") as f:
                            json.dump(users, f)
                        await context.reply(
                            f"You have just killed every hacker on {member.name}'s bank!",
                            mention_author=False,
                        )
                        return
        except:
            index = 1

        if chance > 60:
            users[str(member.id)]["bank"] -= earn
            users[str(user.id)]["wallet"] += earn
            if earn == bal[0]:
                await context.reply(
                    f"You have robbed everything from {member.name}'s bank",
                    mention_author=False,
                )
            else:
                await context.reply(
                    f"You have robbed only {earn:,}$ from {member.name}'s bank",
                    mention_author=False,
                )
        else:
            users[str(member.id)]["wallet"] += earn2
            users[str(user.id)]["wallet"] -= earn2
            await context.reply(
                f"You got caught by {member.name}, and you lost {earn:,}$",
                mention_author=False,
            )

        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)

    @commands.command(aliases=["pay"])
    @commands.cooldown(1, 3, BucketType.user)
    async def send(
        self, context, member: discord.Member, amount, bank="no"
    ):
        """
        Send an amount of money to a member
        """

        await openaccount(context.author)
        await openaccount(member)
        char = "wallet"
        tu = 0
        if not bank=="no":
            char = "bank"
            tu = 1
        bal = await ub(context.author)

        if member == context.author:
            await context.reply(
                f"You can't send money to yourself", mention_author=False
            )
            return

        if amount == "all":
            amount = bal[tu]
        elif amount == "half":
            amount = round(bal[tu] / 2)
        
        amount = int(amount)
        if amount > bal[tu]:
            await context.reply(
                    f"You don't have {amount:,}$ in your {char}", mention_author=False
                )
            return
        elif amount < 1:
            await context.reply(
                    f"The amount you want to send must be positive",
                    mention_author=False,
                )
            return
        elif amount == None:
            await context.reply(
                    f"The amount you want to send must be valid",
                    mention_author=False,
                )
            return

        users = await getbankdata()
        user = context.author
        earn = amount
        users[str(member.id)]["wallet"] += earn

        if earn == bal[tu]:
            users[str(user.id)][char] = 0

            await context.reply(
                f"You have successfuly gave all your money to {member.name}",
                mention_author=False,
            )
        else:
            users[str(char)][char] -= amount
            await context.reply(
                f"You have successfuly gave {earn:,}$ to {member.name}",
                mention_author=False,
            )

        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)

    @commands.command(name="withdraw")
    @commands.cooldown(1, 3, BucketType.user)
    async def withdrawbank(self, context, amount):
        """
        Withdraw an amount of money from your bank
        """

        await openaccount(context.author)
        bal = await ub(context.author)
        users = await getbankdata()
        user = context.author
        hasbank = 0
        for item in users[str(user.id)]["bag"]:
            if item["item"] == "bank":
                hasbank = 1
                break

        if hasbank == 0:
            await context.reply(
                f"You must have a bank in order to withdraw",
                mention_author=False,
            )
            return

        if amount == "all":
            amount = bal[1]
        elif amount == "half":
            amount = round(bal[1] / 2)
        else:
            amount = int(amount)
            if amount > bal[1]:
                await context.reply(
                    f"You don't have {amount:,}$ in your bank", mention_author=False
                )
                return
            elif amount < 0:
                await context.reply(
                    f"The amount you want to withdraw must be positive",
                    mention_author=False,
                )
                return
            elif amount == None:
                await context.reply(
                    f"The amount you want to withdraw must be valid",
                    mention_author=False,
                )
                return
            
        users[str(user.id)]["wallet"] += amount
        users[str(user.id)]["bank"] -= amount
        if amount == bal[1]:
            await context.reply(
                f"You have successfully withdrew everything from your bank",
                mention_author=False,
            )
        elif amount == round(bal[1] / 2):
            await context.reply(
                f"You have successfully withdrew half the amount you have from your bank",
                mention_author=False,
            )
        else:
            await context.reply(
                f"You have successfully withdrew {amount:,}$ from your bank",
                mention_author=False,
            )

        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)

    @commands.command(name="exchange")
    @commands.cooldown(1, 3, BucketType.user)
    async def exchange(self, context, amount):
        """
        Exchange your crypto into cash
        """

        message = await context.reply("Choose which crypto you want to exchange from\n🇦 Bitcoin\n🇧 Ethereum",mention_author=False)
        await message.add_reaction("🇦")
        await message.add_reaction("🇧")

        def check(reaction, user):
            return user == context.author and str(reaction.emoji) in ["🇦", "🇧", "🇨"] and reaction.message.id == message.id
        reaction, user = await self.bot.wait_for("reaction_add", timeout=15.0, check=check)

        tu = 2
        if str(reaction.emoji) == "🇦":
            char = "bitcoin"
            charn = "bitcoin"
        else:
            tu = 3
            char = "eth"
            charn = "ethereum"
        await openaccount(context.author)
        bal = await ub(context.author)
        amt = bal[tu]

        if amount == "all":
            amount = bal[tu]
        elif amount == "half":
            amount = round(bal[tu]/2)

        amount = int(amount)
        if amount > amt:
            await context.reply(
                    f"You don't have {amount} {charn}", mention_author=False
                )
            return
        elif amount < 0:
            await context.reply(
                    f"The amount you want to exchange must be positive",
                    mention_author=False,
                )
            return
        elif amount == None:
            await context.reply(
                    f"The amount you want to exchange must be valid",
                    mention_author=False,
                )
            return

        users = await getbankdata()
        users[str(user.id)][char] -= amount
        users[str(user.id)]["wallet"] += round(crypto[char]["value"]*amount)
        with open("currency.json", "w") as f:
           json.dump(users, f, indent=4)

        if amount == amt:
            await context.reply(
                f"You have successfully exchanged all your {charn} into cash",
                mention_author=False,
            )
        else:
            await context.reply(
                f"You have successfully exchanged {amount} {charn} into cash",
                mention_author=False,
            )

    @commands.command(name="deposit")
    @commands.cooldown(1, 3, BucketType.user)
    async def deposit(self, context, amount):
        """
        Deposit an amount of money into the bank.
        """

        users = await getbankdata()
        user = context.author
        hasbank = 0
        await openaccount(context.author)
        bal = await ub(context.author)

        for item in users[str(user.id)]["bag"]:
            name = item["item"]

            if name == "bank":
                hasbank = 1
                break

        if hasbank == 0:
            await context.reply(
                f"You must have a bank in order to deposit",
                mention_author=False,
            )
            return

        if amount == "all":
            amount = bal[0]
        elif amount == "half":
            amount = round(bal[0] / 2)
        else:
            amount = int(amount)
            if amount > bal[0]:
                await context.reply(
                    f"You don't have that much money! Your current amount is {bal[0]:,}$",
                    mention_author=False,
                )
                return
            if amount < 0:
                await context.reply(
                    f"The amount you want to deposit must be positive",
                    mention_author=False,
                )
                return
            if amount == None:
                await context.reply(
                    f"The amount you want to deposit must be valid",
                    mention_author=False,
                )
                return

        earn = amount
        to = 500000 * users[str(user.id)]["multiplier"]

        if (users[str(user.id)]["bank"] + amount) > to:
            earn = to
            await context.reply(
                f"You can only deposit {to:,}$ into your bank", mention_author=False
            )
            return

        users[str(user.id)]["wallet"] -= earn
        users[str(user.id)]["bank"] += earn
        if earn == bal[0]:
            await context.reply(
                f"You have successfully deposited all your money into the bank",
                mention_author=False,
            )
        elif earn == round(bal[0] / 2):
            await context.reply(
                f"You have successfully deposited half your money into the bank",
                mention_author=False,
            )
        else:
            await context.reply(
                f"You have successfully deposited {earn:,}$ into your bank",
                mention_author=False,
            )

        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)

    @commands.command(aliases=["bal", "wallet"])
    @commands.cooldown(1, 3, BucketType.user)
    async def balance(self, context, member: discord.Member = None):
        """
        Displays the balance of a member
        """
        if not member:
            member = context.author
        await openaccount(member)

        users = await getbankdata()
        user = member

        wallet_amount = users[str(user.id)]["wallet"]
        bank_amount = users[str(user.id)]["bank"]
        bit_amount = users[str(user.id)]["bitcoin"]
        eth_amount = users[str(user.id)]["eth"]
        a = users[str(user.id)]["description"]
        em = discord.Embed(
            title=f"{member.name}'s balance {a}", color=discord.Color.green()
        )
        em.add_field(name="Wallet", value=f"{wallet_amount:,}$")
        em.add_field(name="Bank", value=f"{bank_amount:,}$")

        if users[str(user.id)]["cryptowallet"] == "yes":
            em.add_field(name="Bitcoin", value=f"{bit_amount}₿")
            em.add_field(name="Ethereum", value=f"{eth_amount}Ξ")
        await context.reply(embed=em, mention_author=False)

    @commands.command(aliases=["stat"])
    @commands.cooldown(1, 3, BucketType.user)
    async def stats(self, context, member: discord.Member = None):
        """
        Displays the statistics of a member
        """
        if not member:
            member = context.author
        await openaccount(member)

        users = await getbankdata()
        user = member

        wallet_amount = users[str(user.id)]["wallet"]
        bank_amount = users[str(user.id)]["bank"]
        mult_amount = users[str(user.id)]["multiplier"]
        bit_amount = users[str(user.id)]["bitcoin"]
        eth_amount = users[str(user.id)]["eth"]
        badges = ""

        if context.guild.owner == member:
            badges += ":crown:"
        
        badges += users[str(user.id)]["badge"]

        desc = users[str(user.id)]["description"]
        joined_at = user.joined_at.strftime("%b %d, %Y, %T")
        created_at = user.created_at.strftime("%b %d, %Y, %T")
        em = discord.Embed(
            title=f"{member.name}'s stats {desc}", color=discord.Color.green()
        )

        a = 0
        for item in users[str(user.id)]["bag"]:
            name = item["item"]
            amount = item["amount"]

            if amount > 0 and (
                name == "house"
                or name == "hut"
                or name == "luxurymansion"
                or name == "exoticmansion"
            ):
                a += amount

        em.add_field(name="Wallet balance", value=f"{wallet_amount:,}$")
        em.add_field(name="Bank balance", value=f"{bank_amount:,}$")
        if users[str(user.id)]["cryptowallet"] == "yes":
            em.add_field(name="Bitcoin balance", value=f"{bit_amount}₿")
            em.add_field(name="ETH balance", value=f"{eth_amount}Ξ")

        if mult_amount != 1:
            em.add_field(name="Multiplier", value=f"{mult_amount}", inline=False)

        if a > 0:
            em.add_field(name="Properties", value=f"{a}", inline=False)

        em.add_field(name="Join date", value=f"{joined_at}", inline=False)
        em.add_field(name="Creation date", value=f"{created_at}", inline=False)
        if badges != "":
            em.add_field(name="Badges", value=f"{badges}", inline=False)

        if not "<:swastika:1109944785021710527>" in users[str(member.id)]["badge"]:
            if member.avatar == None:
                em.set_thumbnail(
                    url="https://wompampsupport.azureedge.net/fetchimage?siteId=7575&v=2&jpgQuality=100&width=700&url=https%3A%2F%2Fi.kym-cdn.com%2Fphotos%2Fimages%2Fnewsfeed%2F002%2F320%2F268%2Fa53.jpg"
                )
            else:
                em.set_thumbnail(url=member.avatar)
        else:
            em.set_thumbnail(
                url=f"https://cdn.discordapp.com/emojis/1109944785021710527.webp?size=96&quality=lossless"
            )

        await context.reply(embed=em, mention_author=False)

    @commands.command(name="beg")
    @commands.cooldown(1, 3, BucketType.user)
    async def beg(self, context):
        """
        Beg people on streets for money
        """
        await openaccount(context.author)

        users = await getbankdata()
        user = context.author
        earn = random.randint(10, 100) * users[str(user.id)]["multiplier"]
        earndiv = random.randint(0, 1)
        earnr = random.randint(0, 100)

        if earnr > 60:
            if earndiv == 1 and earn != 0:
                earn = earn / 2

            users[str(user.id)]["wallet"] += round(earn)
            await context.reply(
                f"Take some money, little beggar! You have got {round(earn):,}$ 🍫",
                mention_author=False,
            )
        else:
            await context.reply(
                f"You have found nobody to beg to, sucks to be you",
                mention_author=False,
            )

        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)

    @commands.command(aliases=["lb", "baltop", "leader", "rich", "richest"])
    @commands.cooldown(1, 3, BucketType.user)
    async def leaderboard(self, context):
        """
        Displays the leaderboard
        """

        users = await getbankdata()
        leader_board = {}
        total = []
        await opencrypto("bitcoin", 1)
        await opencrypto("eth", 1)
        xmr = await getcrypto()

        for user in users:
            name = int(user)
            total_amount = (
                users[user]["wallet"]
                + users[user]["bank"]
                + (users[user]["bitcoin"] * xmr["bitcoin"]["value"])
                + (users[user]["eth"] * xmr["eth"]["value"])
            )
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total, reverse=True)

        em = discord.Embed(
            title=f"Top 10 Richest People", description="", color=0x42F56C
        )
        index = 1

        for amount in total:
            id = leader_board[amount]
            name = await context.author.guild.fetch_member(id)
            if amount == 0:
                continue

            if index == 1:
                char = f"🥇 {name}"
            elif index == 2:
                char = f"🥈 {name}"
            elif index == 3:
                char = f"🥉 {name}"
            else:
                char = f" {index} {name}"
                
            em.add_field(name=char, value=f"{amount:,}$", inline=False)

            if index == 10:
                break
            else:
                index += 1
        em.title=f"Top {index-1} richest members"

        await context.reply(embed=em, mention_author=False)

    @commands.command(name="shop")
    @commands.cooldown(1, 3, BucketType.user)
    async def shop(self, context):
        """
        Displays the items you can buy
        """
        await context.reply("", view=Shop())

    @commands.command(name="cookmeth")
    async def cookmeth(self, context):
        """
        Create meth using a meth lab
        """
        await openaccount(context.author)
        users = await getbankdata()
        user = context.author

        hasmeth = 0
        pseudo = 0
        phosphor = 0
        ha = 0
        sh = 0
        hc = 0
        index = 0
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == "meth lab":
                hasmeth = 1
            
            if n == "pseudoephedrine":
                pseudo = 1
                users[str(user.id)]["bag"][index]["amount"] -= 1
            if n == "red phosphorus":
                users[str(user.id)]["bag"][index]["amount"] -= 1
                phosphor = 1
            if n == "hydriodic acid":
                users[str(user.id)]["bag"][index]["amount"] -= 1
                ha = 1
            if n == "sodium hydroxide":
                users[str(user.id)]["bag"][index]["amount"] -= 1
                sh = 1
            if n == "hydrogen chloride":
                users[str(user.id)]["bag"][index]["amount"] -= 1
                hc = 1
            index += 1

        if hasmeth == 0:
            await context.reply(f"You must have a meth lab in order to cook meth", mention_author=False)
            return
    
        if pseudo == 0:
            await context.reply(f"You must have a gram of Pseudoephedrine in order to cook meth", mention_author=False)
            return
        elif phosphor == 0:
            await context.reply(f"You must have a gram of Red Phosphorus in order to cook meth", mention_author=False)
            return
        elif ha == 0:
            await context.reply(f"You must have a gram of Hydriodic Acid in order to cook meth", mention_author=False)
            return
        elif sh == 0:
            await context.reply(f"You must have a gram of Sodium Hydroxide in order to cook meth", mention_author=False)
            return
        elif hc == 0:
            await context.reply(f"You must have a gram of Hydrogen Chloride in order to cook meth", mention_author=False)
            return

        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == "meth":
                    users[str(user.id)]["bag"][index]["amount"] += 1
                    t = 1
                    break
                index += 1
            if t == None:
                obj = {"item": "meth", "amount": 1, "icon": "<:meth:1110538413360295986>", "purity": users[str(user.id)]["multiplier"]}
                users[str(user.id)]["bag"].append(obj)
        except:
            obj = {"item": "meth", "amount": 1, "icon": "<:meth:1110538413360295986>", "purity": users[str(user.id)]["multiplier"]}
            users[str(user.id)]["bag"] = [obj]

        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)

        await context.reply(f"You have just cooked a gram of meth using your meth lab", mention_author=False)

    @commands.command(name="buy")
    @commands.cooldown(1, 3, BucketType.user)
    async def buy(self, context, item, item2="", item3="", amount=1):
        """
        Buy an item from the shop
        """
        toamount = amount

        if toamount < 1:
                await context.reply(
                    f"You can't buy a negative amount of {item}", mention_author=False
                )
                return

        if item2 != "":
            if item2.isnumeric() or item2 == "-1":
                toamount = int(item2)
            elif type(item2) == str:
                item += f" {item2}"

        if item3 != "":
            if item3.isnumeric() or item3 == "-1":
                toamount = int(item3)
            elif type(item3) == str:
                item += f" {item3}"

        item = item.lower()
        if item == "eth":
            item = "ethereum"
        elif item == "btc":
            item = "bitcoin"

        user = context.author
        users = await getbankdata()
        ab = 0
        abb = 0
        ae = 1
        ind = 0
        for iteme in users[str(user.id)]["bag"]:
            aname = iteme["item"]
            aamount = iteme["amount"]
            if aname == "bitcoin" or aname == "ethereum" or aname == "monero":
                continue

            if aname == "house" or aname == "hut":
                ae += aamount
            elif aname == "exoticmansion":
                ae += aamount * 10
            elif aname == "luxurymansion":
                ae += aamount * 3
            elif aname == "padlock":
                ab += aamount
            elif aname == "firewall":
                abb += aamount
            ind += aamount

        shop = mainshop
        n = "wallet"
        for itemb in btcshop:
            nameb = itemb["name"].lower()
            if nameb == item:
                shop = btcshop
                n = "bitcoin"
                break
        for iteme in ethshop:
            namee = iteme["name"].lower()
            if namee == item:
                shop = ethshop
                n = "eth"
                break
        for itemm in blackmarket:
            namem = itemm["name"].lower()
            if namem == item:
                shop = blackmarket
                break

        await openaccount(context.author)
        res = await buy_item(context, context.author, item, toamount, shop, n)

        to = 1000 * ae
        if (ind + toamount) > to and await notcrypto(item):
            await context.reply(
                f"You can't have more than {to} items in your bag", mention_author=False
            )
            return

        if item == "padlock" and ab + toamount > 5:
            await context.reply(
                f"You can't have more than 5 padlocks", mention_author=False
            )
            return

        if item == "firewall" and abb + toamount > 5:
            await context.reply(
                f"You can't have more than 5 firewalls", mention_author=False
            )
            return

        if not res[0]:
            if res[1] == 1:
                await context.reply(f"{item} is not valid", mention_author=False)
                return
            if res[1] == 2:
                if toamount == 1:
                    if shop == btcshop:
                        await context.reply(
                            f"You don't have enough bitcoin to buy a {item}",
                            mention_author=False,
                        )
                    elif shop == ethshop:
                        await context.reply(
                            f"You don't have enough ethereum to buy a {item}",
                            mention_author=False,
                        )
                    else:
                        await context.reply(
                            f"You don't have enough money to buy a {item}",
                            mention_author=False,
                        )
                else:
                    if shop == btcshop:
                        await context.reply(
                            f"You don't have enough bitcoin to buy {toamount} {item}s",
                            mention_author=False,
                        )
                    elif shop == ethshop:
                        await context.reply(
                            f"You don't have enough ethereum to buy {toamount} {item}",
                            mention_author=False,
                        )
                    else:
                        await context.reply(
                            f"You don't have enough money to buy {toamount} {item}",
                            mention_author=False,
                        )
                return
            if res[1] == 3:
                await context.reply(f"You can't buy {item}", mention_author=False)
                return
            if res[1] == 5:
                await context.reply(
                    f"You don't own a cryptowallet", mention_author=False
                )
                return
            if res[1] == 6:
                await context.reply(
                    f"You already own a cryptowallet", mention_author=False
                )
                return

        msg = ":poop:"
        
        if toamount == 1:
            if item == "oil":
                msg = "You have just bought a kilo of oil"
            elif item == "pseudoephedrine" or item == "red phosphorus" or item == "hydriodic acid" or item == "sodium hydroxide" or item == "hydrogen chloride":
                msg = f"You have just bought a gram of {item}"
            else:
                msg = f"You have just bought a {item}"
        else:
            if item == "oil":
                msg = f"You have just bought {toamount} kilos of oil"
            elif item == "pseudoephedrine" or item == "red phosphorus" or item == "hydriodic acid" or item == "sodium hydroxide" or item == "hydrogen chloride":
                msg = f"You have just bought {toamount} grams of {item}"
            elif await iscrypto(item):
                msg = f"You have just bought {toamount} {item}"
            else:
                msg = f"You have just bought {toamount} {item}s"

        await context.reply(msg, mention_author=False)
        
    @commands.command(name="sell")
    @commands.cooldown(1, 3, BucketType.user)
    async def sell(self, context, item, item2="", item3="", amount=1):
        """
        Sell an item
        """
        toamount = amount

        if item2 != "":
            if item2.isnumeric() or item2 == "-1":
                toamount = int(item2)
            elif type(item2) == str:
                item += f" {item2}"

        if item3 != "":
            if item3.isnumeric() or item3 == "-1":
                toamount = int(item3)
            elif type(item3) == str:
                item += f" {item3}"

        await openaccount(context.author)
        res = await sell_item(context.author, item, toamount)

        if toamount < -1:
            await context.reply(f"You can't sell {toamount} {item}s", mention_author=False)
            return

        if not res[0]:
            if res[1] == 1:
                await context.reply(f"{item} is not valid", mention_author=False)
                return
            if res[1] == 2:
                await context.reply(
                    f"You don't have {toamount} {item}s in your bag", mention_author=False
                )
                return
            if res[1] == 3:
                await context.reply(
                    f"You don't have {item} in your bag", mention_author=False
                )
                return
            if res[1] == 4:
                await context.reply(f"You can't sell {item}", mention_author=False)
                return

        msg = ":poop:"
        if amount == 1:
            if item == "oil":
                msg = "You have just sold a kilo of oil"
            elif item == "meth" or item == "cocaine":
                msg = f"You have just sold a gram of {item}"
            else:
                msg = f"You have just sold a {item}"
        else:
            if item == "oil":
                msg = f"You have just sold {toamount} kilos of oil"
            elif item == "meth" or item == "cocaine":
                msg = f"You have just sold {toamount} grams of {item}"
            elif await iscrypto(item):
                msg = f"You have just sold {toamount} {item}"
            else:
                msg = f"You have just sold {toamount} {item}s"

        await context.reply(msg, mention_author=False)

    @commands.command(aliases=["bag"])
    @commands.cooldown(1, 3, BucketType.user)
    async def inventory(self, context, member: discord.Member = None):
        """
        Displays the inventory of a member
        """
        if not member:
            member = context.author
        await openaccount(member)

        users = await getbankdata()
        user = member

        bag = users[str(user.id)]["bag"]

        em = discord.Embed(
            title=f"{member.name}'s inventory", color=discord.Color.green()
        )
        for item in bag:
            name = item["item"]
            amount = item["amount"]
            if amount < 1 or name == "hut" or name == "house" or name == "bank" or name == "exotic mansion" or name == "luxury mansion":
                continue

            ico = item["icon"]

            if name == "coems":
                em.add_field(name=f"{name} {ico}", value="", inline=False)
                continue
            elif name == "oil":
                if amount == 1:
                    em.add_field(name=f"a kilo of oil {ico}", value="", inline=False)
                else:
                    em.add_field(name=f"{amount} kilos of oil {ico}", value="", inline=False)
                continue
            elif name == "meth" or name == "redphosphorus" or name == "pseudoephedrine" or name == "hydriodicacid" or name == "sodiumhydroxide":
                if amount == 1:
                    em.add_field(name=f"a gram of {name} {ico}", value="", inline=False)
                else:
                    em.add_field(name=f"{amount} grams of {name} {ico}", value="", inline=False)
                continue

            if amount == 1:
                name = "a " + name
            else:
                name = str(amount) + " " + name + "s"

            em.add_field(name=f"{name} {ico}", value="", inline=False)

        em.set_footer(text="Use .shop in order to see the current items available")
        if not "<:swastika:1109944785021710527>" in users[str(user.id)]["badge"]:
            em.set_thumbnail(url=member.avatar)
        else:
            em.set_thumbnail(
                url=f"https://cdn.discordapp.com/emojis/1109944785021710527.webp?size=96&quality=lossless"
            )

        await context.reply(embed=em, mention_author=False)

    @commands.command(name="daily")
    @commands.cooldown(1, 86400, BucketType.user)
    async def daily(self, context):
        """
        Claim your daily amount of money
        """
        await openaccount(context.author)
        users = await getbankdata()
        user = context.author
        to = 50000 * users[str(user.id)]["multiplier"]
        users[str(user.id)]["wallet"] += to
        await context.reply(
            f"You have just claimed your daily {to}$", mention_author=False
        )
        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)

    @commands.command(name="multiply")
    @commands.cooldown(1, 3, BucketType.user)
    async def mult(self, context):
        """
        Makes a deal with someone to multiply your money
        """
        await openaccount(context.author)

        users = await getbankdata()
        user = context.author
        mult = users[str(user.id)]["wallet"]

        if users[str(user.id)]["wallet"] == 0:
            await context.reply("You have no money to multiply", mention_author=False)

        earnings = (random.randint(1, 3) * mult) * users[str(user.id)]["multiplier"]
        earn = random.randint(0, 1)

        if earn == 1:
            users[str(user.id)]["wallet"] += earnings
            await context.reply(
                f"You have successfully multiplied your money! You now have {(mult + earnings):,}$",
                mention_author=False,
            )
        elif earn == 0:
            users[str(user.id)]["wallet"] = 0
            await context.reply(
                f"You have got scammed by the dealer! You now have 0$",
                mention_author=False,
            )

        with open("currency.json", "w") as f:
            json.dump(users, f, indent=4)

    @commands.command(name="dig")
    @commands.cooldown(1, 3, BucketType.user)
    async def dig(self, context):
        """
        Use your shovel.
        """
        await openaccount(context.author)

        users = await getbankdata()
        user = context.author
        earnings = random.randint(100, 300) * users[str(user.id)]["multiplier"]
        earn = random.randint(0, 100)
        earndiv = random.randint(1, 5)
        bag = users[str(user.id)]["bag"]

        index = 0
        for item in bag:
            name = item["item"]
            amount = item["amount"]
            if name == "shovel" and amount > 0:
                if earn > 0 and earn < 50:
                    if earndiv == 1:
                        try:
                            index = 0
                            t = None
                            for thing in users[str(user.id)]["bag"]:
                                n = thing["item"]
                                if n == "worm":
                                    users[str(user.id)]["bag"][index]["amount"] += 1
                                    t = 1
                                    break
                                index += 1
                            if t == None:
                                obj = {"item": "worm", "amount": 1, "icon": ":worm:"}
                                users[str(user.id)]["bag"].append(obj)
                        except:
                            obj = {"item": "worm", "amount": 1, "icon": ":worm:"}
                            users[str(user.id)]["bag"] = [obj]
                        await context.reply(
                            f"You have found a worm underground", mention_author=False
                        )
                        if not ":worm:" in users[str(user.id)]["badge"]:
                            users[str(user.id)]["badge"] += ":worm:"
                    elif earndiv == 2:
                        users[str(user.id)]["wallet"] += earnings
                        await context.reply(
                            f"You have found {earnings}$ underground",
                            mention_author=False,
                        )
                    elif earndiv == 3:
                        try:
                            index = 0
                            t = None
                            for thing in users[str(user.id)]["bag"]:
                                n = thing["item"]
                                if n == "teddy bear":
                                    users[str(user.id)]["bag"][index]["amount"] += 1
                                    t = 1
                                    break
                                index += 1
                            if t == None:
                                obj = {"item": "teddy bear", "amount": 1, "icon": ":teddy_bear:"}
                                users[str(user.id)]["bag"].append(obj)
                        except:
                            obj = {"item": "teddy bear", "amount": 1, "icon": ":teddy_bear:"}
                            users[str(user.id)]["bag"] = [obj]
                        await context.reply(
                            f"You have found a buried teddy bear", mention_author=False
                        )
                        if not ":teddy_bear:" in users[str(user.id)]["badge"]:
                            users[str(user.id)]["badge"] += ":teddy_bear:"
                    elif earndiv == 4:
                        try:
                            index = 0
                            t = None
                            for thing in users[str(user.id)]["bag"]:
                                n = thing["item"]
                                if n == "roll of paper":
                                    users[str(user.id)]["bag"][index]["amount"] += 1
                                    t = 1
                                    break
                                index += 1
                            if t == None:
                                obj = {"item": "roll of paper", "amount": 1, "icon": ":roll_of_paper:"}
                                users[str(user.id)]["bag"].append(obj)
                        except:
                            obj = {"item": "roll of paper", "amount": 1, "icon": ":roll_of_paper:"}
                            users[str(user.id)]["bag"] = [obj]
                        await context.reply(
                            f"You have found a roll of paper deep underground",
                            mention_author=False,
                        )
                        if not ":roll_of_paper:" in users[str(user.id)]["badge"]:
                            users[str(user.id)]["badge"] += ":roll_of_paper:"
                    elif earndiv == 5:
                        try:
                            index = 0
                            t = None
                            for thing in users[str(user.id)]["bag"]:
                                n = thing["item"]
                                if n == "oil":
                                    users[str(user.id)]["bag"][index]["amount"] += 1
                                    t = 1
                                    break
                                index += 1
                            if t == None:
                                obj = {"item": "oil", "amount": 1, "icon": ":oil:"}
                                users[str(user.id)]["bag"].append(obj)
                        except:
                            obj = {"item": "oil", "amount": 1, "icon": ":oil:"}
                            users[str(user.id)]["bag"] = [obj]
                        await context.reply(
                            f"You have found a kilo of oil deep underground",
                            mention_author=False,
                        )
                        if not ":oil:" in users[str(user.id)]["badge"]:
                            users[str(user.id)]["badge"] += ":oil:"
                    elif earndiv == 6:
                        try:
                            index = 0
                            t = None
                            for thing in users[str(user.id)]["bag"]:
                                n = thing["item"]
                                if n == "newspaper":
                                    users[str(user.id)]["bag"][index]["amount"] += 1
                                    t = 1
                                    break
                                index += 1
                            if t == None:
                                obj = {"item": "newspaper", "amount": 1, "icon": ":newspaper:"}
                                users[str(user.id)]["bag"].append(obj)
                        except:
                            obj = {"item": "newspaper", "amount": 1, "icon": ":newspaper:"}
                            users[str(user.id)]["bag"] = [obj]
                        froma = [
                            1943,
                            1945,
                            1954,
                            1980,
                            2013,
                            2012,
                            1942,
                            1941,
                            1940,
                            1938,
                            1939,
                            1937,
                        ]
                        await context.reply(
                            f"You have found a buried newspaper from {random.choice(froma)} deep underground",
                            mention_author=False,
                        )
                        if not ":newspaper:" in users[str(user.id)]["badge"]:
                            users[str(user.id)]["badge"] += ":newspaper:"
                    with open("currency.json", "w") as f:
                        json.dump(users, f)
                elif earn > 50 and earn < 90:
                    await context.reply(
                        f"You have found nothing, sucks to be you", mention_author=False
                    )
                elif earn > 90:
                    users[str(user.id)]["bag"][index]["amount"] -= 1
                    await context.reply(
                        f"Your shovel broke, sucks to be you", mention_author=False
                    )
                    with open("currency.json", "w") as f:
                        json.dump(users, f)
                return
            index += 1

        await context.reply(f"You don't own a shovel", mention_author=False)

    @commands.command(name="fish")
    @commands.cooldown(1, 3, BucketType.user)
    async def fish(self, context):
        """
        Use your fishing pole.
        """
        await openaccount(context.author)

        users = await getbankdata()
        user = context.author
        earnings = random.randint(100, 300) * users[str(user.id)]["multiplier"]
        earn = random.randint(0, 100)
        earndiv = random.randint(1, 4)
        bag = users[str(user.id)]["bag"]
        index = 0
        for item in bag:
            name = item["item"]
            amount = item["amount"]
            if name == "fishing pole" and amount > 0:
                if earn > 0 and earn < 50:
                    if earndiv == 1:
                        try:
                            index = 0
                            t = None
                            for thing in users[str(user.id)]["bag"]:
                                n = thing["item"]
                                if n == "worm":
                                    users[str(user.id)]["bag"][index]["amount"] += 1
                                    t = 1
                                    break
                                index += 1
                            if t == None:
                                obj = {"item": "worm", "amount": 1, "icon": ":worm:"}
                                users[str(user.id)]["bag"].append(obj)
                        except:
                            obj = {"item": "worm", "amount": 1, "icon": ":worm:"}
                            users[str(user.id)]["bag"] = [obj]
                        await context.reply(
                            f"You have found a worm in the lake", mention_author=False
                        )
                        if not ":worm:" in users[str(user.id)]["badge"]:
                            users[str(user.id)]["badge"] += ":worm:"
                    elif earndiv == 2:
                        users[str(user.id)]["wallet"] += earnings
                        await context.reply(
                            f"You have found {earnings}$ floating on the lake",
                            mention_author=False,
                        )
                    elif earndiv == 3:
                        try:
                            index = 0
                            t = None
                            for thing in users[str(user.id)]["bag"]:
                                n = thing["item"]
                                if n == "teddy bear":
                                    users[str(user.id)]["bag"][index]["amount"] += 1
                                    t = 1
                                    break
                                index += 1
                            if t == None:
                                obj = {"item": "teddy bear", "amount": 1, "icon": ":teddy_bear:"}
                                users[str(user.id)]["bag"].append(obj)
                        except:
                            obj = {"item": "teddy bear", "amount": 1, "icon": ":teddy_bear:"}
                            users[str(user.id)]["bag"] = [obj]
                        await context.reply(
                            f"You have found a floating teddy bear on the lake",
                            mention_author=False,
                        )
                        if not ":teddy_bear:" in users[str(user.id)]["badge"]:
                            users[str(user.id)]["badge"] += ":teddy_bear:"
                    elif earndiv == 4:
                        try:
                            index = 0
                            t = None
                            for thing in users[str(user.id)]["bag"]:
                                n = thing["item"]
                                if n == "roll of paper":
                                    users[str(user.id)]["bag"][index]["amount"] += 1
                                    t = 1
                                    break
                                index += 1
                            if t == None:
                                obj = {"item": "roll of paper", "amount": 1, "icon": ":roll_of_paper:"}
                                users[str(user.id)]["bag"].append(obj)
                        except:
                            obj = {"item": "roll of paper", "amount": 1, "icon": ":roll_of_paper:"}
                            users[str(user.id)]["bag"] = [obj]
                        await context.reply(
                            f"You have found a roll of paper floating on the lake",
                            mention_author=False,
                        )
                        if not ":roll_of_paper:" in users[str(user.id)]["badge"]:
                            users[str(user.id)]["badge"] += ":roll_of_paper:"
                    with open("currency.json", "w") as f:
                        json.dump(users, f)
                elif earn > 50 and earn < 90:
                    await context.reply(
                        f"You have found nothing, sucks to be you", mention_author=False
                    )
                elif earn > 90:
                    users[str(user.id)]["bag"][index]["amount"] -= 1
                    await context.reply(
                        f"Your fishing pole broke, sucks to be you",
                        mention_author=False,
                    )
                    with open("currency.json", "w") as f:
                        json.dump(users, f)
                return
            index += 1

        await context.reply(f"You don't own a fishing pole", mention_author=False)

    @commands.group(name="company")
    @commands.cooldown(1, 3, BucketType.user)
    async def company(self, context):
        """
        Displays the company leaderboard
        """
        if context.invoked_subcommand is None:
            totalcomp = await getcompanies()
            leader_board = {}
            total = []
            for comp in totalcomp:
                total_amount = totalcomp[str(comp)]["net_worth"]
                leader_board[total_amount] = totalcomp[str(comp)]
                total.append(total_amount)

            total = sorted(total, reverse=True)

            em = discord.Embed(
            title=f"Top 10 Richest companies by net worth", description="", color=0x42F56C
        )
            index = 1

            for amount in total:
                named = leader_board[amount]["identity"]
                icon = leader_board[amount]["icon"]
                id_ = leader_board[amount]["owner"]
                namek = await context.author.guild.fetch_member(id_)
                if leader_board[amount]["net_worth"] < 1:
                    continue
                if not leader_board[amount]["icon"] == "":
                    named = f"{icon} {named}"
                if index == 1:
                    char = f"🥇 {named} | {namek}"
                elif index == 2:
                    char = f"🥈 {named} | {namek}"
                elif index == 3:
                    char = f"🥉 {named} | {namek}"
                else:
                    char = f"  {index} {named} | {namek}"
                
                em.add_field(name=char, value=f"{amount:,}$", inline=False)
                
                if index == 10:
                    break
                else:
                    index += 1
            em.title = f"Top {index-1} companies by net worth"
            em.set_footer(text=f"Use .company create <name> in order to create a company")
            await context.reply(embed=em, mention_author=False)

    @company.command(name="info")
    async def company_info(self, context, member: discord.Member=None):
        """
        Displays info of a company
        """
        mbr = member
        if member == None:
            mbr = context.author
        comps = await getcompanies()
        comp = ""
        net = 0
        upg = 0
        icon = ""
        rn = ""
        for comp in comps:
                if comps[str(comp)]["owner"] == mbr.id or mbr.id in comps[str(comp)]["employees"]:
                    rn = comps[str(comp)]["name"]
                    comp = comps[rn]["identity"]
                    net = comps[rn]["net_worth"]
                    upg = comps[rn]["upgrade"]
                    icon = comps[rn]["logo"]
                    break
        
        name = comp
        if not icon == "":
            name = f"{icon} {name}"
        
        if rn == "":
            await context.reply(f"{mbr.name} has no company", mention_author=False)
            return
        em = discord.Embed(
            title=f"{mbr.name}'s company info", description="", color=0x42F56C
        )

        em.add_field(name="Name", value=name, inline=False)
        em.add_field(name="Net worth", value=f"{net:,}", inline=False)
        em.add_field(name="Upgrades", value=upg, inline=False)
        await context.reply(embed=em, mention_author=False)

    @company.command(name="create")
    @commands.cooldown(1, 3, BucketType.user)
    async def comp_create(self, context, *, name):
        """
        Create a company
        """

        found = 0
        users = await getcompanies()
        for comp in users:
                if users[str(comp)]["name"].lower() == name.lower():
                    found = 1
                    break
                if users[str(comp)]["owner"] == context.author.id:
                    found = 2
                    break
                if context.author.id in users[str(comp)]["employees"]:
                    found = 3
                    break
        if found == 1:
            await context.reply(f"{name} is already taken", mention_author=False)
            return
        elif found == 2:
            await context.reply(f"You already own a company", mention_author=False)
            return
        elif found == 3:
            await context.reply(f"You are already an employee", mention_author=False)
            return
        elif len(name)>32:
            await context.reply(f"Your company name must be lower than 32 letters", mention_author=False)
            return

        await opencompany(name, context.author.id)
        await context.reply(f"Successfully created company {name}", mention_author=False)

    @company.command(name="invest")
    @commands.cooldown(1, 3, BucketType.user)
    async def comp_invest(self, context, amount: int=1):
        """
        Invest into your company
        """

        await openaccount(context.author)
        found = 0
        users = await getcompanies()
        for comp in users:
                if users[str(comp)]["owner"] == context.author.id or context.author.id in users[str(comp)]["employees"]:
                    found = 1
                    break
        
        if found == 0:
            await context.reply(f"You are not in a company", mention_author=False)
            return
        us = await getbankdata()
        if amount>us[str(context.author.id)]["wallet"]:
            await context.reply(f"You don't have that much money", mention_author=False)
            return
        if amount<1:
            await context.reply(f"The amount must be positive", mention_author=False)
            return
        
        a = int(round(amount/50))
        if a < 1:
            a = 1

        users[str(comp)]["net_worth"] += a*users[str(comp)]["upgrade"]
        us[str(context.author.id)]["wallet"] -= amount

        with open("currency.json", "w") as f:
            json.dump(us, f, indent=4)
        with open("company.json", "w") as f:
            json.dump(users, f, indent=4)
        await context.reply(f"You have successfully invested {amount:,}$ into your company", mention_author=False)

    @company.command(name="rename")
    @commands.cooldown(1, 3, BucketType.user)
    async def comp_rename(self, context, *, name):
        """
        Rename your company
        """

        found = 0
        rn = name
        users = await getcompanies()
        for comp in users:
                if users[str(comp)]["owner"] == context.author.id:
                    found = 1
                    break
                if users[str(comp)]["identity"]==rn:
                    found=2
                    break
        
        if found == 0:
            await context.reply(f"You don't own a company", mention_author=False)
            return
        elif found == 2:
            await context.reply(f"`{name}` already exists", mention_author=False)
            return
        elif len(name)>32:
            await context.reply(f"The name must be lower than 32 letters", mention_author=False)
            return
        
        users[str(comp)]["identity"]=name

        with open("company.json", "w") as f:
            json.dump(users, f, indent=4)
        await context.reply(f"You have successfully renamed your company to `{name}`", mention_author=False)

    @company.command(name="logo")
    @commands.cooldown(1, 3, BucketType.user)
    async def comp_logo(self, context, url):
        """
        Set a logo for your company
        """

        found = 0
        rn = url
        users = await getcompanies()
        for comp in users:
                if users[str(comp)]["owner"] == context.author.id:
                    found = 1
                    break
                if users[str(comp)]["identity"]==rn:
                    found=2
                    break
        
        if found == 0:
            await context.reply(f"You don't own a company", mention_author=False)
            return
        elif found == 2:
            await context.reply(f"A company already uses `{rn}` as a logo", mention_author=False)
            return

        users[str(comp)]["logo"]=rn

        with open("company.json", "w") as f:
            json.dump(users, f, indent=4)
        await context.reply(f"You have successfully set your company logo to `{rn}`", mention_author=False)

    @company.command(name="join")
    @commands.cooldown(1, 3, BucketType.user)
    async def comp_join(self, context, *, name):
        """
        Join a company
        """

        found = 0
        users = await getcompanies()
        for comp in users:
                if users[str(comp)]["identity"].lower() == name.lower():
                    found = 1
                    break
                
                if context.author.id in users[str(comp)]["employees"]:
                    found = 3
                    break

                if context.author.id == users[str(comp)]["owner"]:
                    found = 4
                    break
        
        if found == 0:
            await context.reply(f"{name} is invalid", mention_author=False)
            return
        elif found == 4:
            await context.reply(f"You already own a company", mention_author=False)
            return
        elif context.author.id in users[str(comp)]["employees"]:
            await context.reply(f"You are already an employee to a company", mention_author=False)
            return
           

        users[str(comp)]["net_worth"] += 15*users[str(comp)]["upgrade"]
        users[str(comp)]["employees"] += [context.author.id]

        with open("company.json", "w") as f:
            json.dump(users, f, indent=4)
            
        await context.reply(f"You have successfully joined the company `{name}`", mention_author=False)

    @company.command(name="leave")
    @commands.cooldown(1, 3, BucketType.user)
    async def comp_leave(self, context):
        """
        Leave a company
        """

        found = 0
        users = await getcompanies()
        a = 0
        ab = 0
        nm = ":poop:"
        for comp in users:
                if context.author.id in users[str(comp)]["employees"]:
                    nm = users[str(comp)]["identity"]
                    found = 1
                    break
        
        if found == 0:
            await context.reply(f"You are not an employee at a company", mention_author=False)
            return
        elif found == 2 and a > ab:
            await context.reply(f"You don't work at a company", mention_author=False)
            return
        elif users[str(comp)]["owner"] == context.author.id:
            await context.reply(f"You can't leave your own company", mention_author=False)
            return

        users[str(comp)]["net_worth"] -= 15*users[str(comp)]["upgrade"]
        a = [users[str(comp)]["employees"]]
        a[a == str(context.author.id)+str(",")] = None
        users[str(comp)]["employees"] = a
        with open("company.json", "w") as f:
            json.dump(users, f, indent=4)
        await context.reply(f"You have successfully left the company `{nm}`", mention_author=False)

    @company.command(name="kick")
    @commands.cooldown(1, 3, BucketType.user)
    async def comp_kick(self, context, member: discord.Member=None):
        """
        Kick a member from your company
        """

        users = await getcompanies()
        ab = 0
        for comp in users:
                if member.id in users[str(comp)]["employees"]:
                    ab = 1
                    break
        
        if not users[str(comp)]["owner"] == context.author.id:
            await context.reply(f"You don't own a company", mention_author=False)
            return
        elif ab == 0:
            await context.reply(f"`{member.name}` is not an employee at your company", mention_author=False)
            return

        users[str(comp)]["net_worth"] -= 15*users[str(comp)]["upgrade"]
        a = [users[str(comp)]["employees"]]
        a[a == str(member.id)+str(",")] = None
        with open("company.json", "w") as f:
            json.dump(users, f, indent=4)
        await context.reply(f"You have successfully kicked member `{member}` from your company", mention_author=False)

    @company.command(name="claim")
    @commands.cooldown(1, 30000, BucketType.user)
    async def comp_claim(self, context):
        """
        Claim your salary
        """

        await openaccount(context.author)
        found = 0
        found2 = 0
        users = await getcompanies()
        for comp in users:
                if context.author.id in users[str(comp)]["employees"]:
                    found = 1
                    break
                if users[str(comp)]["owner"] == context.author.id:
                    found = 1
                    break
        
        if found == 0 and found2 == 0:
            await context.reply(f"You are not an employee at any company", mention_author=False)
            return
        elif users[str(comp)]["net_worth"] < 2:
            await context.reply(f"You have no salary to claim", mention_author=False)
            return            
        
        if len(users[str(comp)]["employees"]) < 2:
            amount = round(users[str(comp)]["net_worth"]/2)
        else:
            amount = round(users[str(comp)]["net_worth"]/len(users[str(comp)]["employees"]))
        us = await getbankdata()
        us[str(context.author.id)]["wallet"] += amount

        with open("currency.json", "w") as f:
            json.dump(us, f, indent=4)
        with open("company.json", "w") as f:
            json.dump(users, f, indent=4)
        await context.reply(f"You have successfully claimed your salary of `{amount:,}`$", mention_author=False)

    @company.command(name="upgrade")
    @commands.cooldown(1, 3, BucketType.user)
    async def comp_upgrade(self, context, levels=1):
        """
        Upgrade your company for 50000$
        """

        await openaccount(context.author)

        userba = await getbankdata()
        user = context.author
        efg = (50000*levels)*userba[str(user.id)]["multiplier"]
        if userba[str(user.id)]["wallet"] < efg:
            await context.send(f"You don't have {efg}$", mention_author=False)
            return

        found = 0
        users = await getcompanies()
        
        for comp in users:
                if users[str(comp)]["owner"] == context.author.id or context.author.id in users[str(comp)]["employees"]:
                    found = 1
                    break
        
        if found == 0:
            await context.reply(f"You are not in a company", mention_author=False)
            return

        lvl = users[str(comp)]["upgrade"] + levels
        users[str(comp)]["upgrade"] += levels
        userba[str(user.id)]["wallet"] -= efg
        
        with open("currency.json", "w") as f:
           json.dump(userba, f, indent=4)
        with open("company.json", "w") as f:
            json.dump(users, f, indent=4)
        await context.reply(f"You have successfully upgraded your company to the level of {lvl}", mention_author=False)

    @company.command(name="list")
    async def companylist(self, context):
        """
        Displays every company
        """
        if context.invoked_subcommand is None:
            totalcomp = await getcompanies()
            leader_board = {}
            total = []
            for comp in totalcomp:
                total_amount = (totalcomp[str(comp)]["net_worth"]*totalcomp[str(comp)]["upgrade"])
                leader_board[total_amount] = totalcomp[str(comp)]
                total.append(total_amount)

            total = sorted(total, reverse=True)
            index = 1
            msg = ""

            for amount in total:
                namek = leader_board[amount]["identity"]

                msg += f"{index} - {namek} |"
                index += 1
            await context.reply(msg, mention_author=False)

async def notcrypto(strr):
    return not strr == "bitcoin" and not strr == "ethereum" and not strr == "meth "

async def iscrypto(strr):
    return strr == "bitcoin" or strr == "ethereum" or strr == "monero"

async def openaccount(user):
    users = await getbankdata()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["kick"] = 0
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["multiplier"] = 1
        users[str(user.id)]["bitcoin"] = 0
        users[str(user.id)]["eth"] = 0
        users[str(user.id)]["bag"] = ""
        users[str(user.id)]["description"] = ""
        users[str(user.id)]["badge"] = ""
        users[str(user.id)]["cryptowallet"] = "no"

    with open("currency.json", "w") as f:
        json.dump(users, f, indent=4)

    return True

async def opencompany(name, owner):
    comp = await getcompanies()

    if str(name) in comp:
        return False
    else:
        comp[str(name)] = {}
        comp[str(name)]["name"] = name
        comp[str(name)]["identity"] = name
        comp[str(name)]["logo"] = ""
        comp[str(name)]["owner"] = owner
        comp[str(name)]["employees"] = []
        comp[str(name)]["pending"] = []
        comp[str(name)]["net_worth"] = 0
        comp[str(name)]["upgrade"] = 1

    with open("company.json", "w") as f:
        json.dump(comp, f, indent=4)

    return True

async def opencrypto(name, value):
    crypto = await getcrypto()

    if str(name) in crypto:
        return False
    else:
        crypto[str(name)] = {}
        crypto[str(name)]["value"] = value

    with open("crypto.json", "w") as f:
        json.dump(crypto, f, indent=4)

    return True

async def getbankdata():
    with open("currency.json", "r") as f:
        users = json.load(f)

    return users

async def getcompanies():
    with open("company.json", "r") as f:
        users = json.load(f)

    return users

async def getcrypto():
    with open("crypto.json", "r") as f:
        users = json.load(f)

    return users

async def ub(user):
    users = await getbankdata()

    with open("currency.json", "w") as f:
        json.dump(users, f, indent=4)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"], users[str(user.id)]["bitcoin"], users[str(user.id)]["eth"], users[str(user.id)]["multiplier"]]
    return bal

def setup(bot):
    bot.add_cog(economy(bot))