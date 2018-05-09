import discord
from discord.ext.commands import Bot
from discord.ext import commands
import discord.channel
import asyncio
import time
import sys
import datetime
from datetime import datetime
from datetime import timezone
from time import gmtime, strftime
#run me in Python 3.6.4

Client = discord.Client()
client = commands.Bot(command_prefix = "?")
prefix = "?"
logchannel = '443530106065911829'
dt = datetime.now()

@client.event
async def on_ready():
    print("Bot is online and connected to Discord")
    print(client.get_channel('443530106065911829'))
        

@client.event
async def on_message(message):
    #logging function
    print(message.author.name + " said " + message.content + " at " + str(message.timestamp))
    if message.content.upper().startswith(prefix + 'PING'):
        userID = message.author.id
        t1 = time.perf_counter()
        await client.send_typing(message.channel)
        t2 = time.perf_counter()
        ping = format(round((t2-t1)*1000))
        em = discord.Embed(title='Bot Ping', description=ping + 'ms', colour=0x00ecff)
        em.set_author(name='Cooler Bot', icon_url=client.user.avatar_url)
        await client.send_message(message.channel, embed=em)
    elif message.content.upper().startswith(prefix + 'SAY'):
        await say(message)
    elif message.content.upper().startswith(prefix + 'STATUS'):
        await change_status(message)
    elif message.content.upper().startswith(prefix + 'USERINFO'):
        await user_info(message)
        




#METHODS FOR COMMANDS
#
#
#
@client.event
async def say(message):
    args = message.content.split(" ")
    await client.send_message(message.channel, "%s" % (" ".join(args[1:])))

@client.event
async def change_status(message):
    print('Changing status')
    if 'ONLINE' in message.content.upper():
        await client.change_presence(game=None, status=discord.Status('online'), afk=False)
    if 'DND' in message.content.upper():
        await client.change_presence(game=None, status=discord.Status('dnd'), afk=False)
    if 'IDLE' in message.content.upper():
        await client.change_presence(game=None, status=discord.Status('idle'), afk=False)
    if 'INVISIBLE' in message.content.upper():
        await client.change_presence(game=None, status=discord.Status('invisible'), afk=False)

@client.event
async def user_info(message):
    for server in client.servers:
        for member in server.members:
            if member.mention in message.content:
                em = discord.Embed(title='Username     Account Age', description=member.name + '    ' + member.created_at +' ',timestamp=datetime.now(),colour=0xf44242)
                em.set_author(name=message.author.name,icon_url=message.author.avatar_url)
                em.set_footer(text='ID:' + message.author.id)
                await client.send_message(client.get_channel(lmessage.channel), embed=em)
                
#LOGGING METHODS
#
#
#
@client.event
async def on_message_delete(message):
    #await client.send_message(logchannel, "User" + message.author.name + " deleted the following:\n" + message.content)
    em = discord.Embed(title=':x: Message Deleted', description='Message sent by <@' + message.author.id + '> deleted in <#' + message.channel.id + '> \n`' + message.content +'`',timestamp=datetime.now(),colour=0xf44242)
    em.set_author(name=message.author.name,icon_url=message.author.avatar_url)
    em.set_footer(text='ID:' + message.author.id)
    await client.send_message(client.get_channel(logchannel), embed=em)

@client.event
async def on_message_edit(before, after):
    if (before.author.bot):
        return
    em = discord.Embed(title=':pencil: Message Edited', description='Message sent by <@' + before.author.id + '> edited in <#' + before.channel.id + '> \n**Original:** `' + before.content + '`\n**Edited:**    `' + after.content + '`',timestamp=datetime.now(),colour=0xf4d041)
    em.set_author(name=before.author.name,icon_url=before.author.avatar_url)
    em.set_footer(text='ID:' + before.author.id)
    await client.send_message(client.get_channel(logchannel), embed=em)

@client.event
async def on_member_join(member):
    em = discord.Embed(title=':wave: User Joined', description='User <@' + member.id + '> has joined the server!',timestamp=datetime.now(), colour=0x6df441)
    em.set_author(name=member.name,icon_url=member.avatar_url)
    em.set_footer(text='ID:' + member.id + '•' + datetime.now().strftime("%-I:%M %p"))
    await client.send_message(client.get_channel(logchannel), embed=em)

@client.event
async def on_member_remove(member):
    em = discord.Embed(title=':wave: User Left', description='User <@' + member.id + '> has left the server. Hope to see you again soon, <@' + member.id+'>!',timestamp=datetime.now(), colour=0xf46d41)
    em.set_author(name=member.name,icon_url=member.avatar_url)
    em.set_footer(text='ID:' + member.id + '•' + datetime.now().strftime("%-I:%M %p"))
    await client.send_message(client.get_channel(logchannel), embed=em)

#name of token, connects to Discord with token to auth
client.run("NDQyMTEyNjY0MzE1ODg3NjE2.DdDX2A.jVyidJh4_hzmY-Ny2zV0xq_6rjE")
