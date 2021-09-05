"""
Author :  Sitanshu15
Bot : Nora
"""
from difflib import get_close_matches
import asyncio
import datetime
import io
import json
import math
import random
import time
from io import BytesIO
import re

import aiohttp
import asyncpg
import discord
import requests
import wikipedia
from discord.ext import commands
from discord.ext.commands import BucketType, Cog
from PIL import Image, ImageFilter


class Help(commands.Cog):

  def __init__(self, bot):
      self.bot = bot
      self.bot.remove_command("help")
  
  @commands.group(case_insensitive=True, invoke_without_command=True)
  async def help(self, ctx, page=None):
      if page == None:
          page = "1"
      if page == "1":
          e = discord.Embed(title="Standard Commands", description="Type `nr.help [command]` for more help eg. `nr.help beg`.\nType `nr.help moderation` (This requires for the user to have the manage_messages permission)\nror further inquiry join https://discord.gg/T4ywdPkMTE", color=discord.Color.dark_blue(), timestamp=datetime.datetime.utcnow())
          e.add_field(name=f"<a:economy_items:837216761585336362> **Items & Economy**", value="`beg, open, fish, hunt, post_meme, mine, buy, gamble, balance, deposit, withdraw, steal, buy, sell, shop, inventory, use, rich, pet, petshop, buypet, petnick, petdisown`", inline=False)
          e.add_field(name=f"<a:images:837228370160910347> **Images**", value="`pixel, colors, wanted, trigger, america, wasted, invert, triangle, hog, blur, rgb, obama, jail, rainbow, deepfry, ascii, satan, hitler, posterize, paint, pat, spin, solar, stringify, comment, tweet`", inline=False)
          e.add_field(name=f"<a:search:837237712926277643> **Internet**",value="`wiki, google, reddit, meme`", inline=False)
          e.add_field(name=f"<a:music:837255911172734996> **Music**", value="`play, connect, pause, resume, skip, stop, volume, shuffle, np, queue, swap_dj`", inline=False)
          e.add_field(name=f"<a:fun_stuff:837257046821961768> **Fun Stuff**", value="`8ball, diceroll, pie, cookie, rps, xkcd, fight, quote, ttt`")
          e.set_footer(text="Page 1/2")
          await ctx.send(embed=e)
          return
      if page == "2":
          e = discord.Embed(title="Standard Commands", description="", color=discord.Color.dark_blue(), timestamp=datetime.datetime.utcnow())
          e.add_field(name=f"<a:animals:837259365828132876> **Animals**", value="`fact, koala, panda, foxy, birb, inspireme, duck, dog, cat`", inline=False)
          e.add_field(name=f"<a:utilities:837260058839482448> **Utilities**", value="`ping, uptime, mystbin, charinro, source, invite, botinro, quickpoll, poll, strawpoll`", inline=False)
          e.set_footer(text="Page 2/2")
          await ctx.send(embed=e)
          return
  
  @help.command(case_insensetive=True)
  async def beg(self, ctx):
      await self.make_help(ctx, "beg", "None", "30 seconds", 'You can use the command beg for money and get money ranging from 0-170  ', "nr.beg")     
  
  @help.command(case_insensetive=True)
  async def mine(self, ctx):
      await self.make_help(ctx, 'mine', 'None', "1 minute 10 seconds", "Run the command and mine for nerfeli and sell them for money ranging from 1-10 X 125-150. This requires a pickaxe from the shop, and removes 3-15% from your pickaxe durability.", 'nr.mine')
  
  @help.command()
  async def fish(self, ctx):
    await self.make_help(ctx, 'fish', 'None', "1 minute 10 seconds", "Get fish to sell in the market. This requires a fishing rod from the shop.", 'nr.fish')
  
  @help.command(aliases=["pm"])
  async def postmeme(self, ctx):
    await self.make_help(ctx, 'postmeme', '`pm`', "1 minute", "Post a meme and get sweet ad revenue. This requires a laptop from the shop.", 'nr.postmeme')
  
  @help.command()
  async def hunt(self, ctx):
    await self.make_help(ctx, 'hunt', 'None', "1 minute 40 seconds", "Hunt for animals and sell them for moneyy!. This requires a hunting rifle from the shop.", 'nr.hunt')
  
  @help.command(aliases=["bet"])
  async def gamble(self, ctx):
    await self.make_help(ctx, 'gamble', '`bet`', "50 seconds", "Gamble and loose or win against me, btw dont gamble in real life", 'nr.gamble')
  
  @help.command(aliases=["bal"])
  async def balance(self, ctx):
    await self.make_help(ctx, 'balance', '`bal`', "None", "Check someone's balance if none it will show you yours!", 'nr.balance [member]')
  
  @help.command(aliases=["dep"])
  async def deposit(self, ctx):
    await self.make_help(ctx, 'deposit', '`dep`', "None", "Deposit money to your bank", 'nr.deposit <amt, max, half>')

  @help.command(aliases=['wd', 'with'])
  async def withdraw(self, ctx):
    await self.make_help(ctx, 'withdraw', '`wd, with`', "None", "Withdraw money from your bank", 'nr.withdraw <amt, max, half>')
  
  @help.command(aliases=["rob"])
  async def steal(self, ctx):
    await self.make_help(ctx, 'steal', '`rob`', "35 seconds", "Steal money from given members", 'nr.steal <member>')
  
  @help.command()
  async def buy(self, ctx):
    await self.make_help(ctx, 'buy', 'None', "None", "Buy items given in the shop nr.shop for the list of items", 'nr.buy <name> <amt>')
  
  @help.command()
  async def shop(self, ctx):
    await self.make_help(ctx, 'shop', 'None', "None", "Get the list of items to buy with nr.buy. If page is none it's going to show you the first page", 'nr.shop [page]')
  
  @help.command(aliases=['inv'])
  async def inventory(self, ctx):
    await self.make_help(ctx, 'inventory', '`inv`', "None", "Check someone's inventory if none it's going to show your's", 'nr.inventory [member]')
  
  @help.command()
  async def use(self, ctx):
    await self.make_help(ctx, 'use', 'None', "35 seconds", "Use an item you have from the shop!, find the usage key in the shop to find items to use", 'nr.use <item>')
  
  @help.command(aliases=["leaderboard, lb"])
  async def rich(self, ctx):
   await self.make_help(ctx, 'rich', '`leaderboard, lb`', "None", "Get the list of the richest  10", 'nr.rich')
  
  @help.command(aliases=["av"])
  async def avatar(self, ctx):
    await self.make_help(ctx, 'avatar', '`av`', "None", "Look at someones avatar, if member is none it will show yours!", 'nr.avatar [member]')
  
  @help.command(aliases=["pixelate"])
  async def pixel(self, ctx):
    await self.make_help(ctx, 'pixel', '`pixelate`', "45 seconds", "Pixelate mentioned user's avatar, if member is none it will show yours", 'nr.pixel [member]')

  @help.command()
  async def colors(self, ctx):
    await self.make_help(ctx, 'colors', 'None', "45 seconds", "Show the colors of the given user's avatar, if member is none it will show yours", 'nr.colors [member]')

  @help.command(aliases=["want"])
  async def wanted(self, ctx):
    await self.make_help(ctx, 'wanted', '`want`', "45 seconds", "Adds a wanted sorta filter to given user's avatar, if member is none it will show yours", 'nr.wanted [member]')
  
  @help.command()
  async def trigger(self, ctx):
    await self.make_help(ctx, 'trigger', '`triggred`', "45 seconds", "Adds a triggered filter to given user's avatar, if member is none it will show yours'", 'nr.trigger [member]')
  
  @help.command()
  async def america(self, ctx):
    await self.make_help(ctx, 'america', 'None', "cd", "desc", 'nr.america')
  
  
  async def make_help(self, ctx, command, aliases, cooldown, description, usage):
      e = discord.Embed(title=f"Help for {command}", description=f"`{description}`", color=discord.Color.dark_blue(), timestamp=datetime.datetime.utcnow())
      e.add_field(name=f"Usage", value=f"> `{usage}`")
      e.add_field(name=f"Cooldown/Aliases", value=f"> Aliases: `{aliases}`\n> Cooldown: `{cooldown}`")
      e.set_footer(text=f"<> => Required | [] => Optional", icon_url=ctx.author.avatar.url)
      await ctx.send(embed=e)
  
def setup(bot):
  bot.add_cog(Help(bot))