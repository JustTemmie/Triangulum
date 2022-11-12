from discord import app_commands, Interaction
from discord.ext import commands

from math import *
from interruptingcow import timeout

replacement_table = {
    "x": "*",
    "^": "**"
}

allowedCharacters = "1234567890()+-*/^"

class mathCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="math",
        description="i can do math too!"
    ) 
    async def math_command(
        self,
        interaction: Interaction,
        equation: str) -> None:
        
        for symbol in replacement_table:
            mathEquation = equation.replace(symbol, replacement_table[symbol])
        try:
            with timeout(5, exception=RuntimeError):
                if set(mathEquation).difference(set(allowedCharacters)):
                    return await interaction.response.send_message(f"invalid characters used, please only use the following symbols: `{allowedCharacters}`")
                
                await interaction.response.send_message(f"{equation} = {eval(mathEquation)}")
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(mathCommands(bot))
