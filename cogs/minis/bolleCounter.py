import discord
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json

import libraries.dataStuff as dataStuff

class bolle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="bolle", brief="count how many bolle's you've eaten")
    async def bolleCoutercommand(self, ctx, bolles = 0.0):
        await dataStuff.open_account(self, ctx)

        userNotExist = await dataStuff.check_if_not_exist(ctx.author)
        if userNotExist:
            return await ctx.send(f"i could not find your inventory, they need to create an account first")

        bank = await dataStuff.get_bank_data()
        
        if bolles == 0:
            embed = Embed()
            embed.title = f"{ctx.author.display_name}'s bolle addiction level"
            embed.colour = ctx.author.colour

            embed.add_field(name = "they've eaten", value = f'{bank[str(ctx.author.id)]["stats"]["bolle_eaten"]} bolle')
            
            await ctx.send(embed=embed)
            return
        

        bank[str(ctx.author.id)]["stats"]["bolle_eaten"] += bolles

        with open("./storage/playerData.json", "w") as f:
            json.dump(bank, f)
        
        embed = Embed()
        embed.title = f"{ctx.author.display_name} just ate {bolles} bolles"
        embed.colour = ctx.author.colour

        embed.add_field(name = "now they've eaten", value = f'{bank[str(ctx.author.id)]["stats"]["bolle_eaten"]} bolle')
        
        await ctx.send(embed=embed)
        
        
async def setup(bot):
    await bot.add_cog(bolle(bot))
