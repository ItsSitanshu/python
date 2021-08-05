"""
Author :  Sitanshu15
Bot : Nora
"""
import sys
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
from prettytable import PrettyTable
from requests.utils import quote

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, ".")


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener(name="cog_command_error")
    async def _cog_error(self, ctx, error):
        if isinstance(error, aiohttp.client_exceptions.ContentTypeError):
            embed = discord.Embed(title="Error", description="There was an error, please try again later", Color=discord.Color.dark_blue())
            await ctx.send(embed=embed)
        else:
            pass
    
    @commands.is_owner()
    @commands.group(name="sql", invoke_without_command=True)
    async def sql(self, ctx, *, command):
        res = await self.bot.db.fetch(command)
        if len(res) == 0:
            return await ctx.send("Query finished successfully No results to display")
        headers = list(res[0].keys())
        table = PrettyTable()
        table.field_names = headers
        for record in res:
            lst = list(record)
            table.add_row(lst)
        msg = table.get_string()
        await ctx.send(f"```\n{msg}\n```")

    @sql.command()
    async def show(self,ctx, w:str):
        if w == "tables":
            cmd = await self.bot.get_command("sql")
            await cmd(ctx,)

    @sql.error
    async def sql_error_handling(self,ctx,error):
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
            if isinstance(error, asyncpg.exceptions.UndefinedTableError):
                return await ctx.send("The table does not exists")
            elif isinstance(error, asyncpg.exceptions.PostgresSyntaxError):
                return await ctx.send(f"syntax error ```\n {error} ```")
            else:
                await ctx.send(error)
        else:
            await ctx.send(error)
    
    @commands.command(hidden=True, aliases=["l"])
    @commands.is_owner()
    async def load(self, ctx, *, cog=None):
        try:
            self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            e = discord.Embed(title=f"{cog}.py raised an error <:python:596577462335307777>", description='{}: {}'.format(type(e).__name__, e), color=discord.Color.dark_blue())
            em = await ctx.send(embed=e)
            await em.add_reaction('<a:nrnop:826064891101446184>')
        else:
            e = discord.Embed(title=f"{cog}.py was loaded <:python:596577462335307777>", color=discord.Color.green())
            em = await ctx.send(embed=e)
            await em.add_reaction('<a:nryep:826064891253096488>')
    
    @commands.command(aliases=['reload'], hidden=True)
    @commands.is_owner()
    async def r(self, ctx, *, cog=None):
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            e = discord.Embed(title=f"{cog}.py raised an error <:python:596577462335307777>", description='{}: {}'.format(type(e).__name__, e), color=discord.Color.dark_blue())
            em = await ctx.send(embed=e)
            await em.add_reaction('<a:nrnop:826064891101446184>')
        else:
            e = discord.Embed(title=f"{cog}.py was reloaded <:python:596577462335307777>", color=discord.Color.green())
            em = await ctx.send(embed=e)
            await em.add_reaction('<a:nryep:826064891253096488>')
    

    @commands.command(hidden=True, aliases=['u'])
    @commands.is_owner()
    async def unload(self, ctx, *, cog=None):
        try:
            self.bot.unload_extension(f"cogs.{cog}")
        except Exception as e:
            e = discord.Embed(title=f"{cog}.py raised an error", description='{}: {}'.format(type(e).__name__, e), color=discord.Color.dark_blue())
            em = await ctx.send(embed=e)
            await em.add_reaction('<a:nrnop:826064891101446184>')
        else:
            e = discord.Embed(title=f"{cog}.py was unloaded", color=discord.Color.green())
            em = await ctx.send(embed=e)
            await em.add_reaction('<a:nryep:826064891253096488>')
    
    
    @commands.command(name="toggle")
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        command = self.bot.get_command(command)

        if command is None:
            await ctx.send("I can't find a command with that name!")
            await ctx.message.add_reaction('<a:nrnop:826064891101446184>')

        elif ctx.command == command:
            await ctx.send("You cannot disable this command.")
            await ctx.message.add_reaction('<a:nrnop:826064891101446184>')

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send(f"I have {ternary} {command.qualified_name} for you!")
            await ctx.message.add_reaction('<a:nryep:826064891253096488>')
    
    @commands.command(name="kys", aliases=["shutdown"])
    @commands.is_owner()
    async def _kys(self, ctx):
        msg = await ctx.send("K bye.")
        await self.bot.close()
    
    async def restart_program():
        python = sys.executable
        os.execl(python, python, * sys.argv)

    @commands.command()
    @commands.is_owner()
    async def reboot(self, ctx):
        await ctx.send("Restarting... This may take some time")
        await self.restart_program()
    
def setup(bot):
    bot.add_cog(Owner(bot))