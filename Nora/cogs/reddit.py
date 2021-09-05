"""
Author :  Sitanshu15
Bot : Nora
"""
import discord
from discord.ext import commands
import aiohttp
import random
import textwrap

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reddit")
    async def _reddit(self, ctx, subreddit):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            
            try:
                if subreddit.startswith("r/"):
                    subreddit = subreddit[2:]

                async with aiohttp.ClientSession() as con:
                    async with con.get(f"https://www.reddit.com/r/{subreddit}/.json") as r:
                        data = await r.json()

                if data["data"]["children"]:
                    if ctx.channel.is_nsfw():
                        for _ in range(1, 30):
                            post = random.choice(data["data"]["children"])
                            if post["data"]["domain"] == "i.redd.it" and not post["data"]["stickied"]:
                                break
                            else:
                                post = None

                    else:
                        for _ in range(1, 30):
                            post = random.choice(data["data"]["children"])
                            if post["data"]["domain"] in ["i.redd.it"] and not post["data"]["stickied"] and not post["data"]["over_18"]:
                                break
                            else:
                                post = None

                    if post:
                        embed = discord.Embed(title=textwrap.fill(
                            post["data"]["title"], width=35), url=f"https://www.reddit.com{post['data']['permalink']}", color=discord.Color.dark_blue())
                        embed.set_image(url=post["data"]["url"])
                        embed.add_field(
                            name="Upvotes", value=f"```py\n{int(post['data']['ups']) - int(post['data']['downs'])}```", inline=True)
                        embed.set_footer(
                            text=f"Uploaded by u/{post['data']['author']}", icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Error!", description=f"```diff\n- Failed getting a post from {subreddit}! (This may be because the post was a video, which is unsupported)```", color=discord.Color.dark_blue()).set_footer(text="This could be because the subreddit doesn't exist, or is private", icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- Couldn't find anything matching {subreddit}!```", color=discord.Color.dark_blue()).set_footer(text="This could be because the subreddit doesn't exist, or is private", icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)

            except Exception as e:
                if isinstance(e, KeyError):
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- Couldn't find anything matching {subreddit}!```", color=discord.Color.dark_blue()).set_footer(text="This could be because the subreddit doesn't exist, or is private", icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- There was an error, please try again later```", color=discord.Color.dark_blue())
                    await ctx.send(embed=embed)
    
    @commands.command(name="meme")
    async def _meme(self, ctx):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            try:
                async with aiohttp.ClientSession() as con:
                    async with con.get(f"https://www.reddit.com/r/meme/.json") as r:
                        data = await r.json()

                if data["data"]["children"]:
                    if ctx.channel.is_nsfw():
                        for _ in range(1, 30):
                            post = random.choice(data["data"]["children"])
                            if post["data"]["domain"] == "i.redd.it" and not post["data"]["stickied"]:
                                break
                            else:
                                post = None

                    else:
                        for _ in range(1, 30):
                            post = random.choice(data["data"]["children"])
                            if post["data"]["domain"] in ["i.redd.it"] and not post["data"]["stickied"] and not post["data"]["over_18"]:
                                break
                            else:
                                post = None

                    if post:
                        embed = discord.Embed(title=textwrap.fill(
                            post["data"]["title"], width=35), url=f"https://www.reddit.com{post['data']['permalink']}", color=discord.Color.dark_blue())
                        embed.set_image(url=post["data"]["url"])
                        embed.add_field(
                            name="Upvotes", value=f"```py\n{int(post['data']['ups']) - int(post['data']['downs'])}```", inline=True)
                        embed.set_footer(
                            text=f"Uploaded by u/{post['data']['author']}", icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Error!", description=f"```diff\n- Failed getting a post from ! (This may be because the post was a video, which is unsupported)```", color=discord.Color.dark_blue()).set_footer(text="There was an error", icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- Couldn't find anything matching!```", color=discord.Color.dark_blue()).set_footer(text="There was an error", icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)

            except Exception as e:
                if isinstance(e, KeyError):
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- Couldn't find anything matching !```", color=discord.Color.dark_blue()).set_footer(text=f"There was an error", icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error!", description=f"```diff\n- There was an error, please try again later```", color=discord.Color.dark_blue())
                    await ctx.send(embed=embed)
    
#PYTHON IS COOL

def setup(bot):
    #Im dead ... :,
    bot.add_cog(Reddit(bot))