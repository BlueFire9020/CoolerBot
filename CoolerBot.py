import discord
from discord.ext.commands import Bot
from discord.ext import commands
import discord.channel
import asyncio
import time
import sys
import datetime
import time
from datetime import datetime
from datetime import timezone
from time import gmtime, strftime
import json
from pprint import pprint
#run me in Python 3.6.4

Client = discord.Client()
client = commands.Bot(command_prefix = "?")
logchannel = '443530106065911829'
dt = datetime.now()

@client.event
async def on_ready():
    print("Bot is online and connected to Discord")
    for server in client.servers:
        await load_json(server)


       
#MESSAGE HANDLER/DELEGATION
#
#
#
@client.event
async def on_message(message):
    args = message.content.split(" ")
    prefix = str(await load_json_val(message.server,"prefix"))
    #logging function
    #print(message.author.name + " said " + message.content + " at " + str(message.timestamp))
    if message.content.upper().startswith(prefix + 'PING') or message.content.upper().startswith(prefix + 'PONG'):
        global time
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
        creator = await is_creator(message)
        if creator == True:
            await change_status(message)
        else:
            await client.send_message(message.channel,"You are not the chosen one!")
    elif message.content.upper().startswith(prefix + 'USERINFO'):
        await user_info(message)
    elif (str(args[0].upper())) == prefix + "NICK" or (str(args[0].upper())) == prefix + "NICKNAME":
         try:
             if args[1] is not None:
                 await edit_json_val(message.server,"nickname",(" ".join(args[1:])))
         except:
             var = await load_json_val(message.server,"nickname")
             await client.send_message(message.channel,"The bot's nickname is: `" + var + "`")
        
    elif (str(args[0].upper())) == prefix + "PREFIX" or str(args[0].upper()) == prefix + "PREF":
        args = message.content.split(" ")
        try:
            await change_pref(args[1],message.server)
            var = await load_json_val(message.server,"nickname")
            await client.send_message(message.channel, var + "'s prefix has been successfully changed to `" + args[1] + "`")
        except:
            val = await load_json_val(message.server,"prefix")
            await client.send_message(message.channel,"The bot's prefix is: `" + val + "`")
    elif message.content.upper().startswith(prefix + 'KILL'):
        creator = await is_creator(message)
        if creator == True:
            await client.send_message(message.channel,"Killing the bot...")
            await sys.exit("Killed with user command")
        else:
            await client.send_message(message.channel,"You are not the chosen one!")
    elif (str(args[0].upper())) == prefix + "LOGCHANNEL":
        args = message.content.split(" ")
        if args[1] is not None:
            await edit_json_val(message.server,"logchannel",args[1])
            channel = await load_json_val(message.server,"logchannel")
            await client.send_message(message.channel,"Log channel changed to : `" + str(message.server.get_channel(args[1]).name) +"`")
        else:
            await client.send_message(message.channel,"Something went wrong! Make sure you only have one parameter and that parameter is the Log Channel ID.")
    elif message.content.upper().startswith(prefix + 'INVITES'):
        for invite in await client.invites_from(message.server):
            em = discord.Embed(title='Invite Link', description=' ', colour=0x00d0ff)
            em.add_field(name="Link",value=str(invite.url),inline=False)
            em.add_field(name="Created At",value=str(invite.created_at),inline=False)
            em.add_field(name="Uses",value=str(invite.uses),inline=True)
            em.add_field(name="Channel",value=str(invite.channel),inline=True)
            em.set_footer(text="Invite created by " + str(invite.inviter))
            await client.send_message(message.channel,embed=em)
    elif message.content.upper().startswith(prefix + 'NICKELBACK'):
        await client.send_message(message.channel, "https://i.ytimg.com/vi/uNZ5P4C5E24/maxresdefault.jpg")
    elif message.content.upper().startswith(prefix + 'BAN') or message.content.upper().startswith(prefix + 'BANUSER'):
        args = message.content.split(" ")
        try:
            time = 1
            try:
                print(args[2])
                time = args[2]
            except:
                print("error!")
            if ("<@" in args[1]):
                trimmed = args[1].strip('<@!>')
                success = await ban_user(message.server, trimmed, time)
            else:
                success = await ban_user(message.server,args[1],time)
            if (success == True):
                await client.send_message(message.channel, ":white_check_mark: Successfully banned user!")
            else:
                await client.send_message(message.channel, ":thinking: Uh oh! Something went wrong!")
        except:
            await client.send_message(message.channel,":x: Error! No user ID or amount of messages to delete given!")
    elif message.content.upper().startswith(prefix + 'UNBAN') or message.content.upper().startswith(prefix + 'UNBANUSER'):
        args = message.content.split(" ")
        try:
            if ("<@" in args[1]):
                trimmed = args[1].strip('<@!>')
                success = await unban_user(message.server, trimmed)
            else:
                success = await unban_user(message.server,args[1])
            if (success == True):
                await client.send_message(message.channel, ":white_check_mark: Successfully unbanned user!")
            else:
                await client.send_message(message.channel, ":thinking: Uh oh! Something went wrong!")
        except:
            await client.send_message(message.channel,":x: Error! No user ID to unban given!")
    elif message.content.upper().startswith(prefix + 'KICK'):
        args = message.content.split(" ")
        try:
            if ("<@" in args[1]):
                trimmed = args[1].strip('<@!>')
                success = await kick_user(message.server, trimmed)
            else:
                success = await kick_user(message.server, args[1])
            if (success == True):
                await client.send_message(message.channel, ":white_check_mark: Successfully kicked user!")
            elif (success == False):
                await client.send_message(message.channel, ":thinking: Something went wrong, unable to kick user.")
        except:
            await client.send_message(message.channel,":x: Error! Missing user param!")




