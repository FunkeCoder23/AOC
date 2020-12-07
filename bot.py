# bot.py
import uwuify
from discord.ext.commands import Bot
import json
from asyncio.windows_events import NULL
from ratelimit import limits
from ratelimit import RateLimitException
import requests
from discord.ext import commands
from discord import Embed, Emoji
from time import strftime, time
from datetime import datetime
from random import randint


def extract_score(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return (int(json['local_score']))
    except KeyError:
        return 0


def extract_stars(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return (int(json['stars']))
    except KeyError:
        return 0


global hugs
hugs = ["https://tenor.com/view/milk-and-mocha-hug-cute-kawaii-love-gif-12535134", "https://tenor.com/view/love-couple-hug-cute-cat-gif-16032768",
        "https://tenor.com/view/hugs-hugging-hearts-love-hug-you-gif-12853824", "https://giphy.com/gifs/editingandlayout-the-office-hug-michael-scott-yidUzriaAGJbsxt58k",
        "https://giphy.com/gifs/hug-love-winnie-the-pooh-llmZp6fCVb4ju", "https://giphy.com/gifs/cheezburger-hug-baymax-lXiRKBj0SAA0EWvbG",
        "https://giphy.com/gifs/Friends-friends-episode-16-tv-VbawWIGNtKYwOFXF7U", "https://giphy.com/gifs/duck-animal-friendship-pals-4No2q4ROPXO7T6NWhS",
        "https://giphy.com/gifs/etredcarpet--golden-globes-2017-3o6ZtbGDpbSMEbffiM", "https://giphy.com/gifs/Friends-season-6-friends-tv-episode-602-eMIGPdZ77kPgD7nf4j",
        "https://giphy.com/gifs/homer-simpson-the-simpsons-season-12-1GJRIgTY4sS6k", "https://giphy.com/gifs/hug-cat-love-NhjPhBQIIxdxm",
        "https://giphy.com/gifs/martin-hug-lawrence-4vDQtFRvx5ZSM", "https://giphy.com/gifs/hug-brother-bbxTrFmeoM7aU"]

# json stuff
with open('secrets.json', 'r') as f:
    secrets = json.load(f)
    global TOKEN, GUILD, sessionID
    TOKEN = secrets["TOKEN"]
    GUILD = secrets["GUILD"]
    sessionID = secrets["sessionID"]


url = 'https://adventofcode.com/2020/leaderboard/private/view/974092.json'
cookies = dict(session=sessionID)
# members = data["members"]
# i = 0
# global response
# response = "Leaderboard: \n"
# for member_num in members:
#     i += 1
#     response += str(i)+". "
#     response += str(members[member_num]["name"])+": "
#     response += str(members[member_num]["stars"])+" stars "
#     response += "Score: " + str(members[member_num]["local_score"]) + str("\n")
# response += "\nCome join at https://adventofcode.com/ and join the leaderboard with code '974092-d0365788'\n"
# print(response)
# print(data)
# datetime.datetime.fromtimestamp(
#     int("1284105682")
# ).strftime('%Y-%m-%d %H:%M:%S')
# discord stuff

# client = discord.Client()


@limits(calls=1, period=900)
def update_json():
    print("Updated")
    global current_time
    current_time = time()
    r = requests.get(url, cookies=cookies)
    global data
    data = r.json()


# @client.event
# async def on_ready():
#     for guild in client.guilds:
#         if guild.name == GUILD:
#             break

#     print(
#         f'{client.user} is connected to the following guild:\n'
#         f'{guild.name}(id: {guild.id})\n'
#     )

#     members = '\n - '.join([member.name for member in guild.members])
#     print(f'Guild Members:\n - {members}')

# client.run(TOKEN)

async def record_usage(ctx):
    t = datetime.fromtimestamp(time()).strftime('%I:%M:%S %p')
    print(t, ":", ctx.author, 'used', ctx.command)


bot = commands.Bot(command_prefix='!')


@bot.command(name='hi-vinnie', help='@\'s vinnie')
@commands.before_invoke(record_usage)
async def atvinnie(ctx):
    response = '<@!218931468603228160>'
    await ctx.send(response)


@bot.command(name='uwu', help='You already know')
@commands.before_invoke(record_usage)
async def uwu(ctx, *, args):
    await ctx.send(uwuify.uwu(args))


@bot.command(name='test', help='Test shit out')
@commands.before_invoke(record_usage)
async def echo(ctx, *, args):
    await ctx.send(args)


@bot.command(name='hug', help="Sends a hug")
@commands.before_invoke(record_usage)
async def hugA(ctx, *, args=None):
    response = hugs[randint(0, len(hugs)-1)]
    if(args != None):
        await ctx.send(args)
    await ctx.send(response)


@bot.command(name='score', help="Get score of user")
@commands.before_invoke(record_usage)
async def score(ctx, *, name):
    # with open('AOC.json') as f:
    #     data = json.load(f)
    # print(name)
    # current_time = time()
    try:
        update_json()
    except RateLimitException:
        print("rate limited")

    members = data["members"]
    name_num = 0
    for member_num in members:
        if members[member_num]["name"] == name:
            name_num = member_num
            break
    if(name_num == 0):
        await ctx.send(name + " not found in leaderboard. 😑")
        return
    # print(name_num)
    score = members[name_num]["local_score"]
    levels = members[name_num]["completion_day_level"]
    # print(levels)
    embed = Embed(title="{}\n{} Points".format(name, score), color=0x990000)
    embed.set_author(name="Advent of Code Leaderboard")
    for day in range(1, 26):
        if str(day) in levels:
            stars = "2" if "2" in levels[str(day)] else "1"
            value = "⭐⭐\n" if stars == "2" else "⭐\n"
            value += datetime.fromtimestamp(int(
                levels[str(day)][stars]["get_star_ts"])).strftime('%b %d\n %I:%M %p')
            embed.add_field(name="Day " + str(day),
                            value=value, inline=True)
            # print("Day " + str(day))
            # print(value)

    updated = datetime.fromtimestamp(current_time).strftime('%I:%M:%S %p')
    nextupdate = datetime.fromtimestamp(
        900+current_time).strftime('%I:%M:%S %p')
    embed.set_footer(
        text="Updated at " + updated + "\nNext update available at " + nextupdate)
    await ctx.send(embed=embed)


@bot.command(name='join', help='Shows information on how to join the Advent of Code Leaderboard')
@commands.before_invoke(record_usage)
async def join_us(ctx):
    embed = Embed(title="Join the Leaderboard", url="https://adventofcode.com/2020",
                  description="Leaderboard Code: 974092-d0365788", color=0x226d1c)
    embed.set_author(name="Advent of Code Leaderboard",
                     icon_url="https://i.imgur.com/Jlp3GB8.png")
    embed.set_thumbnail(url="https://i.stack.imgur.com/ArhPo.gif")
    await ctx.send(embed=embed)


@bot.command(name='day', help="Get the rankings (time) for individual days")
@commands.before_invoke(record_usage)
async def day(ctx, day):
    max_day = 0
    if(day == None):
        await ctx.send("usage: !day <day>")
        return
    embed = Embed(title="Day "+day+" Leaderboard", color=0x9a8623)
    embed.set_author(name="Advent of Code Leaderboard",
                     icon_url="https://i.imgur.com/Jlp3GB8.png")
    embed.set_thumbnail(url="https://i.stack.imgur.com/ArhPo.gif")
    lines = []

    try:
        update_json()
    except RateLimitException:
        print("rate limited")

    part1 = {}
    part2 = {}
    members = data["members"]
    for member in members:
        name = members[member]["name"]
        levels = members[member]["completion_day_level"]
        if day in levels:
            max_day = day
            for part in levels[day]:
                # print(levels[day][part])
                if part == '1':
                    part1.update({name: levels[day][part]["get_star_ts"]})
                if part == '2':
                    part2.update({name: levels[day][part]["get_star_ts"]})
    if max_day == 0:
        await ctx.send("No data available for day " + day)
        return
    part1 = dict(sorted(part1.items(), key=lambda item: item[1]))
    part2 = dict(sorted(part2.items(), key=lambda item: item[1]))

    response = ""
    place = 0
    for name in part1:
        place += 1
        response += str(place)+'. ' + name + '\n⠀' + \
            datetime.fromtimestamp(int(part1[name])).strftime(
                '%m/%d %I:%M:%S %p') + '\n'
    embed.add_field(name="Part 1", value=response, inline=True)

    response = ""
    place = 0
    for name in part2:
        place += 1
        response += str(place)+'. ' + name + '\n⠀' + \
            datetime.fromtimestamp(int(part2[name])).strftime(
                '%m/%d %I:%M:%S %p') + '\n'

    embed.add_field(name="Part 2", value=response, inline=True)
    updated = datetime.fromtimestamp(current_time).strftime('%I:%M:%S %p')
    nextupdate = datetime.fromtimestamp(
        900+current_time).strftime('%I:%M:%S %p')
    embed.set_footer(
        text="Updated at " + updated + "\nNext update available at " + nextupdate)
    await ctx.send(embed=embed)


@ bot.command(name='leaderboard', help='Show the Advent of Code Leaderboard')
@ commands.before_invoke(record_usage)
async def board(ctx):
    embed = Embed(title="Join the Leaderboard", url="https://adventofcode.com/2020",
                  description="Leaderboard Code: 974092-d0365788", color=0x226d1c)
    embed.set_author(name="Advent of Code Leaderboard",
                     icon_url="https://i.imgur.com/Jlp3GB8.png")
    embed.set_thumbnail(url="https://i.stack.imgur.com/ArhPo.gif")
    lines = []

    try:
        update_json()
    except RateLimitException:
        print("rate limited")

    members = data["members"]
    i = 0

    for member_num in members:
        lines.append(members[member_num])
    lines.sort(key=extract_score, reverse=True)
    lines.sort(key=extract_stars, reverse=True)
    # print(lines)

    for leader in lines:
        i += 1
        if leader["name"] == None:
            name = "Anonymous #"+leader+": "
        else:
            name = str(leader["name"])+"  "
        if (i == 1):
            name += "<:platinum:752979216592797836>"
        elif (i == 2):
            name += "<:gold:752979203078619186>"
        elif (i == 3):
            name += "<:silver:752979184367698041>"

        response = "‎‎⠀" + str(leader["stars"])+" ⭐ | "
        response += str(leader["local_score"]) + str(" points")
        response += "!" if (leader["local_score"] !=
                            0) else " <:sunglass_cry:757783574232694906>"
        embed.add_field(name=str(i)+". " + name,
                        value=response, inline=False)
    # response += "\nCome join at https://adventofcode.com/ and join the leaderboard with code '974092-d0365788'\n"
    # response += "Updated at " + \
    #     + "\n"
    # response += "Next update available at " + \
    #     datetime.fromtimestamp(
    #         current_time+900).strftime('%I:%M %p') + "\n"
    # print(response)
    updated = datetime.fromtimestamp(current_time).strftime('%I:%M:%S %p')
    nextupdate = datetime.fromtimestamp(
        900+current_time).strftime('%I:%M:%S %p')
    embed.set_footer(
        text="Updated at " + updated + "\nNext update available at " + nextupdate)
    await ctx.send(embed=embed)

bot.run(TOKEN)

# score(ctx=0, name="FunkeCoder23")
