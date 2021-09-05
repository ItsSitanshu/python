"""
Author :  Sitanshu15
Bot : Nora
"""
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
#from discord.ext.buttons import Paginator
from discord.ext.commands import BucketType, Cog, Greedy
from dotenv import load_dotenv
from googletrans import Translator
from googletrans.constants import LANGUAGES
from jishaku.codeblocks import codeblock_converter

from jishaku.functools import executor_function
from mystbin import Client
from PIL import Image, ImageFilter
from requests.utils import quote



class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        
    @commands.command(case_insensitive = True, aliases=['purge', 'clean'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        if amount > 100:
            await ctx.send("This action could not be performed because you dont have premium privileges.")
            return
        else:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"Deleted {amount} messages.", delete_after = (20))
        
        
    @commands.command(case_insensitive = True, aliases=['slowmodeset', 'setslowmode'])
    @commands.has_permissions(manage_messages=True)
    async def setsm(self, ctx, seconds: int):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        await ctx.channel.edit(slowmode_delay=seconds)
        Embed=discord.Embed(title="Slow-mode",description=f"Now *s* *-* *l* *-* *o* *-* *w* *-* *m* *-* *o*  *-* *d* *-* *e*  is {seconds} seconds",color=discord.Color.dark_blue())
        await ctx.send(embed=Embed)


    @commands.command(name = "ban", aliases = ["banish"])
    @commands.has_guild_permissions(ban_members = True)
    @commands.bot_has_guild_permissions(ban_members = True)
    async def _ban(self, ctx, member: discord.Member, *, reason = None):
        e
        await ctx.message.delete()
        if reason == None:
            reason = "None"
        if member.top_role > ctx.author.top_role:
            error_embed = discord.Embed(title = "Error!", description = "You can't punish someone with a higher role than yourself!", color = discord.Color.dark_blue())
            return await ctx.reply(embed = error_embed)
        elif member == ctx.author:
            error_embed = discord.Embed(title = "Error!", description = "```diff\n-You can't ban yourself!```", color = discord.Color.dark_blue())
            return await ctx.reply(embed = error_embed)
        else:
            try:
                await member.send(f"You were banned from {ctx.guild.name}.Reason: {reason}. Moderator: {ctx.author} *(ID:{ctx.author.id})*")
                await member.ban(reason = reason)
                await ctx.send(f"**{member}** Banned")
            except discord.errors.Forbidden:
                error_embed = discord.Embed(title = "Error!", description = f"I can't ban {member.mention} because they have a higher role than me!", color = discord.Color.dark_blue())
                await ctx.reply(embed = error_embed)

    @commands.command(name = "unban", aliases = ["unbanish"])
    @commands.has_guild_permissions(ban_members = True)
    async def _unban(self, ctx, member: discord.Object, *, reason = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        await ctx.message.delete()
        if reason == None:
            reason = "None"
        try:
            await ctx.guild.unban(member, reason = reason)
            unbanned_embed = discord.Embed(title = "Success!", description = f"Successfully unbanned {member}", Color = discord.Color.dark_blue())
            return await ctx.reply(embed = unbanned_embed)

        except discord.errors.HTTPException:
            error_embed = discord.Embed(title = "Error!", description = f"Please enter the member id in the format `{self.bot.user.id}`", Color = discord.Color.dark_blue())
            return await ctx.reply(embed = error_embed)
        
    @commands.command(name = "kick", aliases = ["yeet"])
    @commands.has_guild_permissions(kick_members = True)
    async def _kick(self, ctx, member: discord.Member, *, reason = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        await ctx.message.delete()
        e =  discord.Embed(title = f"You have been kicked from{ctx.guild.name} ", description = f"Responsible Modertator/Admin's name: {ctx.author}\nfesponsible Modertator/Admin's id: {ctx.author.id}\nMember's  name: {member}\nMember's ID: {member.id}\nfeason: {reason}\nJoined discord : {member.created_at} ", color = discord.Color.dark_blue())
        e.set_thumbnail(url=f"{member.avatar.url}")
        await member.send(embed=e)
        if member.top_role > ctx.author.top_role:
            error_embed = discord.Embed(title = "Error!", description = "You can't punish someone with a higher role than yourself!", Color = discord.Color.dark_blue())
            return await ctx.reply(embed = error_embed)     
        await member.kick(reason = reason)
        e =  discord.Embed(title = f"You have been kicked from{ctx.guild.name} ", description = f"Responsible Modertator/Admin's name: {ctx.author}\nfesponsible Modertator/Admin's id: {ctx.author.id}\nMember's  name: {member}\nMember's ID: {member.id}\nfeason: {reason}\nJoined discord : {member.created_at} ", color = discord.Color.dark_blue())
        e.set_thumbnail(url=f"{member.avatar.url}")
        await member.send(embed=e, delete_after = 10)
    
    

def setup(bot):
    bot.add_cog(Mod(bot))
