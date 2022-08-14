import discord
from discord import app_commands
from discord.ext import commands

import glob
import json
from typing import List

cog_choices = []

for filename in glob.iglob("./cogs/**", recursive=True):
    if filename.endswith('.py'):
        # removes the .py
        cog_path = filename[:-3]
        # cogs use a dot to separate the path, not slashes
        cog = cog_path.replace("/", ".")
        # remove the ./cogs/ part
        cog = cog[7:]
        cog_choices.append(cog)

class ownerSlash(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    async def cog_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:

        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in cog_choices
        ]

    @app_commands.command(
        name="load",
        description="Owner Command: Loads a cog")
    @app_commands.describe(cog = "The cog to load")
    @app_commands.autocomplete(cog = cog_autocomplete, cog2 = cog_autocomplete, cog3 = cog_autocomplete, cog4 = cog_autocomplete, cog5 = cog_autocomplete, cog6 = cog_autocomplete, cog7 = cog_autocomplete, cog8 = cog_autocomplete, cog9 = cog_autocomplete)
    async def load(
            self,
            interaction: discord.Interaction,
            cog: str,
            cog2: str = None,
            cog3: str = None,
            cog4: str = None,
            cog5: str = None,
            cog6: str = None,
            cog7: str = None,
            cog8: str = None,
            cog9: str = None) -> None:
        
        if interaction.user.id not in self.bot.owner_ids:
            return await interaction.response.send_message("You are not my owner!")
        try:
            await self.bot.load_extension(f"cogs.{cog}")
            await interaction.response.send_message(f"Loaded: {cog}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @app_commands.command(
        name="unload",
        description="Owner Command: Unloads a cog")
    @app_commands.describe(cog = "The cog to unload")
    @app_commands.autocomplete(cog = cog_autocomplete, cog2 = cog_autocomplete, cog3 = cog_autocomplete, cog4 = cog_autocomplete, cog5 = cog_autocomplete, cog6 = cog_autocomplete, cog7 = cog_autocomplete, cog8 = cog_autocomplete, cog9 = cog_autocomplete)
    async def unload(
            self,
            interaction: discord.Interaction,
            cog: str,
            cog2: str = None,
            cog3: str = None,
            cog4: str = None,
            cog5: str = None,
            cog6: str = None,
            cog7: str = None,
            cog8: str = None,
            cog9: str = None) -> None:

        marked_cogs = [cog, cog2, cog3, cog4, cog5, cog6, cog7, cog8, cog9]
        
        if interaction.user.id not in self.bot.owner_ids:
            return await interaction.response.send_message("You are not my owner!")
        try:
            for cog in marked_cogs:
                if cog is not None:
                    await self.bot.unload_extension(f"cogs.{cog}")
                    await interaction.response.send_message(f"Unloaded: {cog}", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
        
async def setup(bot: commands.bot) -> None:
    with open("config.json", "r") as f:
        config = json.load(f)

    servers = []
    for guild in config["ADMIN_SERVER_IDS"]:
        servers.append(discord.Object(id=guild))
    await bot.add_cog(ownerSlash(bot), guilds = servers)
