"""
Author :  Sitanshu15
Bot : Nora
"""
import asyncio
import datetime
import difflib
import functools
import io
import math
import os
import json
import random
import re
import textwrap
import time
import typing as t
import unicodedata
from difflib import get_close_matches
from io import BytesIO

import aiohttp
import asyncpg
import discord
import dotenv
import humanize
import paginator
import requests
import wavelink
import wikipedia
import xkcd_wrapper
from trivia import trivia
from asyncdagpi import Client, ImageFeatures
from discord.ext import commands
from discord.ext.buttons import Paginator
from discord.ext.commands import BucketType, Cog, Greedy
from dotenv import load_dotenv
from jishaku.codeblocks import codeblock_converter
from jishaku.functools import executor_function
from mystbin import Client
from PIL import Image, ImageFilter
from requests.utils import quote
from random_words import RandomWords
from core.utils import Quiz as quiz

class CantBuyMoreThanOne(commands.CommandError):
    pass

class CantSellMoreThanOne(commands.CommandError):
    pass

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.SHARE_THRESHOLD = 175
    
    @commands.command()
    async def open(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        if accounts:
            await ctx.reply(f"You alredy opened an account")
            return False
        await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", ctx.author.id)
        e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
        e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)
    
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        if not accounts:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", ctx.author.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        val = random.randint(0, 170)
        await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] + val, ctx.author.id)
        no_msg = ["No lol", "Imagine begging lol", "I need to buy my air pods", "Be gone thot"]
        ppl = ["Zezus", "Niki minaj", "Ed sheran",  "The guy you hate", "Taylor swift",  "Vyy", "", "A stranger", "The guy you hate", "Mr.Beast", "Your mom", "Kevin Jones", "Pauly D", "Tom hanks", "Tom criuse", "Leanardo DiCaprio", "Pia Mia", "Morgan feeman", "Zach king", "Charlie Damilio", "Addison rae", "Sommer ray", "Faze rug", "Morgz", "Brent",  "Jimmin"]
        if val == 0:
            msg = f"{random.choice(ppl)}: {random.choice(no_msg)}"
        if val > 1:
            msg = f"{random.choice(ppl)} gave you, **{val}**  "
        e = discord.Embed(description=f"{msg}", color=discord.Color.dark_blue())
        e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)
        if await self.bot.db.fetchrow("SELECT econ_index FROM econ WHERE user_id = $1", ctx.author.id) <= self.SHARE_THRESHOLD:
            mm = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
            await self.bot.db.execute("UPDATE econ SET econ_index = $1 WHERE user_id = $2", mm["econ_index"] + 1, ctx.author.id)
    
    @commands.command()
    @commands.cooldown(1, 70, commands.BucketType.user)
    async def mine(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        pi_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", ctx.author.id, "pickaxe")
        ec_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        pickaxe = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", ctx.author.id, "pickaxe")
        if not accounts:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", ctx.author.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        if not pickaxe:
            e = discord.Embed(title=f"Item missing", description=f"You need a pickaxe to mine!! ⛏", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
            return
        if 0 > pi_data["dur"]:
            await self.bot.db.execute("DELETE FROM inve WHERE user_id = ($1) AND item = ($2)", ctx.author.id, "pickaxe")
            await ctx.reply("You broke your pickaxe! ⛏")
            return
        else:
            ore_amt = random.randint(1, 10)
            ore_val = random.randint(125, 150)
            dur_minus = random.randint(3, 15)
            amt = ore_val * ore_amt
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ec_data["wallet"] + amt, ctx.author.id)
            await self.bot.db.execute("UPDATE inve SET dur = $1 WHERE user_id = $2 AND item = $3", pi_data["dur"] - dur_minus, ctx.author.id, "pickaxe")
            e = discord.Embed(description=f"⛏ You used **{dur_minus}%** of your pickaxe and found {ore_amt} noranics(Nora ore).\nnoranics was going up for {ore_val}   you sold your {ore_amt} and profited {amt}  !!")            
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        if await self.bot.db.fetchrow("SELECT econ_index FROM econ WHERE user_id = $1", ctx.author.id) <= self.SHARE_THRESHOLD:
            mm = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
            await self.bot.db.execute("UPDATE econ SET econ_index = $1 WHERE user_id = $2", mm["econ_index"] + 1, ctx.author.id)
    
    @commands.command()
    @commands.cooldown(1, 70, commands.BucketType.user)
    async def fish(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        fr_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", ctx.author.id, "fishing_rod")
        ec_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        fishing_rod = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", ctx.author.id, "fishing_rod")
        pet = await self.bot.db.fetch("SELECT * FROM pets WHERE user_id = $1", ctx.author.id)
        if not accounts:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", ctx.author.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        if not fishing_rod:
            e = discord.Embed(title=f"Item missing", description=f"You need a fishing rod to fish!! <:fishing_pole:835185055433097329> ", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
            return
        if random.randint(1, 100) < 100:
            f_img = "🐡"
            f_amt = random.randint(3, 15)
            f_pri = 100
            f_nme = "Blow-fish"
        if random.randint(1, 100) < 30:
            f_img = "🐟"
            f_amt = random.randint(3, 8)
            f_pri = 500
            f_nme = "Blue-fish"
        if random.randint(1, 100) < 10:
            f_img = "🐠"
            f_amt = random.randint(1, 4)
            f_pri = 1000
            f_nme = "Tropical-fish"
        if random.randint(1, 100) == 1:
            f_img = "🦈"
            f_amt = random.randint(1, 2)
            f_pri = 5000
            f_nme = "Shark"
        else:
            grnd_ttl = f_amt * f_pri
            if pet:
                pet_data = await self.bot.db.fetchrow("SELECT * FROM pets WHERE user_id = $1", ctx.author.id)
                if pet_data["name"] == "dog":
                    grnd_ttl = int(f_amt*f_pri+f_amt*f_pri*0.1)
                if pet_data["name"] == "cat":
                    grnd_ttl = int(f_amt*f_pri+f_amt*f_pri*0.2)
                if pet_data["name"] == "parrot":
                    grnd_ttl = int(f_amt*f_pri+f_amt*f_pri*0.3)
                if pet_data["name"] == "dragon":
                    grnd_ttl = int(f_amt*f_pri+f_amt*f_pri*0.4)
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ec_data["wallet"] + grnd_ttl, ctx.author.id)
            e = discord.Embed(description=f"You casted you line in to the water and found `{f_amt}` of the {f_nme}(s).\nThe {f_nme} was going up in the market for {f_pri}   you sold your {f_amt} and profited {grnd_ttl}  !! `{f_img}`")         
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        if await self.bot.db.fetchrow("SELECT econ_index FROM econ WHERE user_id = $1", ctx.author.id) <= self.SHARE_THRESHOLD:
            mm = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
            await self.bot.db.execute("UPDATE econ SET econ_index = $1 WHERE user_id = $2", mm["econ_index"] + 1, ctx.author.id)
        
    @commands.command(aliases=["post meme", "pm"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def post_meme(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        lp_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", ctx.author.id, "laptop")
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        laptop = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", ctx.author.id, "laptop")
        if not accounts:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", ctx.author.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        if not laptop:
            e = discord.Embed(title=f"Item missing", description=f"You need a laptop to post memes!! <:laptop:835185820230615091> ", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
            return
        if random.randint(1, 100) <  25:
            await self.bot.db.execute("DELETE FROM inve WHERE user_id = ($1) AND item = ($2)", ctx.author.id, "laptop")
            e = discord.Embed(title="You broke your laptop!", description="Imagine breaking your laptop, lol.." , color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        else:
            data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
            amt = random.randint(100, 955)
            e = discord.Embed(title=f"Choose a genre of meme", description=f"React for each genre!\n\n`1️⃣`● Dank Meme\n`2️⃣`● Dark Meme\n`3️⃣`● Comic Meme\n`4️⃣`● Intellectual Meme\n`5️⃣`● Reposted Meme\n`6️⃣`● Fresh Meme")
            msg = await ctx.send(embed=e)
            def check(reaction, user):
                return (user == ctx.author) and (str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣",  "6️⃣"])
            await msg.add_reaction('1️⃣')
            await msg.add_reaction('2️⃣')
            await msg.add_reaction('3️⃣')
            await msg.add_reaction('4️⃣')
            await msg.add_reaction('5️⃣')
            await msg.add_reaction('6️⃣')
            try:
                reaction, _user = await self.bot.wait_for('reaction_add', timeout=60, check=check)

            except asyncio.TimeoutError:
                error = discord.Embed(description="Reaction timed out.", Color=discord.Color.dark_blue())
                await msg.edit(content=None, embed=error)

                try:
                    await msg.clear_reactions()

                except discord.errors.HTTPException:
                    pass
            else:
                if str(reaction.emoji) == "1️⃣":
                    meme_type = "Dank Meme"
                if str(reaction.emoji) == "2️⃣":
                    meme_type = "Dark Meme"
                if str(reaction.emoji) == "3️⃣":
                    meme_type = "Comic Meme"
                if str(reaction.emoji) == "4️⃣":
                    meme_type = "Intellectual Meme"
                if str(reaction.emoji) == "5️⃣":
                    meme_type = "Reposted Meme"
                if str(reaction.emoji) == "6️⃣":
                    meme_type = "Fresh Meme"
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] + amt, ctx.author.id)
            e = discord.Embed(title=f"{meme_type}", description=f"You earned {amt}   from ad cents", color=discord.Color.dark_blue())
            await msg.delete()
            await ctx.send(embed=e)
        if await self.bot.db.fetchrow("SELECT econ_index FROM econ WHERE user_id = $1", ctx.author.id) <= self.SHARE_THRESHOLD:
            mm = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
            await self.bot.db.execute("UPDATE econ SET econ_index = $1 WHERE user_id = $2", mm["econ_index"] + 1, ctx.author.id)

    
    @commands.command()
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def hunt(self, ctx):
        pet = await self.bot.db.fetch("SELECT * FROM pets WHERE user_id = $1", ctx.author.id)
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        ht_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", ctx.author.id, "h_rifle")
        ec_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        ht_rf = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", ctx.author.id, "h_rifle")
        if not accounts:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", ctx.author.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        if not ht_rf:
            e = discord.Embed(title=f"Item missing", description=f"You need a hunting rifle to hunt!! <:hunting_rifle:835185487542747225> ", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
            return
        if random.randint(1, 100) < 100:
            f_img = "🦨"
            f_amt = random.randint(1, 8)
            f_pri = 50
            f_nme = "Skunk"
        if random.randint(1, 100) < 60:
            f_img = "🐇"
            f_amt = random.randint(1, 8)
            f_pri = 100
            f_nme = "Rabbit"
        if random.randint(1, 100) < 50:
            f_img = "🦆"
            f_amt = random.randint(1, 8)
            f_pri = 300
            f_nme = "Duck"
        if random.randint(1, 100) < 40:
            f_img = "🦌"
            f_amt = random.randint(1, 8)
            f_pri = 500
            f_nme = "Deer"
        if random.randint(1, 100) < 30:
            f_img = "🐗"
            f_amt = random.randint(1, 4)
            f_pri = 1000
            f_nme = "Boar"
        if random.randint(1, 100) < 5:
            f_img = "🐲"
            f_amt = random.randint(1, 2)
            f_pri = 5000
            f_nme = "Dragon"
        else:
            amt = f_amt*f_pri
            if pet:
                pet_data = await self.bot.db.fetchrow("SELECT * FROM pets WHERE user_id = $1", ctx.author.id)
                if pet_data["name"] == "parrot":
                    amt = int(f_amt*f_pri+f_amt*f_pri*0.1)
                if pet_data["name"] == "dragon":
                    amt = int(f_amt*f_pri+f_amt*f_pri*0.2)
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ec_data["wallet"] + amt, ctx.author.id)
            e = discord.Embed(description=f"You went hunting and found {f_amt} {f_img}{f_nme}(s)\nYou sold each one for {f_pri}   and earned a total of {amt}  .", color=discord.Color.dark_blue())            
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        if await self.bot.db.fetchrow("SELECT econ_index FROM econ WHERE user_id = $1", ctx.author.id) <= self.SHARE_THRESHOLD:
            mm = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
            await self.bot.db.execute("UPDATE econ SET econ_index = $1 WHERE user_id = $2", mm["econ_index"] + 1, ctx.author.id)
        
    @commands.command(aliases=["bet"])
    @commands.cooldown(1, 50, commands.BucketType.user)
    async def gamble(self, ctx, amount=None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        bot_choice = random.randint(1, 10)
        u_choice = random.randint(1, 10)
        b_amt = int(amount) + random.randint(70, 300)
        amt = int(amount) + b_amt
        accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        if not accounts:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", ctx.author.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        if amount == "all":
            amount = data["wallet"]
        if amount == "wallet":
            amount = data["wallet"]
        if amount == "wallet":
            amount_up = data["wallet"]
            amount = 0.5*amount_up
        if amount == None:
            e = discord.Embed(title="Please enter amount", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e) 
            return
        if int(amount) > data["wallet"]:
            e = discord.Embed(description=f"Please enter a valid amount you are trying to gamble more than you have", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
            return
        if u_choice == int(bot_choice):
            e = discord.Embed(title=f"{ctx.author.name}'s gamble", description=f"It was a draw!!", color=discord.Color.dark_blue())
            e.add_field(name=f"{ctx.author.name}", value=f"> `{u_choice}`")
            e.add_field(name=f"{self.bot.name}", value=f"> `{bot_choice}`")
            await ctx.send(embed=e)
            return
        if bot_choice < int(u_choice):
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] + amt, ctx.author.id)
            e = discord.Embed(title=f"{ctx.author.name}'s gamble", description=f"You won {amt}  !", color=discord.Color.dark_blue())
            e.add_field(name=f"{ctx.author.name}", value=f"> `{u_choice}`")
            e.add_field(name=f"Nora", value=f"> `{bot_choice}`")
            await ctx.send(embed=e)
            return
        if u_choice < int(bot_choice):
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] - amt, ctx.author.id)
            e = discord.Embed(title=f"{ctx.author.name}'s gamble", description=f"You lost {amt}  !", color=discord.Color.dark_blue())
            e.add_field(name=f"{ctx.author.name}", value=f"> `{u_choice}`")
            e.add_field(name=f"Nora", value=f"> `{bot_choice}`")
            await ctx.send(embed=e)
            return
        if await self.bot.db.fetchrow("SELECT econ_index FROM econ WHERE user_id = $1", ctx.author.id) <= self.SHARE_THRESHOLD:
            mm = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
            await self.bot.db.execute("UPDATE econ SET econ_index = $1 WHERE user_id = $2", mm["econ_index"] + 1, ctx.author.id)
            
    @commands.command(aliases=["bal"])
    async def balance(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        member = member or ctx.author
        accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", member.id)
        if not accounts:
            await ctx.send(f"{member} has no balance")
            return False
        data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        wal_amt = data["wallet"]
        bank_amt = data["bank"]
        e = discord.Embed(title=f"{member}'s balance", description=f"Wallet: {wal_amt}  \nBank: {bank_amt}  ", timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_blue())
        e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        e.set_footer(text=f"What a scrub")
        await ctx.send(embed=e)
    
    @commands.command(aliases=["dep"])
    async def deposit(self, ctx, amount=None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        if not accounts:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", ctx.author.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        if amount == "all":
            amount = data["wallet"]
        if amount == "max":
            amount = data["wallet"]
        if amount == "half":
            amount_up = data["wallet"]
            amount = 0.5*amount_up
        if amount == None:
            e = discord.Embed(title="Please enter amount", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e) 
            return
        if int(amount) > data["wallet"]:
            e = discord.Embed(description=f"Please enter a valid amount you are trying to deposit more than you have", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
            return 
        else:
            walt = data["wallet"] - int(amount)
            bnk =  data["bank"] + int(amount)
            await self.bot.db.execute("UPDATE econ SET wallet = $1, bank = $2 WHERE user_id = $3",walt , bnk, ctx.author.id)
            e = discord.Embed(tittle=f"Deposit success", description=f"I have deposited **{amount}**   to your bank" , color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)

    @commands.command(aliases=["with", "wd"])
    async def withdraw(self, ctx, amount=None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        if not accounts:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", ctx.author.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        if amount == "all":
            amount = data["bank"]
        if amount == "max":
            amount = data["bank"]
        if amount == "half":
            amount_up = data["bank"]
            amount = 0.5*amount_up
        if amount == None:
            e = discord.Embed(title="Please enter amount", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e) 
            return
        if int(amount) > data["bank"]:
            e = discord.Embed(description=f"Please enter a valid amount you are trying to withdraw more than you have", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
            return 
        else:
            walt = data["wallet"] + int(amount)
            bnk =  data["bank"] - int(amount)
            await self.bot.db.execute("UPDATE econ SET wallet = $1, bank = $2 WHERE user_id = $3",walt , bnk, ctx.author.id)
            e = discord.Embed(tittle=f"Withdrawal success", description=f"I have withdrew **{amount}**   from your bank to your pocket" , color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)          
    
    @commands.command(aliases=["rob"])
    @commands.cooldown(1, 35, commands.BucketType.user)
    async def steal(self, ctx, member: discord.Member):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        m_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", ctx.author.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        if not m_data:
            await ctx.send(f"{member.name} has no balance!")
            return
        if 100 > ctx_data["wallet"]:
            l = ctx_data["wallet"]
            e = discord.Embed(title=f"You need at least 100", description=f"You will need 100   to pay the fine if you get caught of course" ,color=discord.Color.dark_blue())
            e.set_footer(text=f"Your wallet's balance is {l}  ")
            await ctx.send(embed=e)
            return
        if 100 > m_data["wallet"]:
            l = m_data["wallet"]
            e = discord.Embed(title=f"{member} is broke", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            e.set_footer(text=f"Their wallet's balance is {l}  ")
            await ctx.send(embed=e)
            return
        if random.randint(1, 100) < 20:
            fine_nmb = random.randint(60, 100)
            e = discord.Embed(description=f"You try to rob {member}, but the police see you and let you go with a {fine_nmb}   fine and a warning", color=discord.Color.dark_blue())           
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
            return
        else:
            member_m = m_data["wallet"]*0.3
            amount = random.randint(100, member_m)
            m_walt = member_m - amount 
            ctx_walt = amount
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2",m_walt , member.id)
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2",ctx_walt , ctx.author.id)
            e = discord.Embed(title=f"You robbed {member}", description=f"You robbed them for {amount}   now they have got {m_walt}  ", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        
    
    @commands.command(aliases=["give", "send"])
    async def share(self, ctx, member: discord.Member, perms=None, amount=None):
        if perms == "--sudo":
            if ctx.author.id == 814030950597132321 or 728260210464129075:
                ff = int(amount)
                data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
                accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", member.id)
                if not accounts:
                    await ctx.send("They have no account")
                    return
                else:
                    await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] + ff, member.id)
                    await ctx.reply(f"Added {amount} to {member}'s balance")
            else:
                await ctx.send("You cant run this command with sudo permissions. Only my developers are eligible to run this command wuth sudo permissions")
        if not perms:
            bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
            if bl_users:
                e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
                await ctx.send(embed=e)
                return
            accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
            if not accounts:
                await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", ctx.author.id)
                e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
                e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=e)
            if not await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", member.id):
                e = discord.Embed(description=f"{member} does not have an account", color=discord.color.dark_blue())
                e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=e)
                return
            data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
            if data["econ_index"] >= self.SHARE_THRESHOLD: 
                if amount == "all":
                    amount = data["wallet"]
                if amount == "max":
                    amount = data["wallet"]
                if amount == "half":
                    amount_up = data["wallet"]
                    amount = 0.5*amount_up
                if amount == None:
                    e = discord.Embed(title="Please enter amount", color=discord.Color.dark_blue())
                    e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=e) 
                    return
                if int(amount) > data["wallet"]:
                    e = discord.Embed(description=f"Please enter a valid amount you are trying to give {member} more than you have", color=discord.Color.dark_blue())
                    e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=e)
                    return
                member_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
                if member_data:
                    await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] - amount, ctx.author.id)
                    await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] + amount, member.id)
                    e = discord.Embed(description=f"I have sent {amount} to {member}!", color=discord.Color.dark_blue())
                    e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=e)
            else:
                e = discord.Embed(title="You are a normie!", description="You cant share money with other people yet, you are still a noob!(In all seriouness, this is a method of stopping alt accounts from sending money to a main account.)", color=discord.Color.dark_blue())
                e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=e)
                return
        if perms != "--sudo":
            await ctx.reply(f"{perms} is not a valid permission flag.")

    #BUY AND SELL
    
    @commands.command()
    async def buy(self, ctx, item, amount=1):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        amt = int(amount)
        if item.lower() == "pickaxe":
            if amt > 1:
                raise CantBuyMoreThanOne
            else:
                await self.buy_pick(ctx, ctx.author)
                return
        if item.lower() == "pick":
            if amt > 1:
                raise CantBuyMoreThanOne
            else:
                await self.buy_pick(ctx, ctx.author)
                return
        if item.lower() == "fishing_rod":
            if amt > 1:
                raise CantBuyMoreThanOne
            else:
                await self.buy_fr(ctx, ctx.author)
                return
        if item.lower() == "fr":
            if amt > 1:
                raise CantBuyMoreThanOne
            else:
                await self.buy_fr(ctx, ctx.author)
                return
        if item.lower() == "lp":
            if amt > 1:
                raise CantBuyMoreThanOne
            else:
                await self.buy_lp(ctx, ctx.author)
                return
        if item.lower() == "hr":
            if amt > 1:
                raise CantBuyMoreThanOne
            else:
                await self.buy_h_r(ctx, ctx.author)
                return
        if item.lower() == "guitar":
            if amt > 1:
                raise CantBuyMoreThanOne
            else:
                await self.buy_guitar(ctx, ctx.author)
                return
        if item.lower() == "drum":
            if amt > 1:
                raise CantBuyMoreThanOne
            else:
                await self.buy_drums(ctx, ctx.author)
                return
        if item.lower() == "alcohol":
            await self.buy_alc(ctx, ctx.author, amount)
            return
        if item.lower() == "life_saver":
            await self.buy_ls(ctx, ctx.author, amount)
            return
        if item.lower() == "ls":
            await self.buy_ls(ctx, ctx.author, amount)
            return
        if item.lower() == "noramedal":
            await self.buy_nrmdl(ctx, ctx.author, amount)
            return
        if item.lower() == "noratrophy":
            await self.buy_nr_trophy(ctx, ctx.author, amount)
            return
        if item.lower() == "lotterytk":
            await self.buy_lotterytk(ctx, ctx.author)
            return

    @buy.error
    async def buy_error(self, ctx, exc):
        if isinstance(exc, CantBuyMoreThanOne):
            await ctx.send("`CantBuyMoreThanOne` **:** You cant buy more than one of that item!")

    @commands.command()
    async def sell(self, ctx, item, amount=1):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        amt = int(amount)
        if item.lower() == "pickaxe":
            if amt > 1:
                raise CantSellMoreThanOne
            else:
                await self.sell_1(ctx, ctx.author, "pickaxe", 7500)
        if item.lower() == "fishing_rod":
            if amt > 1:
                raise CantSellMoreThanOne
            else:
                await self.sell_1(ctx, ctx.author, "fishing_rod", 8500)
        if item.lower() == "laptop":
            if amt > 1:
                raise CantSellMoreThanOne
            else:
                await self.sell_1(ctx, ctx.author, "laptop", 10000)
        if item.lower() == "hr":
            if amt > 1:
                raise CantSellMoreThanOne
            else:
                await self.sell_1(ctx, ctx.author, "h_rifle", 50000)
        if item.lower() == "guitar":
            if amt > 1:
                raise CantSellMoreThanOne
            else:
                await self.sell_1(ctx, ctx.author, "guitar", 75000)
        if item.lower() == "drum":
            if amt > 1:
                raise CantSellMoreThanOne
            else:
                await self.sell_1(ctx, ctx.author, "drum",  100000)
        if item.lower() == "lotterytk":
            if amt > 1:
                raise CantSellMoreThanOne
            else:
                await self.sell_1(ctx, ctx.author, "ltk", 2500)
        if item.lower() == "alcohol":
            await self.sell_inr(ctx, ctx.author, "alcohol", 8500, amt)
            return
        if item.lower() == "life_saver":
            await self.sell_inr(ctx, ctx.author, "life_saver", 25000, amt)
            return
        if item.lower() == "Noramedal":
            await self.sell_inr(ctx, ctx.author, "nr_medal", 10000000, amt)
            return
        if item.lower() == "Noratrophy":
            await self.sell_inr(ctx, ctx.author, "nr_trophy", 50000000, amt)
            return
        if item.lower() == "lotterytk":
            await self.sell_inr(ctx, ctx.author, "ltk", 2500, amt)
            return                                        
    
    #SHOP,INV AND USE
    
    @commands.command(aliases=["store"])
    async def shop(self, ctx, page=None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        if page == None:
            page = "1"
        if page == "1":
            e = discord.Embed(title="Welcome to the Nora store", description="Use `nr.buy <itemname>` to buy something. The `<itemname>` must match the given `key` or some other secret keys!. Your `[itemamount]` should also follow the given `limit`", timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_blue())
            e.add_field(name="<:lottery_ticket:847447419498790952> **Lottery Ticket** — 〄 2,500", value="Key: `lotterytk`\nDescription: Buy this and get a higher chance of winning the lottery, nr.lottery for inro on te next, comming or present lottery. Join the support server for 15% more!(Note)\nUsage: `None - Read description`\nLimit: `1`", inline=False)
            e.add_field(name="<a:pickaxe:836163392796229642> **Pickaxe** — 〄 7,500", value="Key: `pick`\nDescription: Go mining for epic noranics ore!\nUsage: `nr.mine`\nLimit: `1`", inline=False)
            e.add_field(name="<:fishing_pole:835185055433097329> **Fishing Rod** — 〄 8,500", value="Key: `fishing_rod`\nDescription: Go out to your nearest lake chill, fish and sell them for sweet money!\nUsage: `nr.fish`\nLimit: `1`", inline=False)
            e.add_field(name="<:alcohol:836203535728771092> **Alcohol** — 〄 8,500", value="Key: `alcohol`\nDescription: Drink it and you might get lucky, just maybe\nUsage: `nr.use alcohol`\nLimit: `None`", inline=False)
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            e.set_footer(text="Page Index 1/3")
            await ctx.send(embed=e)
            return
        if page == "2":
            e = discord.Embed(title="Welcome to the Nora store", description="Use `nr.buy <itemname>` to buy something. The `<itemname>` must match the given `key` or some other secret keys!. Your `[itemamount]` should also follow the given `limit`", timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_blue())
            e.add_field(name="<:laptop:835185820230615091> **Laptop** — 〄 10,000", value="Key: `lp`\nDescription: Post meme's for the ad cents.\nUsage: `nr.pm`\nLimit: `1`", inline=False)
            e.add_field(name="<:lifesaver:836562944950796309> **Life Saver** — 〄 25,000", value="Key: `life_saver`\nDescription: If a life saver is in your inventory at the time of death, this item will be consumed and prevent you from dying! You will keep your coins and items.\nUsage: `None - Read description`\nLimit: `None`", inline=False)
            e.add_field(name="<:hunting_rifle:835185487542747225> **Hunting Rifle** — 〄 50,000", value="Key: `hr`\nDescription: Go and hunt for animals!\nUsage: `nr.hunt`\nLimit: `1`", inline=False)
            e.add_field(name="<:classical_guitar:836802689635450880> **Guitar** — 〄 75,000", value="Key: `guitar`\nDescription: Go busking(term for: Street performance)\nUsage: `nr.use guitar`\nLimit: `1`", inline=False)
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            e.set_footer(text="Page Index 2/3")
            await ctx.send(embed=e)
            return
        if page == "3":
            e = discord.Embed(title="Welcome to the Nora store", description="Use `nr.buy <itemname>` to buy something. The `<itemname>` must match the given `key` or some other secret keys!. Your `[itemamount]` should also follow the given `limit`", timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_blue())
            e.add_field(name="<:drums:836815664189669427> **Drums** — 〄 100,000", value="Key: `drum`\nDescription: Perform in the public!\nUsage: `nr.use drum`\nLimit: `1`", inline=False)
            e.add_field(name="<:noramedal:836832817307844618> **Nora Medal** — 〄 10,000,000", value="Key: `noramedal`\nDescription: A medal only the top 1% of players have!\nUsage: `Show-off`\nLimit: `None`", inline=False)
            e.add_field(name="<:noratrophy:836834560556662784> **Nora Trophy** — 〄 50,000,000", value="Key: `noratrophy`\nDescription: Literally only the richest of the richest of the richest of the richest of the richest of the rich will hold these beloved trophies.\nUsage: `None - Read description`\nLimit: `None`", inline=False)
            e.set_footer(text="Page Index 3/3")
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
            return
    
    @commands.command(aliases=["inv"])
    async def inventory(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        member = member or ctx.author
        accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", member.id)
        inve = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", member.id)
        if not accounts:
            await ctx.send(f"{member} has no balance")
            return
        if not inve:
            e = discord.Embed(title=f"{member} has no inventory", timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
            return
        ltk = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "ltk")
        fr = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "fishing_rod")
        hr = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "h_rifle")
        lp = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "laptop")
        pick = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "pickaxe")
        drums = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "drum")
        guitar = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "guitar")
        alcohol = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "alcohol")
        alcohol_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "alcohol")
        life_saver = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "life_saver")
        lifesaver_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "life_saver")
        Nora_medal = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "nr_medal")
        Nora_medal_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "nr_medal")
        Nora_trophy = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "nr_trophy")
        Nora_trophy_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "nr_trophy")
        e = discord.Embed(title=f"{member}'s inventory", timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_blue())
        e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        if ltk:
            ltk_amt = Nora_trophy_data["amt"]
            e.add_field(name="<:lottery_ticket:847447419498790952> Lottery Ticket", value=f"Amount: 1")
        if fr:
            e.add_field(name="<:fishing_pole:835185055433097329> Fishing Rod", value="Amount: 1")
        if hr:
            e.add_field(name="<:hunting_rifle:835185487542747225> Hunting Rifle", value="Amount: 1")
        if lp:
            e.add_field(name="<:laptop:835185820230615091> Laptop", value="Amount: 1")
        if pick:
            e.add_field(name="<a:pickaxe:836163392796229642> Pickaxe", value="Amount: 1")
        if drums:
            e.add_field(name="<:drums:836815664189669427> Drums", value="Amount: 1")
        if guitar:
            e.add_field(name="<:classical_guitar:836802689635450880> Guitar", value="Amount: 1")
        if alcohol and alcohol_data["amt"] > 0:
            alcohol_amt = alcohol_data["amt"]
            e.add_field(name="<:alcohol:836203535728771092> Alcohol", value=f"Amount: {alcohol_amt}")
        if life_saver and lifesaver_data["amt"] > 0:
            life_saver_amt = lifesaver_data["amt"]
            e.add_field(name="<:lifesaver:836562944950796309> Life Saver", value=f"Amount: {life_saver_amt}")
        if Nora_medal and Nora_medal_data["amt"] > 0:
            Nora_medal_amt = Nora_medal_data["amt"]
            e.add_field(name="<:noramedal:836832817307844618> Nora Medal", value=f"Amount: {Nora_medal_amt}")
        if Nora_trophy and Nora_trophy_data["amt"] > 0:
            Nora_trophy_amt = Nora_trophy_data["amt"]
            e.add_field(name="<:noratrophy:836834560556662784> Nora Trophy", value=f"Amount: {Nora_trophy_amt}")
        await ctx.send(embed=e)
        
    
    @commands.command()
    @commands.is_owner()
    async def picklotterywinner(self, ctx):
        members = await self.bot.db.fetch("SELECT user_id FROM inve WHERE item = $1", "ltk")
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        ltwinner_up = str(random.choice(members))
        ltwinner_up1 = ltwinner_up.replace('>','')
        ltwinner = ltwinner_up1.replace('<Record user_id=','')
        await ctx.send(ltwinner)
    

    #FUNCTIONS
    
    async def sell_1(self, ctx, member, item, item_price):
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        it = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, item)
        value = item_price*0.5
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        if not it:
            e = discord.Embed(title="You cant sell that", description=f"You cant sell the {item} you dont even have it!", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            ctx.reply(embed=e)
            return
        else:
            await self.bot.db.execute("DELETE FROM inve WHERE user_id = ($1) AND item = ($2)", member.id, item) 
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] + value, member.id)
            e = discord.Embed(title=f"Item sold", description=f"You sold your {item} for 50% of its value at {value}  ", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
    
    async def sell_inr(self, ctx, member, item, item_price, item_amount):
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        it = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, item)
        it_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, item)
        value1 = item_price*item_amount
        value = value1*0.5
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        if not it:
            e = discord.Embed(title="You cant sell that", description=f"You cant sell the {item} you dont even have it!", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            ctx.reply(embed=e)
            return
        if it_data["amt"] == 0:
            await ctx.reply("You dont have any of that item")
            return
        if item_amount > it_data["amt"]:
            await ctx.reply(f"You dont have {item_amount} of {item}.")
            return
        if item_amount == 1:
            await self.bot.db.execute("UPDATE inve SET amt = $1 WHERE user_id = $2 AND item = $3", it_data["amt"] - 1, member.id, item)
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] + value, member.id)
            e = discord.Embed(title=f"Item sold", description=f"You sold {item_amount} {item}(s) for 50% of its value at {value}  ", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
            return
        if item_amount > 1:
            await self.bot.db.execute("UPDATE inve SET amt = $1 WHERE user_id = $2 AND item = $3", it_data["amt"] - item_amount, member.id, item)
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] + value, member.id)
            e = discord.Embed(title=f"Item sold", description=f"You sold {item_amount} {item}(s) for 50% of its value at {value}  ", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
    
    async def buy_lotterytk(self, ctx, member):
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        lottery_ticket = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "ltk")
        value = 7500
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url= member.avatar_url)
            await ctx.send(embed=e)
        if lottery_ticket:
            e = discord.Embed(title=f"You alredy have a lottery ticket, Leave some fun", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
            return
        if value > ctx_data["wallet"]:
            e = discord.Embed(description=f"You are trying to buy an item costing more money than you have\n2500   is the price!", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        else:
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] - value, member.id)
            await self.bot.db.execute("INSERT INTO inve(user_id, item, dur, amt) VALUES($1, $2, $3, $4)", member.id, "ltk", 500, 1)
            e = discord.Embed(title=f"Bought Item", description=f'Good luck on the lottery check inro  on the lottery by running `nr.lottery`', color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)


    async def buy_pick(self, ctx, member):
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        pickaxe = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "pickaxe")
        value = 7500
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url= member.avatar_url)
            await ctx.send(embed=e)
        if pickaxe:
            e = discord.Embed(title=f"You alredy have a pickaxe", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
            return
        if value > ctx_data["wallet"]:
            e = discord.Embed(description=f"You are trying to buy an item costing more money than you have\n7500   is the price!", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        else:
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] - value, member.id)
            await self.bot.db.execute("INSERT INTO inve(user_id, item, dur, amt) VALUES($1, $2, $3, $4)", member.id, "pickaxe", 500, 1)
            e = discord.Embed(title=f"Bought Item", description=f'You bought a pick axe run the `nr.mine` command to make use  of it', color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
    
    
    async def buy_fr(self, ctx, member):
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        fr = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "fishing_rod")
        value = 8500
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        if fr:
            e = discord.Embed(title=f"You alredy have a fishing rod!", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
            return
        if value > ctx_data["wallet"]:
            e = discord.Embed(description=f"You are trying to buy an item costing more money than you have\n8500   is the price!", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        else:
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] - value, member.id)
            await self.bot.db.execute("INSERT INTO inve(user_id, item, amt) VALUES($1, $2, $3)", member.id, "fishing_rod", 1)
            e = discord.Embed(title=f"Bought Item", description=f'You bought a fishing rod run the `nr.fish` command to make use  of it', color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
    
    async def buy_lp(self, ctx, member):
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        fr = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "laptop")
        value = 10000
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        if fr:
            e = discord.Embed(title=f"You alredy have a laptop!", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
            return
        if value > ctx_data["wallet"]:
            e = discord.Embed(description=f"You are trying to buy an item costing more money than you have\n10000   is the price!", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        else:
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] - value, member.id)
            await self.bot.db.execute("INSERT INTO inve(user_id, item, amt) VALUES($1, $2, $3)", member.id, "laptop", 1)
            e = discord.Embed(title=f"Bought Item", description=f'You bought a laptop run the `nr.pm` command to make use of it', color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        
    async def buy_h_r(self, ctx, member):
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        fr = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "h_rifle")
        value = 50000
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        if fr:
            e = discord.Embed(title=f"You alredy have a hunting rifle!", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
            return
        if value > ctx_data["wallet"]:
            e = discord.Embed(description=f"You are trying to buy an item costing more money than you have\n50000   is the price!", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        else:
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] - value, member.id)
            await self.bot.db.execute("INSERT INTO inve(user_id, item, amt) VALUES($1, $2, $3)", member.id, "h_rifle", 1)
            e = discord.Embed(title=f"Bought Item", description=f'You bought a hunting rifle run the `nr.hunt` command to make use of it', color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
    
    async def buy_alc(self, ctx, member, amount):
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        fr = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "alcohol")
        fr_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "alcohol")
        value = 8500*amount
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        if value > ctx_data["wallet"]:
            e = discord.Embed(description=f"You are trying to buy an item costing more money than you have\n{value}   is the price!", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        else:
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] - value, member.id)
            if not fr_data:
                amt = int(amount)
                await self.bot.db.execute("INSERT INTO inve(user_id, item, amt) VALUES($1, $2, $3)", member.id, "alcohol", amt)
                e = discord.Embed(title=f"Bought Item(s)", description=f'You bought `{amount}` alcohol run the `nr.use alcohol` command to make use of it!', color=discord.Color.dark_blue())
                e.set_author(name=f"{member}", icon_url=member.avatar_url)
                await ctx.send(embed=e)
                return
            if fr_data:
                amt = int(amount) + fr_data['amt']
                await self.bot.db.execute("UPDATE inve SET amt = $1 WHERE user_id = $2 AND item = $3", amt, ctx.author.id, "alcohol")
                e = discord.Embed(title=f"Bought Item(s)", description=f'You bought some alcohol run the `nr.use alcohol` command to make use of it!', color=discord.Color.dark_blue())
                e.set_author(name=f"{member}", icon_url=member.avatar_url)
                await ctx.send(embed=e)
                return
        
    async def buy_ls(self, ctx, member, amount):
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        ls = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "life_saver")
        ls_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "life_saver")
        value = 25000*amount
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        if value > ctx_data["wallet"]:
            e = discord.Embed(description=f"You are trying to buy an item costing more money than you have\n{value}   is the price!", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        else:
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] - value, member.id)
            if not ls_data:
                amt = int(amount)
                await self.bot.db.execute("INSERT INTO inve(user_id, item, amt) VALUES($1, $2, $3)", member.id, "life_saver", amt)
                e = discord.Embed(title=f"Bought Item(s)", description=f'You bought `{amount}` life saver(s) the next time you die your life will be saved', color=discord.Color.dark_blue())
                e.set_author(name=f"{member}", icon_url=member.avatar_url)
                await ctx.send(embed=e)
                return
            if ls_data:
                amt = int(amount) + ls_data['amt']
                await self.bot.db.execute("UPDATE inve SET amt = $1 WHERE user_id = $2 AND item = $3", amt, ctx.author.id, "life_saver")
                e = discord.Embed(title=f"Bought Item(s)", description=f'You bought `{amount}` life saver(s) the next time you die your life will be saved', color=discord.Color.dark_blue())
                e.set_author(name=f"{member}", icon_url=member.avatar_url)
                await ctx.send(embed=e)
                return
    
    async def buy_drums(self, ctx, member):
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        fr = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "drum")
        value = 100000
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        if fr:
            e = discord.Embed(title=f"You alredy have a drum!", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
            return
        if value > ctx_data["wallet"]:
            e = discord.Embed(description=f"You are trying to buy an item costing more money than you have\n100000   is the price!", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        else:
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] - value, member.id)
            await self.bot.db.execute("INSERT INTO inve(user_id, item, amt) VALUES($1, $2, $3)", member.id, "drum", 1)
            e = discord.Embed(title=f"Bought Item", description=f'You bought a drum run the `nr.use drum` command to make use of it', color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
    
    async def buy_guitar(self, ctx, member):
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        fr = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "guitar")
        value = 75000
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        if fr:
            e = discord.Embed(title=f"You alredy have a drum!", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
            return
        if value > ctx_data["wallet"]:
            e = discord.Embed(description=f"You are trying to buy an item costing more money than you have\n75000   is the price!", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        else:
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] - value, member.id)
            await self.bot.db.execute("INSERT INTO inve(user_id, item, amt) VALUES($1, $2, $3)", member.id, "guitar", 1)
            e = discord.Embed(title=f"Bought Item", description=f'You bought a guitar run the `nr.use guitar` command to make use of it', color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
    
    async def buy_nrmdl(self, ctx, member, amount):
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        ls = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "nr_medal")
        ls_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "nr_medal")
        value = 10000000*amount
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        if value > ctx_data["wallet"]:
            e = discord.Embed(description=f"You are trying to buy an item costing more money than you have\n{value}   is the price!", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        else:
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] - value, member.id)
            if not ls_data:
                amt = int(amount)
                await self.bot.db.execute("INSERT INTO inve(user_id, item, amt) VALUES($1, $2, $3)", member.id, "nr_medal", amt)
                e = discord.Embed(title=f"Bought Item(s)", description=f'You bought `{amount}` Nora medal(s) welcome to the money gang', color=discord.Color.dark_blue())
                e.set_author(name=f"{member}", icon_url=member.avatar_url)
                await ctx.send(embed=e)
                return
            if ls_data:
                amt = int(amount) + ls_data['amt']
                await self.bot.db.execute("UPDATE inve SET amt = $1 WHERE user_id = $2 AND item = $3", amt, ctx.author.id, "nr_medal")
                e = discord.Embed(title=f"Bought Item(s)", description=f'You bought `{amount}` Nora medal(s) welcome to the money gang', color=discord.Color.dark_blue())
                e.set_author(name=f"{member}", icon_url=member.avatar_url)
                await ctx.send(embed=e)
                return
    
    async def buy_nr_trophy(self, ctx, member, amount):
        ctx_data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        ls = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "nr_trophy")
        ls_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "nr_trophy")
        value = int(50000000*amount)
        if not ctx_data:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        if value > ctx_data["wallet"]:
            e = discord.Embed(description=f"You are trying to buy an item costing more money than you have\n{value}   is the price!", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        else:
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", ctx_data["wallet"] - value, member.id)
            if not ls_data:
                amt = int(amount)
                await self.bot.db.execute("INSERT INTO inve(user_id, item, amt) VALUES($1, $2, $3)", member.id, "nr_trophy", amt)
                e = discord.Embed(title=f"Bought Item(s)", description=f'You bought `{amount}` Nora trophy/trophies welcome to the elite gang', color=discord.Color.dark_blue())
                e.set_author(name=f"{member}", icon_url=member.avatar_url)
                await ctx.send(embed=e)
                return
            if ls_data:
                amt = int(amount) + ls_data['amt']
                await self.bot.db.execute("UPDATE inve SET amt = $1 WHERE user_id = $2 AND item = $3", amt, ctx.author.id, "nr_trophy")
                e = discord.Embed(title=f"Bought Item(s)", description=f'You bought `{amount}` Nora trophy/trophies welcome to the elite gang', color=discord.Color.dark_blue())
                e.set_author(name=f"{member}", icon_url=member.avatar_url)
                await ctx.send(embed=e)
                returns
    
    async def player_kill(self, ctx, member, item, msg):
        ls = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "life_saver")
        ls_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "life_saver")
        if not ls:
            await self.bot.db.execute("DELETE FROM inve WHERE user_id = $1", member.id)
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", 0, member.id)
            e = discord.Embed(title="You died", description=msg, color=discord.Color.dark_blue())
            await ctx.send(embed=e)
        if ls:
            if ls_data["amt"] == 1:
                e = discord.Embed(description=f"You almost died {item} but you were saved by your life saver!", color=discord.Color.dark_blue())
                await ctx.send(embed=e)
                await self.bot.db.execute("DELETE FROM inve WHERE user_id = ($1) AND item = ($2)", member.id, "life_saver")
                return
            if 1 < ls_data["amt"]:
                e = discord.Embed(description=f"You almost died {item} but you were saved by your life saver!", color=discord.Color.dark_blue())
                await ctx.send(embed=e)
                await self.bot.db.execute("UPDATE inve SET amt = $1 WHERE user_id = $2 AND item = $3", ls_data["amt"] - 1, member.id, "life_saver")
                return
        
    async def use_alcohol(self, ctx, member):
        data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        alcohol = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "alcohol")
        a_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "alcohol")
        if not alcohol:
            await ctx.send("You have no alcohol to drink..")
            return
        if a_data["amt"] == 1:
            await self.bot.db.execute("DELETE FROM inve WHERE user_id = ($1) AND item = ($2)", ctx.author.id, "alcohol")
        if 1 < a_data["amt"]:
            await self.bot.db.execute("UPDATE inve SET amt = $1 WHERE user_id = $2 AND item = $3", a_data["amt"] - 1, ctx.author.id, "alcohol")
        if random.randint(1, 100) < 20:
            amt = random.randint(250, 1000)
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] + amt, ctx.author.id)
            e = discord.Embed(title="You drank alcohol", description=f"You got some new friends and they gave you {amt}  !", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        if random.randint(1, 100) < 30:
            await self.player_kill(ctx ,ctx.author, 'drinking alcohol','You fell into the river on alcohol and drowned, All your walllet money was lost!')
            return
        if random.randint(1, 100) < 100:
            walt_1 = data["wallet"]
            walt_2 = 0.5*walt_1
            amt = random.randint(int(walt_2), walt_1)
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] - amt, ctx.author.id)
            e = discord.Embed(title="You drank alcohol", description=f"You got way to drunk and a random guy robbed you of {amt}", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        
    async def busk_guitar(self, ctx, member):
        data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        gui = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "guitar")
        g_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "guitar")
        val = random.randint(100, 1000)
        if not gui:
            await ctx.send("You dont have a guitar to go busking with")
            return
        if random.randint(1, 100) < 20:
            await self.bot.db.execute("DELETE FROM inve WHERE user_id = ($1) AND item = ($2)", ctx.author.id, "guitar")
            await ctx.send("You dropped your guitar and it got ran over by a car , poor you.")
            return
        else:
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] + val, ctx.author.id)
            e = discord.Embed(title="You busked", description=f"You got {val}   by strumming your guitar. You will do anything for money , people  these days..", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
    
    async def busk_drum(self, ctx, member):
        data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        gui = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "drum")
        g_data = await self.bot.db.fetchrow("SELECT * FROM inve WHERE user_id = $1 AND item = $2", member.id, "drum")
        val = random.randint(100, 1000)
        if not gui:
            await ctx.send("You dont have a drum to go busking with")
            return
        if random.randint(1, 100) < 20:
            await self.bot.db.execute("DELETE FROM inve WHERE user_id = ($1) AND item = ($2)", ctx.author.id, "drum")
            await ctx.send("Your drum got ran over by a car , poor you.")
            return
        else:
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] + val, ctx.author.id)
            e = discord.Embed(title="You busked", description=f"You got {val}   by playing your drum. You will do anything for money , people  these days..", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
    
    async def buy_pet(self, ctx, member, pet_name, pet_price):
        accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", member.id)
        data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", member.id)
        pet = await self.bot.db.fetch("SELECT * FROM pets WHERE user_id = $1", member.id)
        if not accounts:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", member.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{member}", icon_url=member.avatar_url)
            await ctx.send(embed=e)
        if pet:
            pet_data = await self.bot.db.fetchrow("SELECT * FROM pets WHERE user_id = $1", member.id)
            pt_name = pet_data["name"]
            pt_nick = pet_data["nick"]
            await ctx.send(f"You alredy have a pet don't you remember {pt_name}({pt_nick})?, dont tell it this but you can disown it using `nr.disownpet`")
            return
        if pet_price > data["wallet"]:
            walt = data["wallet"]
            await ctx.send(f"The {pet_name} you are trying to buy is is {pet_price}   but you only have {walt}  ")
            return
        else:
            await self.bot.db.execute("INSERT INTO pets(user_id, name, nick) VALUES($1, $2, $3)", member.id, pet_name, "No nick")
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] - pet_price, member.id)
            await ctx.send(f"Congrats!! You adopted a {pet_name} for {pet_price}. If you want to change your pet's name type `nr.petnick <NickName>`")
    
    @commands.command()
    async def petshop(self, ctx):
        e = discord.Embed(title="PET SHOP", color=discord.Color.dark_blue())
        e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        e.add_field(name="<:spotted_dog:839739554886058004> Dog —   50,000", value='Key: `dog`\nAdvantages: + 10%   while fishing', inline=False)
        e.add_field(name="<:brown_cat:839739869692428288> Cat —   75,000", value='Key: `cat`\nAdvantages: + 20%   while fishing', inline=False)
        e.add_field(name="<:blue_yellow_orange_parrot:839740445574692884> Parrot —   100,000", value='Key: `parrot`\nAdvantages: + 30%   while fishing and +10% while hunting', inline=False)
        e.add_field(name="<:red_yellow_dragon:839742030930509827> Dragon —   5,000,000", value='Key: `dragon`\nAdvantages: + 40%   while fishing and +20% while hunting', inline=False)
        await ctx.send(embed=e)
      
    @commands.group()
    async def pet(self, ctx):
        pet = await self.bot.db.fetch("SELECT * FROM pets WHERE user_id = $1", ctx.author.id)
        if not pet:
            await ctx.send("You dont have a pet to check the shop type `nr.petshop`")
            return
        if pet:
            pet_data = await self.bot.db.fetchrow("SELECT * FROM pets WHERE user_id = $1", ctx.author.id)
            pet_name = pet_data["name"]
            pet_nick = pet_data["nick"]
            e = discord.Embed(title=f"{ctx.author.name}'s Pet", description=f"Your pet is a {pet_name}\nNickname: {pet_nick}", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
    
    @commands.command()
    async def petnick(self, ctx, *, nick):
        pet = await self.bot.db.fetch("SELECT * FROM pets WHERE user_id = $1", ctx.author.id)
        if not pet:
            await ctx.send("You dont have a pet to check the shop type `nr.petshop`")
            return
        if pet:
            await self.bot.db.execute("UPDATE pets SET nick = $1 WHERE user_id = $2", nick, ctx.author.id)
            await ctx.reply(f"Your pet's nickname is now {nick}")
            return
        else:
            await ctx.send("There was an error in command petnick: Something went wrong.")
        
    @commands.command()
    async def petdisown(self, ctx):
        pet = await self.bot.db.fetch("SELECT * FROM pets WHERE user_id = $1", ctx.author.id)
        if not pet:
            await ctx.send("You dont have a pet to check the shop type `nr.petshop`")
            return
        if pet:
            pet_data = await self.bot.db.fetchrow("SELECT * FROM pets WHERE user_id = $1", ctx.author.id)
            pt_name = pet_data["name"]
            pt_nick = pet_data["nick"]
            await ctx.reply(f"You disowned {pt_name}({pt_nick})")
            await self.bot.db.execute("DELETE FROM pets WHERE user_id = $1", ctx.author.id)
            return
        else:
            await ctx.send("There was an error in command petdisown: Something went wrong.")
    
    @commands.command()
    async def buypet(self, ctx, *, pet_name):
        if pet_name.lower() == "dog":
            await self.buy_pet(ctx, ctx.author, "dog", 50000)
            return
        if pet_name.lower() == "cat":
            await self.buy_pet(ctx, ctx.author, "cat", 75000)
            return
        if pet_name.lower() == "parrot":
            await self.buy_pet(ctx, ctx.author, "parrot", 100000)
            return
        if pet_name.lower() == "dragon":
            await self.buy_pet(ctx, ctx.author, "dragon", 5000000)
            return
        else:
            await ctx.send("That is not a valid pet please check the pet shop again!")    
                   
def setup(bot):
    bot.add_cog(Economy(bot))