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
#from discord.ext.buttons import Paginator
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
            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=e)
        earnings=random.randint(1500, 20000)
        await self.bot.db.execute("UPDATE econ SET wallet = $1 WHERE user_id = $2", data["wallet"] + earnings, ctx.author.id)
        await ctx.send(f"Congratulations {ctx.author.mention}! You got {earnings}   claim your next one after **24** hours!")

def setup(bot):
    bot.add_cog(Cooled(bot))