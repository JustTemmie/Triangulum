import discord
from discord import Member, Embed, app_commands
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = "ping", description = "Pong!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! slash commands have a latency of {round(self.bot.latency * 1000)}ms")
        
async def setup(bot):
    await bot.add_cog(ping(bot))#, guilds = [discord.Object(id = 628212961218920477)])
