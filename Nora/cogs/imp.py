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

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, ".")


class Importaint(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="blacklist", aliases=["bl", "imprison", "ip"])
    @commands.is_owner()
    async def _blacklist(self, ctx):
        pass
    
    @_blacklist.command()
    async def add(self, ctx, user: discord.Member, *, reason):
        if reason is None:
            await ctx.reply("Provide a reason please!")
        await self.bot.db.execute("INSERT INTO bl(user_id, reason) VALUES($1, $2)", user.id, reason)
        e =  discord.Embed(title = f"{user} was black-listed", description = f"Responsible Dev's name: {ctx.author}\nfesponsible Dev's id: {ctx.author.id}\nMember's  name: {user}\nMember's ID: {user.id}\nfeason: {reason}\nGuild Name: {ctx.guild.name}\nGuild ID: {ctx.guild.id}", color = discord.Color.dark_blue())
        e.set_thumbnail(url=f"{user.avatar_url}")
        await ctx.send(embed=e)

    @commands.command()
    async def request(self, ctx, *, reason):
        req = await self.bot.db.fetch("SELECT * FROM aproval WHERE user_id = $1", ctx.author.id)
        if req:
            await ctx.send("You already have sent the request")
            return
        if not req:
            await ctx.send(f"Alright, I will send that report to the support server. {ctx.author.mention}")
            report_channel = self.bot.get_channel(839846992045801523)
            e = discord.Embed(title="New request", description=f"`nf.approve {ctx.author.id}` to accept it!", color=discord.Color.dark_blue())
            e.add_field(name=f"Member Name", value=ctx.author)
            e.add_field(name=f"Reason for request", value=reason)
            await self.bot.db.execute("INSERT INTO aproval(user_id) VALUES($1)", ctx.author.id)
            await report_channel.send(embed=e)
    
    @commands.command()
    @commands.has_role(834786504001060914)
    async def approve(self, ctx, member: int):
        econ = await self.bot.db.fetch("SELECT * FROM econ WHERE user_id = $1", member)
        inve = await self.bot.db.fetch("SELECT * FROM inve WHERE user_id = $1", member)
        pets = await self.bot.db.fetch("SELECT * FROM pets WHERE user_id = $1", member)
        req = await self.bot.db.fetch("SELECT * FROM aproval WHERE user_id = $1", member)
        if req: 
            if econ:
                await self.bot.db.execute("DELETE FROM econ WHERE user_id = ($1)", member)
            if inve:
                await self.bot.db.execute("DELETE FROM inve WHERE user_id = ($1)", member)
            if pets:
                await self.bot.db.execute("DELETE FROM pets WHERE user_id = ($1)", member)
            await ctx.send(f"DONE i have removed {member} from my database")
            await self.bot.db.execute("DELETE FROM aproval WHERE user_id = ($1)", member)
            return
        if not req:
            await ctx.send("They have not requested a remove!")
            return
        else:
            pass
        
            
    
def setup(bot):
    bot.add_cog(Importaint(bot))