#METHODS FOR COMMANDS
#
#
#
@client.event
async def make_invite(message):
    args = message.content.split(" ")
    client.create_invite


@client.event
async def say(message):
    args = message.content.split(" ")
    await client.send_message(message.channel, "%s" % (" ".join(args[1:])))

@client.event
async def change_status(message):
    print('Changing status')
    if 'ONLINE' in message.content.upper():
        await client.change_presence(game=None, status=discord.Status('online'), afk=False)
    elif 'DND' in message.content.upper():
        await client.change_presence(game=None, status=discord.Status('dnd'), afk=False)
    elif 'IDLE' in message.content.upper():
        await client.change_presence(game=None, status=discord.Status('idle'), afk=False)
    elif 'INVISIBLE' in message.content.upper():
        await client.change_presence(game=None, status=discord.Status('invisible'), afk=False)
    #else, default to returning error
    else:
        await client.send_message(message.channel,"Error: No applicable status given.")
        

@client.event
async def user_info(message):
    args = message.content.split(" ")
    try:
        trimmed = args[1].strip('<@!>')
    print(trimmed)
    user = await client.get_user_info(trimmed)
    em = discord.Embed(title='User Info',description='**Username: **' + user.name + '#' + user.discriminator + '\n\n**Bot User: **' + str(user.bot) + '\n\n**Nickname: **' + user.display_name +'\n\n**Account Creation Date: **' + str(user.created_at) + '\n\n',timestamp=datetime.now(),colour=0xf44242)
    em.set_author(name=user.name,icon_url=user.avatar_url)
    em.set_footer(text='ID:' + user.id)
    em.set_thumbnail(url=str(user.avatar_url))
    await client.send_message(message.channel, embed=em)
    

@client.event
async def change_nick(nick,server):
    await edit_json_val(server,"nickname",nick)

