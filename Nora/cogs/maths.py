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
import googletrans
import paginator
import requests
import wavelink
import wikipedia
import xkcd_wrapper
from asyncdagpi import Client, ImageFeatures
from discord.ext import commands
from discord.ext.commands import BucketType, Cog
from dotenv import load_dotenv
from jishaku.codeblocks import codeblock_converter
from jishaku.functools import executor_function
from mystbin import Client
from PIL import Image, ImageFilter
from requests.utils import quote
#from discord.ext.buttons import Paginator

class Maths(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(case_insensitive=True, aliases=['+'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def add(self, ctx, x: float, y: float):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        res = x + y
        e = discord.Embed(title=f"{x} + {y} is = {res}", color=discord.Color.dark_blue())
        await ctx.send(embed=e)

    @commands.command(case_insensitive=True, aliases=['-'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def sub(self, ctx, x: float, y: float):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        res = x - y
        e = discord.Embed(title=f"{x} - {y} is = {res}", color=discord.Color.dark_blue())
        await ctx.send(embed=e)
    
    @commands.command(case_insensitive=True, aliases=['x'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def mult(self, ctx, x: float, y: float):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        res = x * y
        e = discord.Embed(title=f"{x} x {y} is = {res}", color=discord.Color.dark_blue())
        await ctx.send(embed=e)
    
    @commands.command(case_insensitive=True, aliases=['÷'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def div(self, ctx, x: float, y: float):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        res = x / y
        e = discord.Embed(title=f"{x} ÷ {y} is = {res}", color=discord.Color.dark_blue())
        await ctx.send(embed=e)

    @commands.command()
    async def testthee(self, ctx):
        await ctx.send(5*10+5*10*0.4)
        
def setup(bot):
    bot.add_cog(Maths(bot))
