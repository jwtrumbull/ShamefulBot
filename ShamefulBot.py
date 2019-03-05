#ShamefulBot by ShamefulPenguin

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import os
import youtube_dl

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print ("My body is ready")

"""

These detect if any text contains the phrase that is looked for, then does something

"""
@bot.event
async def on_message(message):
    user = message.author.name
    if 'kun' in message.content:
        await bot.send_message(message.channel, user + ":open_mouth:")
    await bot.process_commands(message)

@bot.event
async def on_message(m1):
    user = m1.author.name
    if 'g2' in m1.content:
        await bot.send_message(m1.channel, "Did someone just mention the best team? G2 ARMY")
    await bot.process_commands(m1)

#bot.remove_command('help')

#@bot.command(pass_context=True)
#async def help(ctx):
#    embed = discord.Embed(title="nice bot", description="A Very Nice bot. List of commands are:", color=0xeee657)

#    embed.add_field(name="$add X Y", value="Gives the addition of **X** and **Y**", inline=False)
#    embed.add_field(name="$multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
#    embed.add_field(name="$greet", value="Gives a nice greet message", inline=False)
#    embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
#    embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
#    embed.add_field(name="$help", value="Gives this message", inline=False)
#    await bot.say(embed=embed)

"""

Commands that are called by user
A lot of these were made to test the code

"""
@bot.group(pass_context=True)
async def cookie(ctx):
    """Mmmmm cookie"""
    await bot.say(":cookie:")

@bot.group(pass_context=True)
async def bye(ctx):
    """Says bye"""
    await bot.say(":wave: bye bye!")
        
@bot.group(pass_context=True)
async def repeat(ctx, arg):
    """Repeats whatever is after the command"""
    await bot.say(arg)

@bot.group(pass_context=True)
async def smile(ctx):
    """Smiles"""
    await bot.say(":smile:")

@bot.group(pass_context=True)
async def ping(ctx):
    """Pings the chat and the terminal"""
    await bot.say(":ping_pong: Pong!!!")
    
