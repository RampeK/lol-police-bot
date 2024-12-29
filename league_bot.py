import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime
import os
import json

intents = discord.Intents.all()  # This gives all required permissions

bot = commands.Bot(command_prefix='!', intents=intents)

class LeagueBanneri(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_mentions = {}  # Track mentions per user
        
        # Words that trigger the bot
        self.trigger_words = [
            'league of legends', 'league', 'lol', 'loli', 'lolia', 'leg', 
            'leagu', 'leage', 'legends', 'loli', 'yasuo', 'teemo'
        ]
        
        # Fun responses
        self.responses = [
            "LEAGUE OF LEGENDS ALERT! This game is forbidden on this server!",
            "Sorry, but the L-word is not allowed here...",
            "Forbidden activity detected: League of Legends",
            "*sweeps League of Legends under the rug*",
            "No League talk here, the sun is shining outside!",
            "WARNING: League of Legends discussion detected",
            "Did you know that there are over 1000 better games to play?",
            "League? Let's talk about something more fun!",
            "We only talk about quality games here!",
            "League of Legends mentioned... Fobba Fors has been notified",
            "*plays sad trombone*",
            "League player detected! Time for an intervention!",
            "Error 404: League of Legends not allowed here",
            "Could you kindly stop talking about the L-game?",
            "League? Have you tried literally any other game?"
        ]
        
        # GIF URL
        self.gif_url = "https://media1.tenor.com/m/lQGEzCj6UuQAAAAd/no-league-of-legends.gif"

    @commands.Cog.listener()
    async def on_message(self, message):
        # Don't respond to bot messages
        if message.author.bot:
            return

        # Check if message contains forbidden words
        if any(word.lower() in message.content.lower() for word in self.trigger_words):
            # Track user mentions
            user_id = message.author.id
            if user_id not in self.user_mentions:
                self.user_mentions[user_id] = 1
            else:
                self.user_mentions[user_id] += 1

            # Create embed with GIF
            embed = discord.Embed(color=discord.Color.red())
            embed.set_image(url=self.gif_url)
            
            # Send response with mention count and GIF
            response = random.choice(self.responses)
            bot_message = await message.channel.send(
                content=f"{response}\n{message.author.mention} this is your {self.user_mentions[user_id]}. mention of the forbidden game!",
                embed=embed
            )
            
            # Delete both messages after 2 minutes
            await asyncio.sleep(120)  # Wait 2 minutes
            try:
                await message.delete()
                await bot_message.delete()
            except discord.errors.NotFound:
                pass  # Message already deleted

    @commands.command()
    async def mentions(self, ctx, user: discord.Member = None):
        """Check how many times a user has mentioned League"""
        if user is None:
            user = ctx.author
            
        mentions = self.user_mentions.get(user.id, 0)
        await ctx.send(f"{user.name} has mentioned the forbidden game {mentions} times!")

async def setup(bot):
    await bot.add_cog(LeagueBanneri(bot))

@bot.event
async def on_ready():
    print(f'{bot.user} ready to remove League of Legends! 🎮')
    await setup(bot)


# Read token from config.json
with open('config.json') as f:
    config = json.load(f)
    
# Start the bot
bot.run(config['token'])