#!/usr/bin/env python3
from discord.ext import commands
import requests
import discord
import os

bot = commands.Bot(command_prefix=';mp3;')
TOKEN="dummy"

que = []
basefiles = os.listdir()
stop=False

@bot.event
async def on_ready():
    print("Bot Started")

@bot.command()
async def play(ctx):
    global que, stop
    stop = False
    clean()
    if ctx.author.voice is None:
        await ctx.send('ボイスチャンネルに参加してからコマンドを打ってください。')
        return
    if len(ctx.message.attachments) == 0:
        await ctx.send("ファイルを添付して下さい。")
        return
    filename = ctx.message.attachments[0].filename
    download_audio(ctx.message.attachments[0].url, filename)
    channel = ctx.author.voice.channel
    vc = ctx.voice_client
    if vc != None:
        if vc.is_playing():
            que.append(filename)
            await ctx.send(filename+"がキューに追加されました。")
            return
        else:
            await vc.move_to(channel)
    else:
        vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(source=filename),after=lambda e: nextque(e,ctx))
    await ctx.send(filename+"を再生します。")
    return

@bot.command()
async def play_direct(ctx, url):
    global que, stop
    stop = False
    clean()
    if ctx.author.voice is None:
        await ctx.send('ボイスチャンネルに参加してからコマンドを打ってください。')
        return
    filename = os.path.basename(url)
    download_audio(url, filename)
    channel = ctx.author.voice.channel
    vc = ctx.voice_client
    if vc != None:
        if vc.is_playing():
            que.append(filename)
            await ctx.send(filename+"がキューに追加されました。")
            return
    else:
        vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(source=filename),after=lambda e: nextque(e,ctx))
    await ctx.send(filename+"を再生します。")
    return

@bot.command()
async def stop(ctx):
    global stop
    stop = True
    if ctx.voice_client != None and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("音楽を停止しました。")
    else:
        await ctx.send("音楽は再生されていません。")

@bot.command()
async def exit(ctx):
    if ctx.voice_client != None:
        await ctx.voice_client.disconnect()
        await ctx.send("botは退出しました。")
    else:
        await ctx.send("botは既に退出しています。")

@bot.command()
async def next(ctx):
    if ctx.voice_client == None:
        await ctx.send("このbotはボイスチャンネルに参加していません。")
        return
    global que, stop
    stop = False
    clean()
    if len(que) != 0:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("曲をスキップします。")
            nextque(None,ctx)
        else:
            filename = que.pop(0)
            await ctx.send(filename+"を再生します。")
            ctx.voice_client.play(discord.FFmpegPCMAudio(source=filename),after=lambda e: nextque(e,ctx))
    else:
        await ctx.send("キューに曲が存在しません。")

def clean():
    global basefiles, que
    [os.remove(s) for s in list(set(os.listdir())-set(basefiles+que))]

def download_audio(url, file_name): #添付ファイルをダウンロードする
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(r.content)
        return file_name

def nextque(er,ctx):
    global stop
    if stop:
        return
    vc = ctx.voice_client
    if vc == None:
        return
    if vc.is_playing():
        vc.stop()
    global que
    if len(que) != 0:
        filename = que.pop(0)
        vc.play(discord.FFmpegPCMAudio(source=filename),after=lambda e: nextque(e,ctx))

bot.run(TOKEN)
