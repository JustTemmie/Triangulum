import discord
from discord.ext import commands, tasks
from discord.errors import Forbidden
from discord.ext.commands import (
    CommandNotFound,
    BadArgument,
    MissingRequiredArgument,
    CommandOnCooldown,
)
import random
from datetime import datetime

import logging
import requests
import re
import json
import os

import time
from math import floor

IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

fish_IDs = [1008131433669341274, 885113515411669002, 993869689220509730]

henwees = [
    "henwee :)",
    "henw",
    "green h man my beloved <3",
    "him",
    "what if shenwee tho??",
    "😳",
    "henwee is cool and all, but fuck C",
    "hewwow :)",
    "himwee",
    "smilewee",
    ":)wee",
    "the him",
    "little baby man",
    "little bitch",
    "joker lover 182",
    "he can draw bird :)",
    "wee wee",
    "oui oui",
    "theynwee",
    '"the xwees"',
    "fuckin unity loser lmao imagine using a program with a scuffed cube as an icon smh my head",
    "brib",
    "uwu",
    "ÆwÆ",
    '"Being harassed is dumb people shiz" ',
    "look at him roll :)",
    "breast cheese 😋",
    "the man who never eats a måltid",
    '"cheese is just cow-breast-cheese"',
    '"man is the best gender"',
    "bitchass gorou simp",
    '"feeler shit, man"',
    '"duuuu, thinkeeeeer"',
    "this isn't henwee related i just wanted to say hi geek :)",
    "owo",
    "anywho, beaver clicker",
    "m a n",
    "man",
    "fis :)",
    '"https://store.steampowered.com/app/1718240/Beaver_Clicker/" - Henwee 2022',
    '"flushed best emoji confirmed"',
    "henwy is just some youtuber",
    "<a:henwee_fall:955830194902544415>",
    "henwee spin",
    "please i'm running out of things to put here fajsfdkans nnuwiuab lvbseru sroveronaewruocnweou fuipasn coewivop8aew oaer nuoaern voaernv oer noåerunc voewurnv"
    "holy fuck please stop with the genshin mr hen hen",
    "weehen",
    "beawee:)",
    "gorou 2",
    "gay lil bebi fis",
    "funny fis fredaaag",
    "🏾",
    "🦫",
    "<:wishlistbeaverclickeronsteam:943915845023846401>",
    "the crippledest man in the west",
    "Playing Genshin Impact",
    '"a" -hen 2022',
    '"psfttthhh i dunnu" -hen 2022',
    '"\⬛" -hen 2022',
    '"who tf put the physical theorapist 5 stories up?" -hen 2022',
    '"ok fair" -hen 2022',
    '"yes these kids suck lmao" -hen 2022',
    '"tell me how thaumaturgy and prestidigitation is "utility", but druidcraft is "control"" -hen 2022',
    '"mean ):" -hen 2022',
    '"i feel like i should mention, lillevi and korede isn\'t here (😠)" -hen 2022',
    '"most things, except liquorice" -hen 2022',
    '"Gonna go touch it" -hen 2022',
    "\"well i'm touchable, but I won't be hurt\" -hen 2022",
    '"BTW I\'m not coming to school tomorrow with a lesbian haircut" -hen 2022',
    '"remember, everyone who doesn\'t say anything agrees, just ask Elly" -hen 2022',
    '"js is a shithole hellscape\n(which is nothing like c# i promise)" -hen 2022',
    '"uglies shit i\'ve seen" -hen 2022',
    '"USA er under india" -hen 2022',
    '"not noticed that, so I guess it\'s less noticable" - hen 2022',
    '"i dag seiner tidlig" - not hen 2022',
    "\“blaze can go ******* ***** ***** ********************\” - hen 2022",
    "\“I mean walking is nice\nMiss being able to\”\n- henw2022",
    '"I\'d fuck joker from persona 5"\n"I\'d be fucked by joker from persona 5"\n- hen 2022',
    '"You\'re like one foot in the grave, the other in the closet" - related to hen 2022 ',
    '"æ har ingen oppion om uteliggere" - hen 2022',
    '"no" - hen 2022',
    '"what" - hen 2022',
    '"æ skippe alltid denne delen av biler 1" - hen 2022',
    '"du kan ikke bare si [...]" - hen 2022',
    '"genshin impact e trash" - hen 2022',
    '"cumfused" - hen 2022',
    '"hvor mye packer lightning mcqueen?" - hen 2022',
    '"revert revert actually fixed collison" - hen 2022',
    '"æ hate barn, æ hate barn" - hen 2022',
    '"🦫" - not hen 2022',
    '"henwee quote" - hen 2022',
    '"æ like fugla deez nuts" - hen 2022',
    '"time to commit mass suicide" - hen 2022',
    '"put de som en quote" - hen 2022',
    '"https://cdn.discordapp.com/attachments/847231965764780063/966342099043753984/unknown.png" - hen 2022',
    '"you\'re a fucking idiot" - hen 2022',
    # copilot lmao
    '"i\'m not a fan of the word "fucking"" -hen 2022 - github copilot',
    '\“I\'m not a fan of the word "utility"\” - hen 2022 - github copilot',
    '\“I\'m not a fan of the word "control"\” - hen 2022 - github copilot',
    '"my body is a trashcan" - hen 2022 - github copilot',
    '"joker is a trash" - hen 2022 - github copilot',
    '"henwee is a trash" - hen 2022 - github copilot',
]

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.beaver_break.start()
        self.bloons_challenge.start()
        self.fish_friday.start()
        self.henwee.start()
        self.random_reddit.start()
    
    @commands.Cog.listener()
    async def on_error(self, err, *args, **kwargs):
        await self.bot.get_channel(984577196616216616).send(f"{err}")
        
        if err == "on_command_error":
            await args[0].send("Sorry, something unexpected went wrong.")
            # raise
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            # await ctx.send("Sorry, I couldn't find that command")
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send(
                f"One or more of the required arguments are missing, perhaps the help command could help you out? `{ctx.prefix}help {ctx.command}`"
            )

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(
                f"That command is on cooldown. Please try again in {exc.retry_after:,.2f} seconds.",
                delete_after=(exc.retry_after*1.05 + 0.7),
            )

        #      elif isinstance(exc.original, HTTPException):
        #          await ctx.send("Unable to send message.")

        elif hasattr(exc, "original"):
            # raise exc  # .original

            if isinstance(exc.original, Forbidden):
                await ctx.send("I do not have the permission to do that.")

            else:
                raise exc.original

        else:
            raise exc
    
    
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        logging.info(f"{ctx.command.name} was successfully invoked by {ctx.author}")
        print(f"{ctx.command.name} was successfully invoked by {ctx.author} {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")
    
    # fun things

    @commands.Cog.listener()
    async def on_member_join(self, member):
        #print(f"{member} joined {member.guild} - ({member.id} joined {member.guild.id})")
        if member.bot:
            return
        
        guilds = [694107776015663146, 918787074801401868, 946136828916944987, 885113462378876948, 1046773323163508797]
        
        if not member.guild.id in guilds:
            return
        
        if member.guild.id == 694107776015663146:  # space
            await self.bot.get_channel(694197942000680980).send(
                f"Welcome, {member.mention}! Read through the <#694112817611276348>, assign yourself roles in <#925393973755908136>. And if you wish, introduce yourself in <#694192946387353680>"
            )
            await member.add_roles(
                member.guild.get_role(
                    694108297086631946
                )  # member.guild.get_role(766054606009794580)
            )

            try:
                await member.send(f"Welcome to ***s p a c e !*** We hope you enjoy your stay :)")

            except Forbidden:
                pass

        elif member.guild.id == 1046773323163508797: #dnd server
            await member.add_roles(1046875890086318151)
	
        elif member.guild.id == 918787074801401868:  # frog
            await self.bot.get_channel(918787075434762242).send(
                f"YOOOOO {member.mention} JUST JOINED THE FROG AGENDAAAA!!!!"
            )

        elif member.guild.id == 946136828916944987:  # constaleighton
            await self.bot.get_channel(946146531805900811).send(
                f"hello {member.mention}, have you wishlisted beaver clicker yet?\nhttps://store.steampowered.com/app/1718240"
            )
        
        elif member.guild.id == 885113462378876948:  # maid café
            await self.bot.get_channel(885113515411669002).send(
                f"hello {member.mention} just joined the server!\nwonder if they've wishlisted wishlisted beaver clicker yet?\nhttps://store.steampowered.com/app/1718240"
            )
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if "--" in ctx.content:
            return

        hendex = random.randrange(0, len(henwees))
        
        if ctx.author.bot:
            return

        if ("sus" in ctx.content.lower() and not "jesus" in ctx.content.lower()) or "ussy" in ctx.content.lower():
            msg = await ctx.reply("amogus") 
        
        if "amog" in ctx.content.lower() or "amongu" in ctx.content.lower() or "among us" in ctx.content.lower():
            msg = await ctx.reply("sus")
        
        if "imposter" in ctx.content.lower():
            msg = await ctx.reply("that's not very chungus crewmate of you")
        
        if "crewmate" in ctx.content.lower():
            msg = await ctx.reply("sure thing there you sussy wussy lil amongling")
        
        if "bee " in ctx.content.lower() or "bee" == ctx.content.lower():   
            await ctx.add_reaction("🐝")
            
        
        if random.randint(0, 75000) == 2:
            await ctx.add_reaction("<a:Beaver:984112915206520842>")
        
        
        if ctx.author.id == 325325337615532054:  # adino
            if random.randint(0, 100) == 2:
                await ctx.add_reaction("<:Robpoint:885140068296196106>")


        listies = [
            "dam",
            "revaeb",
            "bippa",
            "biba",
            "bev",
            "castor",
        ]  # if message ==
        
        listies2 = [
            "dam ",
            "bidoof",
            "bæv",
            "beav",
            "bever",
            "castor ",
            "🦫",
        ]  # if in the message
        
        if ctx.guild.id != 918787074801401868:
            listies.append("damn")
        
        if ctx.content == "hut" or "qhut" in ctx.content:
            await ctx.add_reaction("🛖")
            
        if ctx.guild.id == 918787074801401868 and "<:skushed:983643982884139018>" in ctx.content:
            await ctx.add_reaction("😳")
        
        for x in range(0, len(listies)):
            if ctx.content.lower() == listies[x]:
                await self.react_beaver(ctx)

        for x in range(0, len(listies2)):
            if listies2[x] in ctx.content.lower():
                await self.react_beaver(ctx)
                

        if "brain fuck" in ctx.content:
            await ctx.add_reaction("🧠")
            await ctx.add_reaction("🔫")
        

        if (
            "henwee" in ctx.content.lower()
            or "411536312961597440" in ctx.content
        ):  # and ctx.author.id != self.bot.user.id:
            if random.randint(0, 15) == 2:
                await ctx.add_reaction("<a:henwee_fall:955830194902544415>")
                await ctx.add_reaction("<a:henwee_fall_short:955878859197280306>")
                if random.randrange(1, 4) == 2:  # 1/3 chance
                    await ctx.channel.send(
                        henwees[hendex],
                        file=discord.File("images/processed/henwee_fall.gif"),
                    )

    @tasks.loop(seconds=5)
    async def bloons_challenge(self):
        if not self.bot.ready:
            return
        
        with open("storage/bloonsDaily.txt", "r") as f:
            data = f.read()

        if data == str(datetime.now().day) or datetime.now().hour < 8:
            return

        with open("storage/bloonsDaily.txt", "w") as f:
            f.write(str(datetime.now().day))
            
        bloonsDailies = [
            "bloons dailies :pleading_face:",
            "wasss poppin nnnnnn",
            "pssttt.. did you know that bloons has dailies?",
            "bloon go pop",
            "wake up babe bloon's calling",
            "new day, new war crimes",
            "oh god time to play war criminal game again, just don't get mid path ace",
            "god why is churchil so fucking mid",
            "poopers :flushed:",
	    "poppers :pensive:",
	    "can't talk, am blooning",
	    "if you need me you know where to find me",
	    "remember to do contested territories whenever it's around :pleading_face:",
	    "my therapist thinks i should take a break from bloons, but i think she's wrong",
	    "my therapist thinks i should take a break from bloons, but i think they's wrong",
	    "my therapist thinks i should take a break from bloons, but i think he's wrong",
	    "no life, only apes vs helium\n(<https://drive.google.com/file/d/1At38dv-SQVQ3a8FN4AC79Gyhop26DPaB/view>)",
	    "they always say practice makes perfect, but for me it just seems like it ends with more bloons",
        ]

        await self.bot.get_channel(1085938987803357314).send(random.choice(bloonsDailies))
        
    @tasks.loop(seconds=10)
    async def fish_friday(self):
        if not self.bot.ready:
            return
        
        with open("images/video/date.json", "r") as f:
            jsoninfo = json.load(f)

        if jsoninfo == str(datetime.now().day):
            return

        # sends frog in #daily frogs
        await self.send_reddit(1008131433669341274, "frogs", True, 25)
        # await self.send_reddit(993869689220509730, "frogs", True, 25)

        with open("images/video/date.json", "w") as f:
            json.dump(f"{datetime.now().day}", f)

        if datetime.today().weekday() != 4:
            return

        number = random.randrange(0, 100)
        if number < 87:
            for ID in fish_IDs:
                await self.bot.get_channel(ID).send("frog friday!!!", file=discord.File("images/video/funnies/funnyfrogfriday.mp4"))
        
        elif number < 92:
            for ID in fish_IDs:
                await self.bot.get_channel(ID).send("fr- waiit what?", file=discord.File("images/video/funnies/fish.mp4"))
        
        else:
            for ID in fish_IDs:
                await self.bot.get_channel(ID).send("can you guess what day it is?", file=discord.File("images/video/funnies/flatworm.mp4"))
        

    @tasks.loop(hours=1)
    async def beaver_break(self):
        if not self.bot.ready:
            return
        
        if random.randint(0, 5000) != 2:
            return
    
        for ID in fish_IDs:
            await self.bot.get_channel(ID).send("beaver time!!!", file=discord.File("images/video/funnies/thebizzarebeaverbreak.mp4"))
    
    @tasks.loop(seconds=293)
    async def henwee(self):
        if random.randrange(1, 40000) == 2:
            await self.bot.get_channel(919666600955760702).send(
                "reminder to keep on henweeing :)",
                file=discord.File("images/processed/henwee_fall.gif"),
            )
    
    @tasks.loop(minutes=30)
    async def random_reddit(self):
        await self.send_reddit(974642338150367252, "all", True, 100)
        
    
    async def send_reddit(self, channel, subreddit, imageRequired=False, limit=25):
        if self.bot.is_ready():
            try:
                req = requests.get(
                    f"http://reddit.com/r/{subreddit}/hot.json?limit={limit}",
                    headers={"User-agent": "Beaver"},
                )
                json = req.json()
                if "error" in json or json["data"]["after"] is None:
                    await self.bot.get_channel(channel).send(f"an error occured, no r/{subreddit} for now :(")
                    return

                req_len = len(json["data"]["children"])
                
                if imageRequired:
                    for i in range(req_len):
                        post = json["data"]["children"][i]
                        url = post["data"]["url"] # can be image or post link
                        if re.match(r".*\.(jpg|png|gif)$", url):
                            break
                
                else:
                    rand = random.randrange(0, req_len)
                    post = json["data"]["children"][rand]
                    url = post["data"]["url"] # can be image or post link
                    
                              
                title = post["data"]["title"]
                author = "u/" + post["data"]["author"]
                subreddit = post["data"]["subreddit_name_prefixed"]
                link = "https://reddit.com" + post["data"]["permalink"]
                if "selftext" in post["data"]:
                    text = post["data"]["selftext"]  # may not exist
                    if len(text) >= 2000:
                        text = text[:2000].rsplit(" ", 1)[0] + " **-Snippet-**"
                    embed = discord.Embed(title=title, description=text, url=link)
                else:
                    embed = discord.Embed(title=title, url=link)
                
                if re.match(r".*\.(jpg|png|gif)$", url):
                    embed.set_image(url=url)

                embed.set_footer(text=f"By {author} in {subreddit}")
                
                await self.bot.get_channel(channel).send(embed=embed)
            
            except Exception as e:
                print(f"error in send_reddit: {e}")
    
    async def react_beaver(self, ctx):
        await ctx.add_reaction("<a:Beaver:984112915206520842>")
        if random.randrange(0, 40) == 2 and "beaver" in ctx.content:
            message = [
                "DID SOMEONE JUST SAY BEAVER?",
                "beav :)",
                "beaver clicker my beloved <3",
                "wishlist beaver clicker today!",
                "have you wishlisted beaver clicker yet?",
                "go ahead, wishlist beaver clicker already",
            ]
            index = random.randrange(0, len(message))
            await ctx.channel.send(
                f"{message[index]}\nhttps://store.steampowered.com/app/1718240/Beaver_Clicker/"
            )

async def setup(bot):
    await bot.add_cog(events(bot))
