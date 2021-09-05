"""
Author :  Sitanshu15
Bot : Nora
"""
import asyncio
import datetime
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
from discord.ext.commands import BucketType, Cog
from dotenv import load_dotenv
from jishaku.codeblocks import codeblock_converter
from jishaku.functools import executor_function
from mystbin import Client
from PIL import Image, ImageFilter
from requests.utils import quote


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.mystbin = Client()
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            retry = humanize.precisedelta(error.retry_after, minimum_unit='seconds')
            cd = error.cooldown
            command = ctx.invoked_with
            e = discord.Embed(title=f"Command is on cooldown", description=f"<:alert:831806558311677962> The {command} command is on cooldown. Try again in **{retry}**.", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
        if isinstance(error, commands.errors.CommandInvokeError):
            print(error)
        if isinstance(error, commands.errors.NotOwner):
            await ctx.reply("You are not the owner or dev")
    
    @commands.Cog.listener(name="on_message_edit")
    async def _reinvoke_commands(self, before, after):
        if after.content != before.content:
            await self.bot.process_commands(after)
            
def setup(bot):
    bot.add_cog(Events(bot))
