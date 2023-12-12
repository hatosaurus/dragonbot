import discord
from discord import app_commands
import random
from datetime import datetime
from token_price import *
from selfie import *
import os
import asyncio

battle_net_client = os.environ["CLIENT_ID"]
battle_net_key = os.environ["CLIENT_SECRET"]
client_key = os.environ["CLIENT_KEY"]
API_URL = "https://oauth.battle.net/token"

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

status = "the internets go"

client = discord.Client(intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name=status))

tree = app_commands.CommandTree(client)

now = datetime.now()
current_time = now.strftime("%H:%M")


@client.event
async def on_ready():
    # await tree.sync()
    print("Ready!")


@tree.command(name="sync", description="Sync Dragon Bot's available commands.")
async def sync(interaction):
    await tree.sync()
    await interaction.response.send_message("Tree sync complete.")
    print("Tree sync complete.")


@tree.command(name="remind", description="Set a reminder.")
async def add(interaction, minutes: int, reminder: str):
    await interaction.response.send_message(f'Okay {interaction.user.mention}, you have entered {minutes} minutes for "{reminder}".')
    seconds_to_wait = minutes * 60
    print(f"Sending a reminder to {interaction.user} in {minutes} minutes.")
    await asyncio.sleep(seconds_to_wait)
    # await interaction.followup.send(f"Hey, {interaction.user.mention}, {reminder}!")
    await interaction.channel.send(f"Hey, {interaction.user.mention}, {reminder}!")
    print(f"Sent a reminder to {interaction.user} after {minutes} minutes.")


@tree.command(name="selfie", description="Displays your most recent selfie.")
async def selfie(interaction, name: str, realm: str):
    name_lwr = name.lower()
    realm_lwr = realm.lower()
    selfie = get_selfie(battle_net_client, battle_net_key, name_lwr, realm_lwr)
    if f"{selfie}" == "None":
        await interaction.response.send_message("Error retrieving character. Check spelling and use dashes (-) for the spaces in realm names.")
    else:
        await interaction.response.defer()
        await asyncio.sleep(5)
        # await interaction.followup.send(f"{selfie}")
        file = discord.File(f"character_images/{name}{realm}.png")
        await interaction.followup.send(file=file, content=f"{name} {realm}")
        # await interaction.response.send_message(f"{selfie}")
    print("Returned selfie.")


@tree.command(name="token", description="Checks the current price of the WoW token.")
async def token(interaction):
    current_price = get_wow_token_price(battle_net_client, battle_net_key)
    formatted_price = format_price(current_price)
    await interaction.response.send_message(f"The WoW token currently costs {formatted_price}!")
    print("Returned token price.")


@tree.command(name="join", description="Bring Dragon Bot into your current voice channel.")
async def join(interaction):
    vc = interaction.user.voice.channel
    await vc.connect()
    await interaction.response.send_message(f"I have joined {vc}!")
    print(f"I have joined the voice channel {vc}.")


@tree.command(name="leave", description="Tell Dragon Bot to leave your voice channel.")
async def leave(interaction):
    vc = interaction.user.voice.channel
    await interaction.guild.voice_client.disconnect()
    await interaction.response.send_message(f"I have left {vc}!")
    print(f"I have left the voice channel {vc}.")


@tree.command(name="hello", description="Say hello to dragon bot!")
async def hello(interaction):
    await interaction.response.send_message("Hello!")
    print("Said hello!")


@tree.command(name="smell", description="Check how much you smell")
async def smell(interaction):
    choice = random.randint(1, 100)
    await interaction.response.send_message(f"*SNIFF* *SNIFFFFF* ...you are {choice}% stinky.")
    print(f"Smelled someone at {current_time}!")


@tree.command(name="guildinfo", description="Displays guild information")
async def guildinfo(interaction):
    await interaction.response.send_message("The Brain Cell was founded in Season 4 of Shadowlands!")
    print(f"Displayed guild info at {current_time}!")


@tree.command(name="smellcheck", description="Check how much another user smells")
async def smellcheck(interaction, user: discord.Member):
    choice = random.randint(1, 100)
    await interaction.response.send_message(f"*SNIFF* *SNIFFFFF* {user.mention} is {choice}% stinky.")
    print(f"Performed a smell check on another user at {current_time}!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('I like dragons'):
        await message.channel.send('Me too!')

    if message.content.startswith('I do not like dragons'):
        await message.channel.send('BANNED!')

    if message.content.startswith('Saru smells'):
        await message.channel.send('true')

    if message.content.startswith('Did someone say...'):
        await message.channel.send("A triumphant roar echoes from atop the Seat of the Aspects as Nasz'uro,"
                                   " the Unbound Legacy is formed.")

    if message.content.startswith('You smell'):
        await message.channel.send("Thine who smelt it hath dealt it.")

    # if message.content.startswith('LMFAOOO'):
    #     await message.channel.send("Hato told me to stop bullying you guys. I'm sorry.")

    if message.content.startswith('admin'):
        await message.channel.send("Admin can not assist with events that they did not witness. I may have been online,"
                                   "  but I am not capable of monitoring every situation. Check yourself and file a "
                                   "report.")

    if message.content.startswith('ADMIN'):
        await message.channel.send("Admin can not assist with events that they did not witness. I may have been online,"
                                   " but I am not capable of monitoring every situation. Check yourself and file a "
                                   "report.")

    if message.content.startswith('Admin'):
        await message.channel.send("Admin can not assist with events that they did not witness. I may have been online,"
                                   " but I am not capable of monitoring every situation. Check yourself and file a "
                                   "report.")


client.run(client_key)
