"""
Author :  Sitanshu15
Bot : Nora
"""

import discord
from discord.ext import commands
from async_cse import Search
import aiohttp
import json


class Internet(commands.Cog):
    def __init__(self, bot):
        with open('config.json') as config_file:
            data = json.load(config_file)
        self.bot = bot
        self.google = Search([data["google_token_1"],
                              data["google_token_2"],
                              data["google_token_3"],
                              data["google_token_4"]
                              ])
                              
    
    @commands.command(name="google", aliases=["g", "search"])
    async def _google(self, ctx, *, query):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        with ctx.channel.typing():
            try:
                result = await self.google.search(query)
                urlformat = query.replace(" ", "+")
                embed = discord.Embed(title=f"Search results for {query}:", url=f"https://www.google.com/search?safe=active&q={urlformat}", color=discord.Color.dark_blue())
                for entry in result[:3]:
                    embed.add_field(name=entry.title, value=f"{entry.url}\n{entry.description}", inline=False)
                
                embed.set_thumbnail(url=result[0].image_url)
                
                await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(title="Error!", description=f"```diff\n- {e}```", olor=discord.Color.dark_blue())
                await ctx.send(embed=embed)

                
    @commands.command(name="lengthen")
    async def _lengthen(self, ctx, *, url):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        try:
            with ctx.channel.typing():
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        url = str(response.url)
                        embed = discord.Embed(title="Success!", url=url, description=f"`{url}`", color=discord.Color.dark_blue())
                        await ctx.send(embed=embed)
        except aiohttp.InvalidURL:
            embed = discord.Embed(title="Error!", description=f"```diff\n- Invalid URL: {url}```", color=discord.Color.dark_blue())
            await ctx.send(embed=embed)
    
#PYTHON IS COOL
        
def setup(bot):
    bot.add_cog(Internet(bot))
