# bot.py
from asyncio.windows_events import NULL
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')
command_prefix = '$'

bot = commands.Bot(command_prefix=command_prefix)

# FUNCTION DEFINTIONS
async def join_call(ctx):
    for vc in ctx.guild.voice_channels:
        for member in vc.members:
            if ctx.message.author.name == member.name:
                try:
                    await vc.connect()
                    return True, vc
                except discord.ClientException:
                    for v_client in bot.voice_clients:
                        if v_client.guild == ctx.message.guild:
                            await v_client.move_to(vc)
                    return True, vc
                except:
                    print('uh oh')
                return False, NULL
    await ctx.send(ctx.message.author.name + ' isn\'nt in a voice channel :(')
    return False, NULL

async def disconnect_call(ctx):
    for v_client in bot.voice_clients:
        if v_client.guild == ctx.message.guild:
            vc_name = v_client.channel.name
            await v_client.disconnect()
            await ctx.send('Disconnected from the ' + vc_name + ' channel')
            
async def play_audio(ctx):
    return
            
# EVENTS
@bot.event
async def on_connect():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
        
# COMMANDS
@bot.command(name='join_call')
async def join(ctx):
    await join_call(ctx)
    
@bot.command(name='disconnect')
async def disconnect(ctx):
    await disconnect_call(ctx)
            
@bot.command(name='bakamitai')
async def bakamitai(ctx):
    in_call, vc = await join_call(ctx)
    if in_call:
        for v_client in bot.voice_clients:
            if v_client.channel.id == vc.id:
                await ctx.send('yay')
                return     


@bot.command(name='shutdown')
async def shutdown(ctx):
    await disconnect_call(ctx)
    await ctx.send('BYE BYE')
    await bot.close()



bot.run(TOKEN)