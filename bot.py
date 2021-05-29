# bot.py
import os
import random

from discord import Colour
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import math
from pretty_help import DefaultMenu, PrettyHelp
import akinator

aki = akinator.Akinator()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")
menu = DefaultMenu('◀️', '▶️', '❌') # You can copy-paste any icons you want.
bot.help_command = PrettyHelp(navigation=menu, color=15277667, no_category = 'Commands', index_title="Help") 

@bot.command(name='aki', help='Plays a game of akinator')
async def akiNator(ctx):

    q = aki.start_game()

    while aki.progression <= 80:
        embedVar = Embed(title=q, description="""🇾 Yes
🇳 No
🇮 Idk
🇵 Probably
❔ Probably Not
🇧 Back
""", color=15844367)
        a = await ctx.send(embed=embedVar)
        for reaction in ["🇾", "🇳", "🇮", "🇵", "❔", "🇧"]:
            await a.add_reaction(reaction)

        def check(reaction, user):
            global userAnswer
            if reaction.emoji in ["🇾", "🇳", "🇮", "🇵", "❔", "🇧"] and user == ctx.message.author and reaction.message == a:
                if reaction.emoji == "🇾":
                    userAnswer = "y"
                    return True
                elif reaction.emoji == "🇳":
                    userAnswer = "n"
                    return True
                elif reaction.emoji == "🇮":
                    userAnswer = "idk"
                    return True
                elif reaction.emoji == "🇵":
                    userAnswer = "p"
                    return True
                elif reaction.emoji == "❔":
                    userAnswer = "pn"
                    return True
                elif reaction.emoji == "🇧":
                    userAnswer = "b"
                    return True

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            embedVar = Embed(title=f"Timed Out", description="That question timed out.", color=15158332)
            await ctx.send(embed=embedVar)
            q = aki.answer("i")
        else:
            if userAnswer == "b":
                try:
                    q = aki.back()
                except akinator.CantGoBackAnyFurther:
                    embedVar = Embed(title=f"Oops", description="This is the first question.", color=15158332)
                    a = await ctx.send(embed=embedVar)
                    pass
            else:
                q = aki.answer(userAnswer)

    aki.win()

    await ctx.send(random.choice(["https://i.pinimg.com/originals/07/ed/75/07ed75a40de90b6055cf7a7e7be5677e.gif", "https://media0.giphy.com/media/d3mlE7uhX8KFgEmY/giphy.gif", "https://media1.giphy.com/media/xUPGcJYhYHA3IrAO1G/giphy.gif?cid=6c09b9529n4evcvdkcdf5b7n0zl7uh5awfflbhw1ai8gxw15&rid=giphy.gif&ct=s", "https://i.pinimg.com/originals/87/dc/79/87dc799670c06e9754bccb3b37d9541d.gif", "https://media3.giphy.com/avatars/SofiB/dPa4VaR5LL4z.gif"]))
    embedVar = Embed(title="Is it...", description=f"{aki.first_guess['name']} ({aki.first_guess['description']})? ✅ or ❌", color=15105570)
    embedVar.set_image(url=aki.first_guess['absolute_picture_path'])
    correct = await ctx.send(embed=embedVar)
    for reaction in ["✅", "❌"]:
            await correct.add_reaction(reaction)
    def check(reaction, user):
            global cor
            if reaction.emoji in ["✅", "❌"] and user == ctx.message.author and reaction.message == correct:
                if reaction.emoji == "✅":
                    cor = "y"
                    return True
                else:
                    cor = "n"
                    return True

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        embedVar = Embed(title=f"Timed Out", description="You still there? >:", color=15158332)
        await ctx.send(embed=embedVar)
    else:
        if cor == "y":
            embedVar = Embed(title="Yay!", description=f"This was fun...", color=2067276)
            await ctx.send(embed=embedVar)
        else:
            embedVar = Embed(title="Oof!", description=f"But I'm never wrong!!!", color=15158332)
            await ctx.send(embed=embedVar)

bot.run(TOKEN)