@client.event
async def change_pref(pref,server):
    with open('serverJSON/'+server.id+'.json') as f:
        data = json.load(f)
        data["prefix"] = pref
    jsonFile = open("serverJSON/"+server.id+".json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()
    await load_json(server)
    print('done')

@client.event
async def ban_user(server,user,days):
    for member in server.members:
        print(member.id + "vs" + user)
        if member.id == str(user):
            print("is this happening?")
            await client.ban(member,delete_message_days=days)
            return True
    return False

@client.event
async def unban_user(server,user):
    try:
        _user = await client.get_user_info(str(user))
        await client.unban(server,_user)
        return True
    except:
        return False
            
@client.event
async def kick_user(server, user):
    try:
        print("we're here")
        _user = server.get_member(user)
        print("now we're here")
        await client.kick(_user)
        return True
    except:
        return False
        

#AUTHENTICATION METHODS
#
#
#
@client.event
async def is_creator(message):
    if message.author.id == '261965535778963457':
        return True
    else:
        return False


#JSON METHODS
#
#
#
@client.event
async def load_json(server):
    with open('serverJSON/'+server.id+'.json') as f:
        data = json.load(f)
        await client.change_nickname(server.me,data["nickname"])
        #await client.change_presence(game=None, status=discord.Status(data["status"]), afk=False)
        global prefix
        prefix = data["prefix"]
        global logchannel
        logchannel = data["logchannel"]
        
async def load_json_val(server, valName):
    with open('serverJSON/'+server.id+'.json') as f:
        data = json.load(f)
        val = data[valName]
    return val

async def edit_json_val(server, valName, newVal):
    with open('serverJSON/'+server.id+'.json') as f:
        data = json.load(f)
        data[valName] = newVal
    jsonFile = open("serverJSON/"+server.id+".json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()
    await load_json(server)
    
    
                
#LOGGING METHODS
#
#
#
@client.event
async def on_message_delete(message):
    #await client.send_message(logchannel, "User" + message.author.name + " deleted the following:\n" + message.content)
    message2 = message
    em = discord.Embed(title=':x: Message Deleted', description='Message sent by <@' + message.author.id + '> deleted in <#' + message.channel.id + '> \n`' + message.content +'`',timestamp=datetime.now(),colour=0xf44242)
    em.set_author(name=message.author.name,icon_url=message.author.avatar_url)
    em.set_footer(text='ID:' + message.author.id)
    await client.send_message(client.get_channel(await load_json_val(message2.server,"logchannel")), embed=em)

@client.event
async def on_message_edit(before, after):
    if (before.author.bot):
        return
    if (str(before.content) == str(after.content)):
        return
    em = discord.Embed(title=':pencil: Message Edited', description='Message sent by <@' + before.author.id + '> edited in <#' + before.channel.id + '> \n**Original:** `' + before.content + '`\n**Edited:**    `' + after.content + '`',timestamp=datetime.now(),colour=0xf4d041)
    em.set_author(name=before.author.name,icon_url=before.author.avatar_url)
    em.set_footer(text='ID:' + before.author.id)
    await client.send_message(client.get_channel(await load_json_val(before.server,"logchannel")), embed=em)

@client.event
async def on_member_join(member):
    em = discord.Embed(title=':wave: User Joined', description='User <@' + member.id + '> has joined the server!',timestamp=datetime.now(), colour=0x6df441)
    em.set_author(name=member.name,icon_url=member.avatar_url)
    em.set_footer(text='ID:' + member.id + '•' + datetime.now().strftime("%-I:%M %p"))
    await client.send_message(client.get_channel(await load_json_val(member.server,"logchannel")), embed=em)

@client.event
async def on_member_remove(member):
    if (member in await client.get_bans(member.server)):
        print("user was banned!")
        return
    em = discord.Embed(title=':wave: User Left', description='User <@' + member.id + '> has left the server. Hope to see you again soon, <@' + member.id+'>!',timestamp=datetime.now(), colour=0xf46d41)
    em.set_author(name=member.name,icon_url=member.avatar_url)
    em.set_footer(text='ID:' + member.id + '•' + datetime.now().strftime("%-I:%M %p"))
    await client.send_message(client.get_channel(await load_json_val(member.server,"logchannel")), embed=em)

@client.event
async def on_channel_create(channel):
    em = discord.Embed(title=':white_check_mark: Channel Created', description='**Channel Name:**' + channel.name + '\n**Channel Type:**' + str(channel.type),timestamp=datetime.now(), colour=0x6df441)
    em.set_author(name=client.user.name,icon_url=client.user.avatar_url)
    em.set_footer(text='ID:' + channel.id)
    await client.send_message(client.get_channel(await load_json_val(channel.server,"logchannel")), embed=em)

@client.event
async def on_channel_delete(channel):
    em = discord.Embed(title=':x: Channel Deleted', description='**Channel Name:**' + channel.name + '\n**Channel Type:**' + str(channel.type),timestamp=datetime.now(), colour=0xf44242)
    em.set_author(name=client.user.name,icon_url=client.user.avatar_url)
    em.set_footer(text='ID:' + channel.id)
    await client.send_message(client.get_channel(await load_json_val(channel.server,"logchannel")), embed=em)

@client.event
async def on_server_role_create(role):
    em = discord.Embed(title=':bust_in_silhouette: Role Created', description='**Role Name: **' + role.name,timestamp=datetime.now(), colour=role.colour.value)
    em.set_author(name=client.user.name,icon_url=client.user.avatar_url)
    em.set_footer(text='ID:' + role.id)
    await client.send_message(client.get_channel(await load_json_val(role.server,"logchannel")), embed=em)

@client.event
async def on_server_role_delete(role):
    em = discord.Embed(title=':x: Role Deleted', description='**Role Name: **' + role.name,timestamp=datetime.now(), colour=role.colour.value)
    em.set_author(name=client.user.name,icon_url=client.user.avatar_url)
    em.set_footer(text='ID:' + role.id)
    await client.send_message(client.get_channel(await load_json_val(role.server,"logchannel")), embed=em)


@client.event
async def on_server_role_update(before,after):
    if (before.permissions == after.permissions):
        return
    content = ("**Role Name: ** `" + after.name + "`\n**Can Kick: **`" + str(after.permissions.kick_members)+ "`\n**Can Ban: **`" + str(after.permissions.ban_members)
               + "`\n**Admin: **`" + str(after.permissions.administrator) + "`\n**Manage Channels: **`" + str(after.permissions.manage_channels) + "`\n**Manage Server: **`" +
               str(after.permissions.manage_server) + "`\n**Manage Messages: **`" + str(after.permissions.manage_messages) + "`\n**Mention Everyone: **`" + str(after.permissions.mention_everyone) + "`")
    em = discord.Embed(title=':wrench: Role Updated',
                       description=content,timestamp=datetime.now(), colour=after.colour.value)
    em.set_author(name=client.user.name,icon_url=client.user.avatar_url)
    em.set_footer(text='ID:' + after.id)
    await client.send_message(client.get_channel(await load_json_val(before.server,"logchannel")), embed=em)

@client.event
async def on_member_ban(member):
    em = discord.Embed(title=':hammer: User Banned', description='**User: **' + member.name,timestamp=datetime.now(), colour=0xf44242)
    em.set_author(name=member.name,icon_url=member.avatar_url)
    em.set_footer(text='ID:' + member.id)
    await client.send_message(client.get_channel(await load_json_val(member.server,"logchannel")), embed=em)

@client.event
async def on_member_unban(server, member):
    em = discord.Embed(title=':no_entry: User Unbanned', description='**User: **' + member.name,timestamp=datetime.now(), colour=0x6df441)
    em.set_author(name=member.name,icon_url=member.avatar_url)
    em.set_footer(text='ID:' + member.id)
    await client.send_message(client.get_channel(await load_json_val(server,"logchannel")), embed=em)


#name of token, connects to Discord with token to auth
client.run("NDQyMTEyNjY0MzE1ODg3NjE2.DdDX2A.jVyidJh4_hzmY-Ny2zV0xq_6rjE")
