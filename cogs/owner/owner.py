import discord
from discord.ext import commands
from discord.ext.commands import Greedy

from typing import Optional, Literal
import ast

import sys
import os

import asyncio
import subprocess

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the or else
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class owner(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
    
    @commands.command(name="restart", aliases=["reboot"])
    @commands.is_owner()
    async def rebootbot(self, ctx):
        os.execv(sys.executable, ["python3"] + sys.argv)


    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
        
        # Works like:
        # ttsync -> global sync
        # ttsync ~ -> sync current guild
        # ttsync * -> copies all global app commands to current guild and syncs
        # ttsync ^ -> clears all commands from the current guild target and syncs (removes guild commands)
        # ttsync id_1 id_2 -> syncs guilds with id 1 and 2
        
    @commands.command(name="bash")
    @commands.is_owner()
    async def run_bash(self, ctx, *, command):
        commandArray = command.split(" ")
        await ctx.send(f"are you sure you want to run the command `{command}`?")
        try:
            response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send(f"**Timed out** cancelling")

        output = subprocess.run([*commandArray], stdout=subprocess.PIPE, timeout=180)
        output = output.stdout.decode("utf-8")

        if len(output) + len(command) < 1975:
            await ctx.send(f"`{command}` returned output:\n```{output} ```")
            return

        n = 1994
        split_strings = []

        for index in range(0, len(output), n):
            split_strings.append(output[index : index + n])

        for message in split_strings:
            await ctx.send(f"```{message}```")

    @commands.command(name="startandro")
    @commands.is_owner()
    async def run_andro(self, ctx):
        subprocess.run("screen -dmS andromeda bash -c 'cd Scripts/space-bot/; python3.10 main.py'", shell=True, check=True, timeout=180)
        await ctx.send("oke!")
    
    @commands.command()
    @commands.is_owner()
    async def run(self, ctx, *, code: str):
        """
        Run python stuff
        """
        fn_name = "_eval_expr"

        code = code.strip("` ")  # get rid of whitespace and code blocks
        if code.startswith("py\n"):
            code = code[3:]

        try:
            # add a layer of indentation
            cmd = "\n    ".join(code.splitlines())

            # wrap in async def body
            body = f"async def {fn_name}():\n    {cmd}"

            parsed = ast.parse(body)
            body = parsed.body[0].body

            insert_returns(body)

            env = {
                "bot": self.bot,
                "ctx": ctx,
                "message": ctx.message,
                "server": ctx.message.guild,
                "channel": ctx.message.channel,
                "author": ctx.message.author,
                "commands": commands,
                "discord": discord,
                "guild": ctx.message.guild,
            }
            env.update(globals())

            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = await eval(f"{fn_name}()", env)

            out = ">>> " + code + "\n"
            output = "```py\n{}\n\n{}```".format(out, result)

            if len(output) > 2000:
                await ctx.send("The output is too long?")
            else:
                await ctx.send(output.format(result))
        except Exception as e:
            await ctx.send("```py\n>>> {}\n\n\n{}```".format(code, e))
        
async def setup(bot: commands.bot) -> None:
    await bot.add_cog(owner(bot))
