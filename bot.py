# bot.py

import os
import discord
from discord.errors import ClientException
from dotenv import load_dotenv
from discord.ext import tasks, commands
import speech_recognition as sr

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
                return False, None
    await ctx.send(ctx.message.author.name + ' isn\'t in a voice channel :(')
    return False, None

async def disconnect_call(ctx):
    for v_client in bot.voice_clients:
        if v_client.guild == ctx.message.guild:
            vc_name = v_client.channel.name
            await v_client.disconnect()
            await ctx.send('Disconnected from the ' + vc_name + ' channel')
        
async def listen(ctx):
    r = sr.Recognizer()
    r.energy_threshold = 300
    speech = None
    with sr.Microphone(device_index=1, sample_rate=16000, chunk_size=1024) as source:
        print("Sphinx is listening")
        audio = r.listen(source)
    try:
        print("Text: " + r.recognize_sphinx(audio, language='en-US'))
        speech = r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
        
    return await process_speech(ctx, speech)
              
async def process_speech(ctx, speech):
    if not speech:
        print('no text to process')
    if 'playing music' in speech:
        await playfile(ctx, './audio/sample.mp3')
    elif 'karaoke' in speech:
        await playfile(ctx, './audio/bakamitai.mp3')
    print('done')
    # return await listen()
    
            
# EVENTS
@bot.event
async def on_connect():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

@bot.event
async def on_voice_state_update(user, before, after):
    for v_client in bot.voice_clients:
        if v_client.guild == user.guild:
            if len(v_client.channel.members) == 1:
                await v_client.disconnect()
        
# COMMANDS
@bot.command(name='vc')
async def join(ctx):
    in_vc,_ =await join_call(ctx)
    if in_vc:
        await listen(ctx)
    
@bot.command(name='disconnect')
async def disconnect(ctx):
    await disconnect_call(ctx)
            
@bot.command(name='bakamitai')
async def bakamitai(ctx):
    in_call, vc = await join_call(ctx)
    if in_call:
        for v_client in bot.voice_clients:
            if v_client.channel.id == vc.id:
                await playfile(ctx, './audio/bakamitai.mp3')     

@bot.command(name='playfile')
async def playfile(ctx, file):
    print(file)
    await join_call(ctx)
    for v_client in bot.voice_clients:
        if v_client.guild == ctx.message.guild:
            v_client.stop() 
            v_client.play(discord.FFmpegOpusAudio( \
                executable="C:/ffmpeg/bin/ffmpeg.exe", source=file, bitrate=128))
            # v_client.play(discord.FFmpegPCMAudio( \
            #     executable="C:/ffmpeg/bin/ffmpeg.exe", source=file))


@bot.command(name='shutdown')
async def shutdown(ctx):
    await disconnect_call(ctx)
    await ctx.send('BYE BYE')
    await bot.close()

# TASKS

# BOT RUN
bot.run(TOKEN)