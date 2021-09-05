"""
Author :  Sitanshu15
Bot : Nefeli
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


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.sauce_session = aiohttp.ClientSession()
        self.bot.launch_time = datetime.datetime.utcnow()
        self.mystbin = Client()
        self.xkcd = xkcd_wrapper.AsyncClient()
    
    @commands.Cog.listener(name="cog_command_error")
    async def _cog_error(self, ctx, error):
        if isinstance(error, aiohttp.client_exceptions.ContentTypeError):
            embed = discord.Embed(title="Error", description="There was an error, please try again later", color=discord.Color.dark_blue())
            await ctx.send(embed=embed)
        else:
            raise


    @commands.command(case_insensitive=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ping(self, ctx):
        typstart = time.perf_counter()
        msg = await ctx.send("Ponging..")
        typend = time.perf_counter()
        typduration = (typend - typstart) * 1000
        e = discord.Embed(title="Pong!",color=discord.Color.dark_blue())
        e.add_field(name="<:nefeli:835016513543077909> | Bot latency",value=f"`{round(self.bot.latency * 1000)}` ms", inline=False)
        start = time.perf_counter()
        await self.bot.db.fetch("SELECT 1")
        theTime = (time.perf_counter() - start)*1000
        e.add_field(name="<a:typing:597589448607399949> | Typing Latency", value=f"`{round(typduration)}` ms", inline=False)
        e.add_field(name="<:postgresql:828304901964169236> | PostgreSQL Latency",value=f"`{round(theTime)}` ms", inline=False)
        await msg.edit(embed=e, content=None)

    @commands.command(aliases=["ui"])
    async def userinfo(self, ctx, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        member = member or ctx.author
        embed = discord.Embed(title=f"Userinfo for {member}", colour=member.colour)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="General",value=f"**Full Name:** {member}\n**ID:** {member.id}\n**Nickname:** {member.nick}\n**Display Name:** {member.display_name}", inline=False)
        activity = f"{str(member.activity.type).split('.')[1].title()} {member.activity.name}" if member.activity else "None"
        embed.add_field(name="Presence Info",value=f"**Activity:** {activity}", inline=False)
        r = "".join(role.mention for role in member.roles)
        embed.add_field(name="Guild Info",value=f"**Joined:** {humanize.naturaldate(member.joined_at)} ({humanize.precisedelta(datetime.datetime.now() - member.joined_at)} ago)\n**Top Role:** {member.top_role.mention}\n**Roles:**{r}",inline=False)
        embed.add_field(name="Avatar History", value=f"https://krix.xyz/discord/avatarhistory/{ctx.author.id}")
        embed.set_footer(text=f"Created {humanize.precisedelta(datetime.datetime.now() - member.created_at)} ago")
        await ctx.send(embed=embed)
        
    @commands.command(name="8ball", case_insensitive=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def _ball(self, ctx,* ,question:str):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        results8ball = ["It is certain"," It is decidedly so","Without a doubt","Yes, definitely","You may rely on it","As I see it, yes"," Most likely","Outlook good","Yes","Signs point to yes"," Reply hazy try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","My sources say no","Outlook not so good","Very doubtful"]
        await ctx.send(f"The 🎱 says: **{random.choice(results8ball)}** | {ctx.author.name}")

    @commands.command(case_insensitive=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def diceroll(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        resultsdroll = ["1","2","3","4","5","6"]
        await ctx.send(f"{random.choice(resultsdroll)} | {ctx.author.name}")
    
    @commands.command(case_insensitive = True, aliases=['w', 'wiki'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def wikipedia(self, ctx, *, query: str):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        sea = await self.bot.session.get(
            ('https://en.wikipedia.org//w/api.php?action=query'
                '&format=json&list=search&utf8=1&srsearch={}&srlimit=5&srprop='
            ).format(query))
        sea = await sea.json()
        sea = sea['query']
        if sea['searchinfo']['totalhits'] == 0:
            await ctx.send('Sorry, your search could not be found.')
        else:
            for x in range(len(sea['search'])):
                article = sea['search'][x]['title']
                req = await self.bot.session.get('https://en.wikipedia.org//w/api.php?action=query'
                                    '&utf8=1&redirects&format=json&prop=info|images'
                                    '&inprop=url&titles={}'.format(article))
                req = await req.json()
                req = req['query']['pages']
                if str(list(req)[0]) != "-1":
                    break
            else:
                await ctx.send('Sorry, your search could not be found.')
                return
            article = req[list(req)[0]]['title']
            arturl = req[list(req)[0]]['fullurl']
            artdesc = await self.bot.session.get('https://en.wikipedia.org/api/rest_v1/page/summary/'+article)
            artdesc = await artdesc.json()
            artdesc = artdesc['extract']
            lastedited = datetime.datetime.strptime(req[list(req)[0]]['touched'], "%Y-%m-%dT%H:%M:%SZ")
            embed = discord.Embed(title='**'+article+'**', url=arturl, description=artdesc, color=discord.Color.dark_blue())
            embed.set_footer(text='Wiki entry last modified',
                                icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
            embed.set_author(name='Wikipedia', url='https://en.wikipedia.org/',
                                icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            embed.timestamp = lastedited

            await ctx.send('Search result for {}'.format(query), embed=embed)
        

    @commands.command(case_insensitive=True, aliases=["meow"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def cat(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        response = await self.bot.session.get('https://aws.random.cat/meow')
        data = await response.json()
        catt = ["Prr", "meowww", "Here's one"]
        embed = discord.Embed(
            title = f'{random.choice(catt)} 🐈',
            Color = discord.Color.dark_blue()
            )
        embed.set_image(url=data['file'])
        embed.set_footer(text='By https://aws.random.cat/meow')            
        await ctx.send(embed=embed)
        await response.session.close()

    @commands.command(case_insensitive=True, aliases=["woof"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def dog(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        r = await self.bot.session.get("https://dog.ceo/api/breeds/image/random")
        res = await r.json()
        m = discord.Embed(title="Woof 🐶", color=discord.Color.dark_blue())
        m.set_image(url=res["message"])
        m.set_footer(text='By https://dog.ceo')
        await ctx.send(embed = m)

        
    @commands.command(case_insensitive=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def duck(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        async with self.bot.session as cs:
            async with cs.get('https://random-d.uk/api/random?format=json') as r:
                res = await r.json()  
                embed = discord.Embed(title='Here is a duck!', color=discord.Color.dark_blue())
                embed.set_image(url=res["url"])
                embed.set_footer(text='By https://random-d.uk', icon_url='https://avatars2.githubusercontent.com/u/38426912')
                await ctx.send(embed=embed)


    @commands.command(case_insensitive=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def inspireme(self, ctx): 
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        async with self.bot.session as cs:
            async with cs.get('http://inspirobot.me/api?generate=true') as r:
                res = await r.text()
                embed = discord.Embed(title='An inspirational image...', color=discord.Color.dark_blue())
                embed.set_image(url=res)
                embed.set_footer(text='By https://inspirobot.me', icon_url='https://inspirobot.me/website/images/inspirobot-dark-green.png')
                await ctx.send(embed=embed)
    
    @commands.command(case_insensitive=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def birb(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        r = await self.bot.session.get("https://some-random-api.ml/img/birb")
        res = await r.json()
        m = discord.Embed(title="Chirp! 🐦", color=discord.Color.dark_blue())
        m.set_image(url=res["link"])
        m.set_footer(text='By https://some-random-api.ml/img/birb')
        await ctx.send(embed = m)
    
    @commands.command(case_insensitive=True, aliases=["fox"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def foxy(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        r = await self.bot.session.get("https://some-random-api.ml/img/fox")
        res = await r.json()
        m = discord.Embed(title="Foxy! 🦊", color=discord.Color.dark_blue())
        m.set_image(url=res["link"])
        m.set_footer(text='By https://some-random-api.ml/img/fox')
        await ctx.send(embed = m)
    
    @commands.command(case_insensitive=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def panda(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        r = await self.bot.session.get("https://some-random-api.ml/img/panda")
        res = await r.json()
        m = discord.Embed(title="Awww 🐼", color=discord.Color.dark_blue())
        m.set_image(url=res["link"])
        m.set_footer(text='By https://some-random-api.ml/img/panda')
        await ctx.send(embed = m)

    
    @commands.command(case_insensitive=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def koala(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        r = await self.bot.session.get("https://some-random-api.ml/img/koala")
        res = await r.json()
        m = discord.Embed(title="I am a koala and i sleep all the time , So what its cute! 🐨", color=discord.Color.dark_blue())
        m.set_image(url=res["link"])
        m.set_footer(text='By https://some-random-api.ml/img/koala')
        await ctx.send(embed = m)

    
    @commands.command(case_insensitive = True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def choose(self, ctx, *choices: str):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        await ctx.send(f'My choice is : \n{random.choice(choices)}')

    @commands.command(case_insensitive = True)
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def pie(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        embed = discord.Embed(title='Catch the Pie!🥧', color=discord.Color.dark_blue(), description='3')
        msg = await ctx.send(embed=embed)
        for x in ['2', '1']:
            await asyncio.sleep(1)
            embed.description = x
            await msg.edit(embed=embed)
        await asyncio.sleep(1)
        embed.description = 'NOW'
        await msg.edit(embed=embed)
        await msg.add_reaction('\U0001f967')
        time_perf = time.perf_counter()
        def check(reaction, user):
            return str(reaction.emoji) == '🥧' and user.name != self.bot.user.name
        
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        embed.description = user.name + ' got it in ' + str(round((time.perf_counter()-time_perf) * 1000, 6)) + 'ms'
        await msg.edit(embed=embed)
        bin = self.bot.get_channel(820989015691755560)
        await bin.send(f"{reaction}")
    
    @commands.command(case_insensitive = True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def cookie(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        embed = discord.Embed(title='Catch the Cookie!🍪', color=discord.Color.dark_blue(), description='3')
        msg = await ctx.send(embed=embed)
        for x in ['2', '1']:
            await asyncio.sleep(1)
            embed.description = x
            await msg.edit(embed=embed)
        await asyncio.sleep(1)
        embed.description = 'NOW'
        await msg.edit(embed=embed)
        await msg.add_reaction('🍪')
        time_perf = time.perf_counter()
        def check(reaction, user):
            return str(reaction.emoji) == '🍪' and user.name != self.bot.user.name
        
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        embed.description = user.name + ' got it in ' + str(round((time.perf_counter()-time_perf) * 1000, 6)) + 'ms'
        await msg.edit(embed=embed)
        bin = self.bot.get_channel(820989015691755560)
        await bin.send(f"{reaction}")

    @commands.command(aliases=['rock_paper_sissors'])
    async def rps(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        rpsGame = ['rock', 'paper', 'scissors']
        e = discord.Embed(title=f"{ctx.author.name}Lets start", description=f"Choose one Rock <:prock:821286380097372160> , Paper <:ppaper:821286380868468736>  , Scissors <:pscissors:821287611430862858> ")
        e.set_thumbnail(url=f"https://media.giphy.com/media/5k5eVRip9rRaygwCXY/giphy.gif")
        await ctx.send(embed=e)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

        user_choice = (await self.bot.wait_for('message', check=check)).content

        comp_choice = random.choice(rpsGame)
        if user_choice == 'rock':
            if comp_choice == 'rock':
                await ctx.send(f'Well, that was weird. We tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(f'Nice try, but I won that time!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(f"Aw, you beat me. It won't happen again!\nYour choice: {user_choice}\nMy choice: {comp_choice}")

        elif user_choice == 'paper':
            if comp_choice == 'rock':
                await ctx.send(f'The pen beats the sword? More like the paper beats the rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(f'Oh, wacky. We just tied. I call a rematch!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(f"Aw man, you actually managed to beat me.\nYour choice: {user_choice}\nMy choice: {comp_choice}")

        elif user_choice == 'scissors':
            if comp_choice == 'rock':
                await ctx.send(f'HAHA!! I JUST CRUSHED YOU!! I rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(f'Bruh. >: |\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(f"Oh well, we tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}")
    
    @commands.command()
    async def uptime(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        e = discord.Embed(title=f"I've been up  for {days}d, {hours}h, {minutes}m, {seconds}s", color=discord.Color.dark_blue())
        await ctx.send(embed=e)

    @commands.command(name="mystbin")
    async def _mystbin(self, ctx, *, text: codeblock_converter):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        if text[1].strip("\n").startswith("https://mystb.in/") or text[1].strip("\n").startswith("http://mystb.in/"):
            paste = await self.mystbin.get(text[1].strip("\n").strip())
            text = f"```{paste.paste_syntax or ''}\n{paste.paste_content}```"
            embed = discord.Embed(
                title=paste.paste_id, description=text, color=discord.Color.dark_blue())
        else:
            paste = await self.mystbin.post(text[1].strip("\n"), syntax=text[0])
            embed = discord.Embed(
                title=paste.paste_id, description=f"```\n{paste.url}```", color=discord.Color.dark_blue())

        await ctx.send(embed=embed)
        
    @commands.command()
    async def xkcd(self, ctx, number: int=None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        try:
            with ctx.typing():
                if number:
                    try:
                        comic = await self.xkcd.get(number)
                    except TypeError:
                        embed = discord.Embed(title="Error!", description=f"Couldn't find comic {number}", color=discord.Color.dark_blue())
                else:
                    comic = await self.xkcd.get_random()
                
                if comic:
                    embed = discord.Embed(title=comic.title, description=f"[Comic number {comic.id}]({comic.comic_url})\n{comic.description}", color=discord.Color.dark_blue())
                    embed.set_image(url=comic.image_url)
                    embed.set_footer(text=comic.id)
        
        except:
            embed = discord.Embed(title="Error!", description="There was an error, please try again soon", color=discord.Color.dark_blue())        
        await ctx.send(embed = embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fight(self, ctx, user1: discord.Member, user2: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        if user2 is None:
            user2 = ctx.author
        owner = self.bot.get_user(814030950597132321)
        bot = self.bot.get_user(819465403461926942)
        if user1 ==bot or user2 == bot:
            return await ctx.send("I'm not fighting with anyone ✌")
        if user1 == owner or user2 == owner:
            return await ctx.send("Sitanshu beat you up so hard that you died immediately.")

        win = random.choice([user1, user2])
        lose = user2 if win == user1 else user1
        responses = [
            f'That was intense battle, but unfortunatelly {win.mention} has beaten up {lose.mention} to death',
            f'That was a rather un-exicting battle, they both fight themselves to death',
            f'Is that a battle? You both suck',
            f'Yo {lose.mention} you lose! Ha',
            f'I\'m not sure how, but {win.mention} has won the battle']

        await ctx.send(f'{random.choice(responses)}')


    @commands.command()
    async def fact(self, ctx, animal):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        r = await self.bot.session.get(f"https://some-random-api.ml/facts/{animal}")
        res = await r.json()
        fact = res["fact"]
        factfun = ["Here's a fact", "Here's one", "I bet you dint know"]
        m = discord.Embed(title=f"{random.choice(factfun)}", description=f"{fact}", color=discord.Color.dark_blue())
        await ctx.send(embed = m)
    
#PYTHON IS COOL


def setup(bot):
    bot.add_cog(Fun(bot))
