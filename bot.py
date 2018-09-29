import aiohttp
import asyncio
import json
from discord.ext import commands
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!")
TOKEN = "Mzc4NjQ3MzY2OTI1ODExNzM0.DpCLXg.IEiqHi4o4tF3wJByb2JZa1pYfD0"\

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name="test")
async def Test():
    await client.say("hi!")

@client.command(name='sl',
                description="Looks up the given user and returns their stats.",
                brief="Get your Summoner stats!",
                aliases=['SummonerLookup'])
async def summonerLookup(username):
    url = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + username
    header = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": "RGAPI-9f1eb46e-5dff-4681-b530-861a8becb8bd",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }


    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as resp:
            if (resp.status == 200):
                response = await resp.text()
                response = json.loads(response)
                await client.say("Summoner " + username + " is level " + str(response['summonerLevel']) + ".")
            else:
            	await client.say("Error: API call could not be made. "
            		             "Either the given Summoner does not exist, or Riot Games's servers are offline.")

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