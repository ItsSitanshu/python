"""
Author :  Sitanshu15
Bot : Nora
"""
import asyncio
import datetime
import difflib
import functools
import io
import json
import math
import os
import random
import re
import textwrap
import time
import typing
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



class Cooled(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        data = await self.bot.db.fetchrow("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        accounts = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", ctx.author.id)
        if not accounts:
            await self.bot.db.execute("INSERT INTO econ(user_id, bank, wallet) VALUES($1, 250, 125)", ctx.author.id)
            e = discord.Embed(title="Ayo, i've opened a account for you!", description="Go ahead and run the beg command to get started", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
        earnings=random.randint(1500, 20000)
        await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] + earnings, ctx.author.id)
        await ctx.send(f"Congratulations {ctx.author.mention}! You got {earnings}   claim your next one after **24** hours!")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def stocks(self, ctx, amount=None):
        stock_cmpny = ["AETNA INC", "ANTHEM INC", "APPLE INC", "ASPEN INSURANCE HOLDINGS LTD", "BARRICK GOLD CORP", "BEST BUY CO INC", "CAREFUSION CORP", "CBS CORP-CLASS B NON VOTING", "CIGNA CORP", "COMPUTER SCIENCES CORP", "COMPUWARE CORP", "COVENTRY HEALTH CARE INC", "DELPHI AUTOMOTIVE PLC", "DST SYSTEMS INC", "EINSTEIN NOAH RESTAURANT GRO", "ENSCO PLC-CL A", "EXPEDIA INC", "FIFTH STREET FINANCE CORP", "GENERAL MOTORS CO", "GENWORTH FINANCIAL INC-CL A", "GREEN BRICK PARTNERS INC", "HESS CORP", "HUMANA INC", "HUNTINGTON INGALLS INDUSTRIE", "LEGG MASON INC", "MARKET VECTORS GOLD MINERS", "MARVELL TECHNOLOGY GROUP LTD", "MICROSOFT CORP", "NCR CORPORATION", "NVR INC", "OAKTREE CAPITAL GROUP LLC", "REPUBLIC AIRWAYS HOLDINGS IN", "SEAGATE TECHNOLOGY", "SPRINT COMMUNICATIONS INC", "STARZ - A", "STATE BANK FINANCIAL CORP", "SYMMETRICOM INC", "TESSERA TECHNOLOGIES INC", "UNITEDHEALTH GROUP INC","VIRGIN MEDIA INC/OLD"]
        stock = f"{random.choice(stock_cmpny)}"
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
        if int(amount) > data["wallet"]:
            e = discord.Embed(description=f"Please enter a valid amount you are trying to invest more than you have", color=discord.Color.dark_blue())
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
            return
        if random.randint(1, 100) < 65:
            e = discord.Embed(title="Aigh't give me 30 seconds", description=f"Ill scower around the `{stock}` and check if you profit or not", color=discord.Color.dark_blue())
            msg = await ctx.send(embed=e)
            await asyncio.sleep(30)
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] - int(amount), ctx.author.id)
            await msg.reply(f"Lol, you lost {amount}   to {stock}")
            return
        if random.randint(1, 100) < 35:
            amt = int(amount) * 3
            e = discord.Embed(title="Aigh't give me 30 seconds", description=f"Ill scower around the `{stock}` and check if you profit or not", color=discord.Color.dark_blue())
            msg = await ctx.send(embed=e)
            await asyncio.sleep(30)
            await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] + amt, ctx.author.id)
            await msg.reply(f"Epic, you prodited {amt}   to `{stock}`")
            return

def setup(bot):
    bot.add_cog(Cooled(bot))