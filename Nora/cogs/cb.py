"""
Author :  Sitanshu15
Bot : Nora
"""
from async_cleverbot import Cleverbot, DictContext
import asyncio
from discord.ext import commands
import os
from dotenv import load_dotenv
import json

load_dotenv()

class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chatting = []
        with open('config.json') as config_file:
            data = json.load(config_file)
        self.chatbot = Cleverbot(data["cleverbot"], context = DictContext())

    def is_chatting(self, author):
        if author in self.chatting:
            return True
        else:
            return False

    @commands.command(name = "chat", aliases = ["cb"])
    async def _chat(self, ctx, *, text: str):
        bl_users = await self.bot.db.fetch("SELECT * FROM bl WHERE user_id = $1", ctx.author.id)
        if bl_users:
            e = discord.Embed(title="You cant use that command", description="You are blacklisted please join the support sever for further assistance", color=discord.Color.dark_blue())
            await ctx.send(embed=e)
            return
        if 1000 > (len(text)) < 1:
            return await ctx.send("Text must be longer than 1 characters and shorter than 1000.")
        
        elif self.is_chatting(ctx.author):
            return await ctx.send(f"You don't need to put `{ctx.prefix}chat` at the start of your sentence!")
        
        else:
            def check(m):
                return (m.author == ctx.author) and (m.channel == ctx.channel)
            
            context = []
            
            self.chatting.append(ctx.author)
            
            async with ctx.typing():            
                response = await self.chatbot.ask(text, ctx.author.id)

                await ctx.reply(response.text, mention_author = False)
            
            message = False
            
            while True:
                try:
                    message = await self.bot.wait_for("message", check = check, timeout = 60)
                except asyncio.TimeoutError:
                    if message:
                        self.chatting.pop(self.chatting.index(ctx.author))
                        return await message.reply("I'm going now, bye! 👋", mention_author = False)
                    else:
                        self.chatting.pop(self.chatting.index(ctx.author))
                        return await message.reply("I'm going now, bye! 👋", mention_author = False)
                else:
                    text = message.content
                    
                    if text.startswith(f"{ctx.prefix}chat"):
                        await ctx.send(f"You don't need to put `{ctx.prefix}chat` at the start of your sentence!")
                    
                    for i in ["bye", "cancel", "i'm going", "gtr", "gtg", "imma leave", "see you", "se ya"]:
                        if i in text.lower():
                            self.chatting.pop(self.chatting.index(ctx.author))
                            return await message.reply("Bye!", mention_author = False)

                    async with ctx.typing():
                        response = await self.chatbot.ask(text, ctx.author.id)

                        await message.reply(response.text, mention_author = False)
    
#PYTHON IS COOL

def setup(bot):
    bot.add_cog(Chatbot(bot))
