import config

import aiohttp
import asyncio
import json
import sys, traceback
from discord.ext import commands
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!")
TOKEN = config.discord_token

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name="hi",
                description="Greet the bot!",
                brief="Hi!",
                aliases=['hello', 'greetings', 'sup', 'yo'])
async def greet():
    await client.say("hi!")

@client.command(name='sl',
                description="Looks up the given user and returns their stats.",
                brief="Get your Summoner stats!",
                aliases=['SummonerLookup'])
async def summonerLookup(username):
    byNameUrl = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + username
    rankedUrl = "https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/"
    header = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": config.riot_api_key,
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }


    async with aiohttp.ClientSession() as session:
        summonerId = 0
        async with session.get(byNameUrl, headers=header) as resp:
            if (resp.status == 200):
                response = await resp.text()
                response = json.loads(response)
                await client.say("Summoner " + username + " is level " + str(response['summonerLevel']) + ".")
                summonerId = response['id']
            else:
                await client.say("Error: API call could not be made. "
                                 "Either the given Summoner does not exist, or Riot Games's servers are offline.")
                return

        rankedUrl += str(summonerId)
        print(rankedUrl)
        async with session.get(rankedUrl, headers=header) as resp:
            if (resp.status == 200):
                response = await resp.text()
                response = json.loads(response)
                if (len(response) == 0):
                    await client.say("Summoner " + username + " currently unranked.")
                else:
                    await client.say("Summoner " + username + " is currently ranked " + response[0]['tier'] + " " + response[0]['rank'] + ".")
            else:
                await client.say("fail")


@summonerLookup.error
async def summonerLookupHandler(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        await client.say("Did you forget the summoner's name?")
        return

    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@client.event
async def on_ready():
    print("Logged in as " + client.user.name)

client.run(TOKEN)