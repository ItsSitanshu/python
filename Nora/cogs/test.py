import discord
from discord.ext import commands

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx: commands.Context):
        await ctx.send("NONE IN MIND")

def setup(bot):
    bot.add_cog(TestCog(bot))