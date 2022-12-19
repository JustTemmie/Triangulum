import json
import asyncio
from discord import Embed


inv_version = 1.01


async def check_if_not_exist(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False

    return True


async def update_accounts():
    users = await get_bank_data()

    for user in users:
        if users[str(user)]["version"] <= 1.01:
            users[str(user)]["stats"]["bag_eaten"] = 0

        pass


async def open_account(self, ctx):
    user = ctx.author
    users = await get_bank_data()

    if str(user.id) in users:
        return

    embed = Embed(title="Do you want to open an account?", color=ctx.author.color)

    embed.add_field(
        name='If you do, please respond with "yes"\nDoing this means you agree to storing data on Triangulum\'s server',
        value="||\n||",
        inline=False,
    )

    await ctx.send(embed=embed)
    
    try:
        userInput = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60)
    except asyncio.TimeoutError:
        return await ctx.send(f"**Timed out** You took too long to answer")
    

    if userInput.content.lower() != "yes":
        await ctx.send("okay, cancelling")
        return
    
    users[str(user.id)] = {}
    
    
    users[str(user.id)]["stats"] = {}
    
    users[str(user.id)]["stats"]["bolle_eaten"] = 0
    users[str(user.id)]["stats"]["bag_eaten"] = 0
    
    
    users[str(user.id)]["version"] = inv_version

    with open("storage/playerData.json", "w") as f:
        json.dump(users, f)

    return True


async def get_bank_data():
    with open("storage/playerData.json", "r") as f:
        data = json.load(f)

    return data
