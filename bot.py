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
async def join_call(ctx):
    for vc in ctx.guild.voice_channels:
        for member in vc.members:
            if ctx.message.author.name == member.name:
                try:
                    await vc.connect()
                    await ctx.send('done')
                except discord.ClientException:
                    for v_client in bot.voice_clients:
                        if v_client.guild == ctx.message.guild:
                            await v_client.move_to(vc)
                            await ctx.send('done')
                except:
                    print('uh oh')
            break
    
@bot.command(name='disconnect')
async def disconnect(ctx):
    for v_client in bot.voice_clients:
        if v_client.guild == ctx.message.guild:
            vc_name = v_client.channel.name
            await v_client.disconnect()
            await ctx.send('Disconnected from the ' + vc_name + ' channel')
            
@bot.command(name='bakamitai')


@bot.command(name='shutdown')
async def shutdown(ctx):
    await ctx.send('BYE BYE')
    await bot.close()



bot.run(TOKEN)