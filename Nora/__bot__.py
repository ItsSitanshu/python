EXTENSIONS = (
    "cogs.imp",
    "cogs.cb",
    "cogs.econ",
    "cogs.emoji",
    "cogs.events",
    "cogs.eval",
    "cogs.fun",
    "cogs.help",
    "cogs.image",
    "cogs.internet",
    "cogs.maths",
    "cogs.misc",
    "cogs.mod", 
    "cogs.music",
    "cogs.owner",
    "cogs.polls",
    "cogs.reddit",
    "cogs.ttt",
    "cogs.cooled",
    "cogs.test",
    "jishaku"
)
import asyncio
import datetime
import functools
import logging
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
import humanize
import paginator
import requests
import wavelink
import wikipedia
import xkcd_wrapper
from asyncdagpi import Client, ImageFeatures
from discord.ext import commands
from discord.ext.commands import BucketType, Cog, Greedy
from googletrans import Translator
from googletrans.constants import LANGUAGES
from jishaku.codeblocks import codeblock_converter

from jishaku.functools import executor_function
from mystbin import Client
from PIL import Image, ImageFilter
from requests.utils import quote

#https://github.com/saghul/aiodns/issues/78
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#Nora's Heart ❤
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="nr.", intents=intents, owner_ids=[814030950597132321], case_insensitive=True)
with open('config.json') as config_file:
    data = json.load(config_file)
TOKEN = data['discord_token']
PSQL_PASSWORD = data['psql_password']

async def create_db_pool():
    bot.db = await asyncpg.create_pool(database="Nora", user="postgres", password=PSQL_PASSWORD)

@bot.event
async def on_ready():
    print(f"Project {bot.user.name} running...\nDeployment:{datetime.datetime.utcnow()}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"to {len(bot.users)} members"))

for ext in EXTENSIONS:
    try:
        bot.load_extension(ext)
    except Exception as err:
        print(f"{type(err).__name__} - {err}")

#Run Nora
bot.loop.create_task(create_db_pool())
bot.run(TOKEN)