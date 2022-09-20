from email.mime import application
import os
import glob
import random
import logging
from time import time
import json
import asyncio
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import discord
from discord.ext import tasks, commands

import topgg
#import libraries.database as db 

from dotenv import load_dotenv

# Load dotenv file
load_dotenv("keys.env")
TOKEN = os.getenv("DISCORD")#_STABLE")

# Load config file
with open("config.json", "r") as f:
    config = json.load(f)

# Grab vars from config.json
DEFAULT_PREFIX = config["DEFAULT_PREFIX"]
OWNER_IDS = config["OWNER_IDS"]
#APP_ID = config["APP_ID"]
ADMIN_SERVER_IDS = config["ADMIN_SERVER_IDS"]

# Logging
logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{time()}.log",
    filemode="w",
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)

logging.warning("warning")
logging.error("error")
logging.critical("critical")


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(DEFAULT_PREFIX),
            intents=discord.Intents.all(),
            owner_ids=OWNER_IDS,
            #application_id=APP_ID
        )
        self.synced = False
        self.timestring = ""
        self.ADMIN_SERVER_IDS = ADMIN_SERVER_IDS
    
    async def sync_tree(self):
        if not self.synced:
            #for server in self.guilds:
            #    print(f"Syncing {server.name}")
            #    await tree.sync(guild = discord.Object(id = server.id))
            await tree.sync(guild = discord.Object(id = 1008187565695848488))
            print("slash commands synced successfully!")
            self.synced = True
    
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.wait_until_ready()
        print("Slash commands are now ready!")
        
        await self.sync_tree()
        if not self.ready:
            change_status_task.start()

            guild_count = 0
            for guild in self.guilds:
                print(f"- {guild.id} (name: {guild.name})")
                guild_count += 1

            # Print the bot name, number of guilds, and number of shards.
            print(f"{self.user} is in {guild_count} guild(s).\nwith {self.shard_count} shard(s)")

            # Set the bot ready to True
            self.ready = True

bot = MyBot()
tree = bot.tree

# Remove default help command
bot.remove_command("help")
# Set the ready status to False, so the bot knows it hasnt been initialized yet.
bot.ready = False

@tasks.loop(seconds = 1)
async def change_status_task():
    if bot.timestring != f"it's {datetime.utcnow().strftime('%I:%M')} UTC":
        bot.timestring = f"it's {datetime.utcnow().strftime('%I:%M')} UTC"
        await bot.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(type=discord.ActivityType.watching, name=bot.timestring),
        )

async def load_cogs(bot):
    print("Loading cogs...")
    # loads cogs
    for filename in glob.iglob("./cogs/**", recursive=True):
        if filename.endswith('.py'):
            filename = filename[2:].replace("/", ".") # goes from "./cogs/economy.py" to "cogs.economy.py"
            await bot.load_extension(f'{filename[:-3]}') # removes the ".py" from the end of the filename, to make it into cogs.economy
    

async def main():
    async with bot:
        #await setup(bot)
        await load_cogs(bot)
        await bot.start(TOKEN)

asyncio.run(main())
