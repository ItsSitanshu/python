"""
Author :  Sitanshu15
Bot : Nora
"""
import asyncio
import codecs
import datetime
import functools
import io
import json
import math
import os
import platform
import random
import time
import typing as t
import unicodedata
from io import BytesIO

import aiohttp
import asyncpg
import discord
import googletrans
import requests
import wavelink
import wikipedia
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.ext.commands import BucketType, Cog
from dotenv import load_dotenv
from googletrans import Translator
from googletrans.constants import LANGUAGES
from jishaku.codeblocks import codeblock_converter
from jishaku.functools import executor_function
from mystbin import Client
from PIL import Image, ImageFilter
from requests.utils import quote


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.session = aiohttp.ClientSession()
        self.trans = googletrans.Translator()
        self.mystbin = Client()
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == ("<@814030950597132321>"):
            await message.channel.send("Hey! my prefix is `nf.`")
    
    @commands.command()
    async def charinfo(self, ctx, *, characters: str):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        def to_string(c):
            digit = f'{ord(c):x}'
            name = unicodedata.name(c, 'Name not found.')
            return f'`\\U{digit:>08}`: {name} - {c} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{digit}>'
        msg = '\n'.join(map(to_string, characters))
        if len(msg) > 2000:
            return await ctx.send('Output too long to display.')
        await ctx.send(msg)
    
    @commands.command(aliases=['src'])
    async def source(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        await ctx.send("https://github.com/Sitanshu-15/Nora")
        
    @commands.command()
    async def invite(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        e = discord.Embed(title="You can invite me to your server using the links below", description=f"[`With Administrator permissions`](https://discord.com/oauth2/authorize?client_id=819465403461926942&permissions=8&scope=bot)\n[`Required permissions for all commands`](https://discord.com/oauth2/authorize?client_id=819465403461926942&permissions=4294967287&scope=bot)", color=discord.Color.dark_blue())
        await ctx.send(embed=e)
    
    @commands.command(aliases=['b.info'])
    async def botinfo(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        e = discord.Embed(title="Nora info", color=discord.Color.dark_blue())
        e.add_field(name="Servers", value=f"{len(self.bot.guilds)}")
        e.add_field(name="Members", value=f"{len(ctx.guild.members)}")
        e.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms")
        e.add_field(name="Uptime", value=f"{days}d, {hours}h, {minutes}m, {seconds}s")
        e.add_field(name="Python version",value=f"3.9.2", inline=False)
        e.add_field(name="Discord.py version", value=f"{discord.__version__}", inline=False)
        e.add_field(name="Developer(s)", value=f"[Sitanshu15#6994](https://discord.com/users/814030950597132321)", inline=False)
        e.set_thumbnail(url=f"https://images-ext-2.discordapp.net/external/h6HCqHA2-QL9hO4qvyXtAbUOQk7jBPJxCsJL8IY-AUM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/819465403461926942/232c04be93b41377cedf288b0b0cd490.png?width=682&height=682")
        await ctx.send(embed=e)
    
    @commands.command()
    @commands.cooldown(1, 40, commands.BucketType.user)
    async def quote(self, ctx, member: discord.Member, *, quote):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        e = discord.Embed(description=f'" {quote} "', color=discord.Color.dark_blue())
        e.set_author(name=member, icon_url=member.avatar_url)
        await ctx.send(embed=e)
    
    @commands.command(help="Check the socket")
    async def socket(self, ctx):
        current_time = time.time()
        lists = []
        difference = int(current_time - self.bot.start_time)/60
        lists.append(f"Received {self.bot.socket_receive} / {self.bot.socket_receive//difference} sockets per minute")
        for i, (n, v) in enumerate(self.bot.socket_stats.most_common()):
            lists.append(f"{n:<30} {v:<15} {round(v/difference, 3)} /minute")
        paginator = commands.Paginator(max_size=500, prefix="ml", suffix="")
        for i in lists:
            paginator.add_line(i)
        interface = PaginatorInterface(ctx.bot, paginator, owner=ctx.author)
        return await interface.send_to(ctx)

            
#PYTHON IS COOL
        
def setup(bot):
    bot.add_cog(Misc(bot))
