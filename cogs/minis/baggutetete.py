import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

import libraries.dataStuff as dataStuff

class bagbag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ostbag", aliases=["ostebaguette", "ostbaguette"], brief="count how many bagbag's you've eaten")
    async def ostbagcommand(self, ctx, bags = 0.0):
        await dataStuff.open_account(self, ctx)

        userNotExist = await dataStuff.check_if_not_exist(ctx.author)
        if userNotExist:
            return await ctx.send(f"i could not find your inventory, they need to create an account first")

        bank = await dataStuff.get_bank_data()
        
        if bags == 0:
            embed = Embed()
            embed.title = f"{ctx.author.display_name}'s bagbag addiction level"
            embed.colour = ctx.author.colour

            embed.add_field(name = "they've eaten", value = f'{bank[str(ctx.author.id)]["stats"]["bag_eaten"]} bagbags')
            
            await ctx.send(embed=embed)
            return
        

        bank[str(ctx.author.id)]["stats"]["bag_eaten"] += bags

        with open("./storage/playerData.json", "w") as f:
            json.dump(bank, f)
        
        embed = Embed()
        embed.title = f"{ctx.author.display_name} just ate {bags} bags"
        embed.colour = ctx.author.colour

        embed.add_field(name = "now they've eaten", value = f'{bank[str(ctx.author.id)]["stats"]["bag_eaten"]} bagbags')
        
        await ctx.send(embed=embed)
        
        
async def setup(bot):
    await bot.add_cog(bagbag(bot))
    