@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    """Shows a users name, id, status, role, date joined, and waifu"""
    if user.name in waifudict:
        waifu = waifudict[user.name]
    else:
        waifu = random.choice(waifus)
    embed = discord.Embed(title="Info of {}-kun".format(user.name), description="This is what I could find", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Role", value=user.top_role, inline=True)
    embed.add_field(name="Joined", value=user.joined_at, inline=True)
    embed.add_field(name="Waifu", value=waifu, inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def rl(ctx, user: discord.Member):
    """Sends a messgae to the user to play Rocket League"""
    await bot.say("Time for Rocket League!!")
    await bot.send_message(user, 'Its time for some Rocket League!!!')
	
@bot.command(pass_context=True)
async def annoy(ctx, user: discord.Member):
    """Sends an annoying message to the user"""
    await bot.say("Sure thing! Ill go annoy ")
    await bot.send_message(user, 'B\nA\nK\nA\nB\nA\nK\nA\nB\nA\nK\nA')
    

@bot.command(pass_context=True)
@commands.has_role("Space Cowboi")
async def kick(ctx, user: discord.Member):
    """Kicks a user from the server, only admins can do this"""
    await bot.say(":boot Cya, {}!".format(user.name))
    await bot.kick(user)
    
@bot.command(pass_context=True)
async def embed(ctx):
    """Used as a refernce for embedding things"""
    embed = discord.Embed(title="test", description="kuuuuunnnnnn", color=0x00ff00)
    embed.set_footer(text="this is a footer")
    embed.set_author(name="Burt Macklin")
    embed.add_field(name="this is a field", value="nope", inline=True)
    await bot.say(embed=embed)

#not done
@bot.command(pass_context=True)
async def clear(ctx, amount=100):
    """Clears the chat channel, not working yet..."""
    channel = ctx.message.channel
    messages = []
    async for message in bot.logs_from(channel, limit=int(amount)+1):
        messages.append(message)
    await bot.delete_messages(messages)
    await bot.say("Messages deleted.")

@bot.command(pass_context=True)

async def poke(ctx, member: discord.Member):
    """Pokes the user"""
    await bot.say("Alrighty!")
    await bot.send_message(member, ":point_right: boooooop")


"""

Music/Video player and the bot channel commands

"""

players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

@bot.command(pass_context=True)
async def join(ctx):
    """Bot joins your current channel"""
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)

@bot.command(pass_context=True)
async def leave(ctx):
    """Bot leaves current channel"""
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    await voice_client.disconnect()

@bot.command(pass_context=True)
async def play(ctx, url):
    """Plays the given url or adds it to the queue"""
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
        player.start()

@bot.command(pass_context=True)
async def pause(ctx):
    """Pauses the current thing playing"""
    id = ctx.message.server.id
    players[id].pause()

@bot.command(pass_context=True)
async def stop(ctx):
    """Pauses the current thing playing and empties queue"""
    id = ctx.message.server.id
    players[id].stop()

@bot.command(pass_context=True)
async def resume(ctx):
    """Resumes current item in queue"""
    id = ctx.message.server.id
    players[id].resume()

@bot.command(pass_context=True)
async def skip(ctx):
    """Go to next item in queue, not working yet..."""
    id = ctx.message.server.id

@bot.command(pass_context=True)
async def queue(ctx, url):
    """Plays the given url or adds it to the queue"""
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
        player.start()

    await bot.say('Video has been Queued')

"""

Waifu part of code

"""
waifus = ['Rem', 'Ram', 'Asuna', 'Ochaco', 'Winry', 'Emi', 'Lucy', 'Hestia', 'Emilia', 'Akatsuki', 'Tetora', 'Felix']

waifudict = {"Shame" : "Emilia", "amazingness" : "Rem", "Katar": "Ochaco", "Yoohoo": "Felix"} 

waifushow = {
    'Rem': 'Re:Zero', 
    'Ram': 'Re:Zero', 
    'Asuna': 'Sword Art Online', 
    'Ochaco': 'My Hero Academia', 
    'Winry': 'Full Metal Alchemist', 
    'Emi': 'The Devil is a Part Timer', 
    'Lucy': 'Fairy Tail', 
    'Hestia': 'Is it Wrong to Pick Up Girls in a Dungeon', 
    'Emilia': 'Re:Zero', 
    'Akatsuki': 'Log Horizon', 
    'Tetora': 'Log Horizon',
    'Felix': 'Re:Zero'
}

@bot.group(pass_context=True)
async def waifu(ctx):
    """Shows the user's Waifu UwU
    If there is not set waifu, then one is chosen at random"""
    user = ctx.message.author.name
    if user in waifudict:
        waif = waifudict[user]
    else:
        waif = random.choice(waifus)

    await bot.say("Your waifu is " + waif)
    
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filelocation = 'data/pics/' + waif + '.txt'
    filename = os.path.join(fileDir, filelocation)
    r = readFile(filename)
    pic = random.choice(r.split())

    embed = discord.Embed()
    show = waifushow[waif]
    embed.add_field(name="Anime", value=show, inline=True)
    embed.set_image(url = pic)
    await bot.say(embed=embed)
    
'''Goal is to have it find /data/pics/rem.txt when !rem is typed the print one of the pics inside it
This can later be automated to find *.txt and print a random pic from the file
Ex. !pic Emilia or !Emilia but not having to rewrite the same code for every single person'''
@bot.group(pass_context=True)
async def rem(ctx):
    """Shows a random picture of Rem
    In the future I want to change this to find any picture of anything in the files"""
    com = 'rem'
    waif = 'Rem'
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, 'data/pics/rem.txt')
    r = readFile(filename)
    pic = random.choice(r.split())
    embed = discord.Embed()
    embed.set_image(url = pic)
    await bot.say(embed=embed)    

@bot.group(pass_context=True)
async def setWaifu(ctx, arg):
    """Set your waifu, not working yet..."""
    pass

@bot.group(pass_context=True)
async def randomWaifu(ctx):
    """Displays a picture of a random Waifu"""
    waif = random.choice(waifus)
    show = waifushow[waif]

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filelocation = 'data/pics/' + waif + '.txt'
    filename = os.path.join(fileDir, filelocation)
    r = readFile(filename)
    pic = random.choice(r.split())

    embed = discord.Embed()
    embed.add_field(name="Name", value=waif, inline=True)
    embed.add_field(name="Anime", value=show, inline=True)
    embed.set_image(url = pic)
    await bot.say(embed=embed)


def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
       if random.randrange(num + 2): continue
       line = aline
    return line

'''Reads the entire file'''
def readFile(filename):
    filehandle = open(filename)
    return filehandle.read()
    filehandle.close()
    

@bot.group(pass_context=True)
async def tets(ctx):
    """Tester function, don't worry about it"""
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, 'data/pics/same.txt')
    r = readFile(filename)
    await bot.say(r)






bot.run(os.getenv('BOT_TOKEN'))

input('Press ENTER to exit')