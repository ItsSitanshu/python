"""
Author :  Sitanshu15
Bot : Nora
"""
import os
import json

from asyncdagpi import Client, ImageFeatures
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp

load_dotenv()


class Images(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        DAGPI = os.getenv('DAGPI1')
        DAGPI1 = os.getenv('DAGPI')
        self.dagp = Client(DAGPI)
        self.bot.dagpi = self.dagp
        self.dagp1 = Client(DAGPI1)
        self.bot.dagpi1 = self.dagp1
        self.bot.session = aiohttp.ClientSession()

    @commands.Cog.listener(name="cog_command_error")
    async def _cog_error(self, ctx, error):
        if isinstance(error, aiohttp.client_exceptions.ContentTypeError):
            embed = discord.Embed(title="Error", description="There was an error, please try again later", Color=discord.Color.dark_blue())
            await ctx.send(embed=embed)
        else:
            raise

    @commands.command(name="avatar", aliases=["av"])
    async def _avatar(self, ctx, *, member: discord.Member = None):
        
        member = member or ctx.author
        pngurl = str(member.avatar_url_as(format="png", static_format="png", size=1024))
        jpgurl = str(member.avatar_url_as(format="jpg", static_format="jpg", size=1024))
        jpegurl = str(member.avatar_url_as(format="jpeg", static_format="jpeg", size=1024))
        webpurl = str(member.avatar_url_as(format=None, static_format="webp", size=1024))
        e = discord.Embed(title=f"{member}'s avatar", description=f"[`PNG`]({pngurl}) | [`JPG`]({jpgurl}) | [`JPEG`]({jpegurl}) | [`WEBP`]({webpurl})", color=member.color)
        e.set_image(url=f"{member.avatar_url}")
        await ctx.reply(embed=e)

    @commands.command(name="pixel", aliases=["pixelate"])
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _pixelate(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.pixel(), url)
            file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="Colors")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _Colors(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.colors(), url)
            file = discord.File(fp=img.image, filename=f"Colors.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="wanted", aliases=["want"])
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _wanted(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.wanted(), url)
            file = discord.File(fp=img.image, filename=f"wanted.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="triggered", aliases=["trigger"])
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _triggered(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.triggered(), url)
            file = discord.File(
                fp=img.image, filename=f"triggered.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="america")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _america(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        e = discord.Embed(title="This may take some time", color=discord.Color.green())
        e.set_thumbnail(url="https://media.giphy.com/media/9pUSVxrcLa3KonkdKP/giphy.gif")
        await ctx.send(embed=e)
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.america(), url)
            file = discord.File(fp=img.image, filename=f"america.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="wasted")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _wasted(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.wasted(), url)
            file = discord.File(fp=img.image, filename=f"wasted.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="invert")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _invert(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.invert(), url)
            file = discord.File(fp=img.image, filename=f"invert.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="triangle")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _triangle(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.triangle(), url)
            file = discord.File(fp=img.image, filename=f"triangle.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="hog")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _hog(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi1.image_process(ImageFeatures.hog(), url)
            file = discord.File(fp=img.image, filename=f"hog.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="blur")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _blur(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi1.image_process(ImageFeatures.blur(), url)
            file = discord.File(fp=img.image, filename=f"blur.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="rgb")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _rgb(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        e = discord.Embed(title="This may take some time", color=discord.Color.green())
        e.set_thumbnail(url="https://media.giphy.com/media/9pUSVxrcLa3KonkdKP/giphy.gif")
        await ctx.send(embed=e)
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi1.image_process(ImageFeatures.rgb(), url)
            file = discord.File(fp=img.image, filename=f"rgb.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="obama")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _obama(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        e = discord.Embed(title="This may take some time", color=discord.Color.green())
        e.set_thumbnail(url="https://media.giphy.com/media/9pUSVxrcLa3KonkdKP/giphy.gif")
        await ctx.send(embed=e)
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi1.image_process(ImageFeatures.obama(), url)
            file = discord.File(fp=img.image, filename=f"obama.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="jail")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _jail(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi1.image_process(ImageFeatures.jail(), url)
            file = discord.File(fp=img.image, filename=f"jail.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)
            
    @commands.command(name="rainbow", aliases=["gay"])
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _rainbow(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi1.image_process(ImageFeatures.gay(), url)
            file = discord.File(fp=img.image, filename=f"gay.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)
            
    @commands.command(name="deepfry")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _deepfry(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi1.image_process(ImageFeatures.deepfry(), url)
            file = discord.File(fp=img.image, filename=f"deepfry.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="ascii")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _ascii(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi1.image_process(ImageFeatures.ascii(), url)
            file = discord.File(fp=img.image, filename=f"ascii.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)
    
    @commands.command(name="satan")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _satan(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.satan(), url)
            file = discord.File(fp=img.image, filename=f"satan.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)
    
    @commands.command(name="hitler")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _hitler(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.hitler(), url)
            file = discord.File(fp=img.image, filename=f"hitler.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)
    
    @commands.command(name="swirl")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _swirl(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.swirl(), url)
            file = discord.File(fp=img.image, filename=f"swirl.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)
    
    @commands.command(name="posterize")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _posterize(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi1.image_process(ImageFeatures.posterize(), url)
            file = discord.File(fp=img.image, filename=f"posterize.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="paint")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _paint(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.paint(), url)
            file = discord.File(fp=img.image, filename=f"paint.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="night")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _night(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.night(), url)
            file = discord.File(fp=img.image, filename=f"night.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)
    
    @commands.command(name="neon")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _neon(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.neon(), url)
            file = discord.File(fp=img.image, filename=f"neon.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)
       
    @commands.command(name="pat")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _pat(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.petpet(), url)
            file = discord.File(fp=img.image, filename=f"petpet.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)
    

    @commands.command(name="spin")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _spin(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.spin(), url)
            file = discord.File(fp=img.image, filename=f"spin.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)
    
    @commands.command(name="solar")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _solar(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.solar(), url)
            file = discord.File(fp=img.image, filename=f"solar.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)

    @commands.command(name="stringify")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _stringify(self, ctx, *, member: discord.Member = None):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.stringify(), url)
            file = discord.File(fp=img.image, filename=f"stringify.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)
    
    @commands.command(name="tweet")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _tweet(self, ctx, member:discord.Member, *, tweet):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            member = member or ctx.author
            url = str(member.avatar_url_as(
                format="png", static_format="png", size=1024))
            img = await self.bot.dagpi.image_process(ImageFeatures.tweet(), url, text=tweet, username=member.name)
            file = discord.File(fp=img.image, filename=f"tweet.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)
    
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def comment(self, ctx, member: discord.Member, *,msg):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        if not member:
            member = ctx.author
        pfp = member.avatar_url_as(format='png')
        session = aiohttp.ClientSession()
        async with session.get(f"https://some-random-api.ml/canvas/youtube-comment?avatar={pfp}&username={ctx.author.name}&comment={msg}") as r:
            if r.status != 200: 
                return await ctx.send("**Unable to load image**")
            data = io.BytesIO(await r.read())
            f = discord.File(data, filename="image.png")
            e = discord.Embed()
            e.set_image(url="attachment://image.png")
            await ctx.reply(embed=e, file=f, mention_author=False)
            await session.close()
    
    @commands.command(name="makememetm")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def _makememetm(self, ctx, image, *, text):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.green())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            img = await self.bot.dagpi.image_process(ImageFeatures.modern_meme(), text=text, url=image)
            file = discord.File(fp=img.image, filename=f"modern_meme.{img.format}")
            cre_e = discord.Embed(title="Procesed by dagpi", description="In my opinion the easiest and fastest image manipulation API!\nhttps://dagpi.xyz", color=discord.Color.dark_blue())
            await ctx.reply(file=file, mention_author=False)
    
#PYTHON IS COOL

def setup(bot):
    bot.add_cog(Images(bot))