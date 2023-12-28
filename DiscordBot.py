import discord
from discord import app_commands
from discord.ext import commands
from config import TOKEN

client = commands.Bot(command_prefix="!", intents = discord.Intents.all())

#class MyClient(discord.Client):
@client.event
async def on_ready():
    print("Bot is logged in.")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@client.event
async def on_raw_reaction_add(garbage, payload):
    message_id = payload.message_id
    if message_id == 1189301652554010624:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        #these work if the name of the role is NOT the same as the emoji 
        if payload.emoji.name == 'Flipper':
            print('Flipper Add')
            role = discord.utils.get(guild.roles, name='Flipper Peeps')
        elif payload.emoji.name == 'OffSec':
            role = discord.utils.get(guild.roles, name='OffSec Peeps')
        elif payload.emoji.name == 'Server':
            role = discord.utils.get(guild.roles, name='Server Peeps')
        else:
            #this works if the name of the role is the same as the name of the emoji
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
            
        if role is not None:
            #assigning the role to the user
            #member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            member = await(await client.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)
            if member is not None:
                await member.add_roles(role)
                print('done')
            else:
                print('Member not found')
        else:
            print('Role not found')

@client.event
async def on_raw_reaction_remove(garbage, payload):
    message_id = payload.message_id
    if message_id == 1189301652554010624:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        #these work if the name of the role is NOT the same as the emoji 
        if payload.emoji.name == 'Flipper':
            print("Flipper Remove")
            role = discord.utils.get(guild.roles, name='Flipper Peeps')
        elif payload.emoji.name == 'OffSec':
            role = discord.utils.get(guild.roles, name='OffSec Peeps')
        elif payload.emoji.name == 'Server':
            role = discord.utils.get(guild.roles, name='Server Peeps')
        else:
            #this works if the name of the role is the same as the name of the emoji
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
            
        if role is not None:
            #assigning the role to the user
            #member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            member = await(await client.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)
            if member is not None:
                await member.remove_roles(role)
                print('done')
            else:
                print('Member not found')
        else:
            print('Role not found')

    # hello command
@client.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!")

@client.tree.command(name="say")
@app_commands.describe(arg = "What should the bot say")
async def say(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{arg}'")

#intents = discord.Intents.all()
#intents.message_content = True

#client = MyClient(intents=intents)
client.run(TOKEN)
