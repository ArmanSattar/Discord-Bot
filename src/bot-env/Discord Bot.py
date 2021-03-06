import discord
import random
import youtube_dl
import unicodedata
from enum import Enum
from discord.ext import commands
import filemanip
import scraper

#suppresses noise from errors

youtube_dl.utils.bug_reports_message = lambda: ''

#creates an instance of a bot and stores it into the variable client to be manipulated later

client = commands.Bot(command_prefix = '.', help_command=None)
client.remove_command('help')

class Subject(Enum):
    Maths = 'Maths'

#creates a tuple and 2 lists

player = {}
roleList = []
links = []

topicList = [
    'Algebraic Expressions',
    'Quadratics',
    'Equations and Inequalities',
    'Graphs and Inequalities',
    'Straight Line Graphs',
    'Circles',
    'Algebraic Methods',
    'Binomial Expansion',
    'Trigonometric Ratios',
    'Trigonometric Identities',
    'Vectors',
    'Differentiation',
    'Integration',
    'Exponentials and Logarithms'
]

downloadId = [
    '11g6CFYPjitvo-1XcroOO6lHxRApmZ4fi'
]

eightBallResponses = [
    'As I see it, yes.',
    'Ask again later.',
    'Better not tell you now.',
    'Cannot predict now.',
    'Concentrate and ask again.',
    'Don’t count on it.',
    'It is certain.',
    'It is decidedly so.',
    'Most likely.',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Outlook good.',
    'Reply hazy, try again.',
    'Signs point to yes.',
    'Very doubtful.',
    'Without a doubt.',
    'Yes.',
    'Yes – definitely.',
    'You may rely on it.'
    ]

def TopicChecker(topicName, counter):
    
    if topicName in topicList:
        if topicList[counter] == topicName:
            return links[counter]
        else:
            counter += 1
            return TopicChecker(topicName, counter)

async def UploadFile(ctx, path):
    await ctx.channel.send(file=discord.File(path))

@client.event
async def on_message(message):
    member = message.author
    role = discord.utils.get(message.guild.roles, name = 'member')
    
    if message.channel.name == 'welcome-room':
        print(message.content)
        if message.content.lower() == 'done':
            await RemoveRole(member, role)

        await message.delete()
    await client.process_commands(message)

@client.event
async def on_ready():
    print('ArmBot is ready.')
    await client.change_presence(status = discord.Status.online, activity = discord.Game('ArmBot'))

@client.event
async def on_member_join(member):

    print(f'{member} has joined the server')
    role = discord.utils.get(member.guild.roles, name = 'member')
    
    await member.add_roles(role)

@client.event
async def on_member_remove(member):
    
    print(f'{member} has left the server')

@client.event
async def on_raw_reaction_add(payload):
    
    #gets the guild the reaction occured in
    
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

    #gets the member that reacted
    
    member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)

    #gets the 'btec' role from the guild's roles
    
    role = discord.utils.find(lambda g : g.name == 'btec', guild.roles)

    #checks to see if the reaction's owner doesn't have the btec role
    
    if role not in member.roles:
        
        #takes the unicode value and converts it to words and then chooses element[1]
        
        char = payload.emoji.name
        name = unicodedata.name(char[0])
        name = name.split(' ')[1].lower()
        print(name)

        #checks what the string name is of the reaction

        
        if name == 'one':
            
            role = discord.utils.get(guild.roles, name = 'further-maths')
            await Role(member, role, guild)
            
        elif name == 'two':
            
            role = discord.utils.get(guild.roles, name = 'maths')
            await Role(member, role, guild)
            
        elif name == 'three':
            
            role = discord.utils.get(guild.roles, name = 'physics')
            await Role(member, role, guild)
            
        elif name == 'four':
            
            role = discord.utils.get(guild.roles, name = 'computer-science')
            await Role(member, role, guild)
            
        elif name == 'five':
            
            role = discord.utils.get(guild.roles, name = 'chemistry')
            await Role(member, role, guild)
            
        elif name == 'six':
            
            role = discord.utils.get(guild.roles, name = 'biology')
            await Role(member, role, guild)
            
        elif name == 'seven':
            
            role = discord.utils.get(guild.roles, name = 'accounting')
            await Role(member, role, guild)
            
        elif name == 'book':
            
            role = discord.utils.get(guild.roles, name = 'a-level')
            await Role(member, role, guild)
            
        elif name == 'palette':

            role = discord.utils.find(lambda g : g.name == 'a-level', guild.roles)
                
            if role not in member.roles:
                print('yes')
                role = discord.utils.get(guild.roles, name = 'btec')
                await Role(member, role, guild)
            else:
                return await member.send(member.mention + ' you can\'t take a-level with btec')

@client.command()
async def Role(member, role, guild):
    if role is not None:

            print(member.roles)
            
            if member is not None:
                
                await member.add_roles(role)

                await member.send(f'Added {role} to your roles in {guild.name}')

@client.command()
@commands.has_permissions(administrator = True)
async def RemoveRole(member, role):
    print(member.roles)
    if member is not None:
        await member.remove_roles(role)
        print(f'Removed {role} from {member}\'s roles')

@client.event
async def on_raw_reaction_remove(payload):
    
    #takes the unicode value and converts it to words and then chooses element[1]
    
    char = payload.emoji.name
    name = unicodedata.name(char[0])
    name = name.split(' ')[1].lower()
    
    #gets the guild the reaction occured in
    
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

    #checks what the string name is of the reaction
        

    #checks what the name of the reaction is and converts it to the corresponding role
    
    if name == 'one':
        
        #finds the role which corresponds to the reaction
        
        role = discord.utils.get(guild.roles, name = 'further-maths')
        
    elif name == 'two':
        
        role = discord.utils.get(guild.roles, name = 'maths')
        
    elif name == 'three':
        
        role = discord.utils.get(guild.roles, name = 'physics')
        
    elif name == 'four':
        
        role = discord.utils.get(guild.roles, name = 'computer-science')
        
    elif name == 'five':
        
        role = discord.utils.get(guild.roles, name = 'chemistry')
        
    elif name == 'six':
        
        role = discord.utils.get(guild.roles, name = 'biology')
        
    elif name == 'seven':
        
        role = discord.utils.get(guild.roles, name = 'accounting')
        
    elif name == 'palette':
        
        role = discord.utils.get(guild.roles, name = 'btec')
        
    elif name == 'book':

        role = discord.utils.get(guild.roles, name = 'a-level')
        
    if role is not None:
        
        #gets the member that reacted
        
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            
        if member is not None:
            
            await member.remove_roles(role)
            await member.send(f'Removed {role} from your roles in {guild.name}')

@client.command()
@commands.has_permissions(administrator = True)
async def Reset(ctx):
    
    #resets the bot
    
    await ctx.channel.send('Resetting')
    await client.close()
    await client.login('NjgyOTk1MzMyODE2MDQ0MTEz.Xlv3wA.fHumvXi1XdP_sshfrtd6fUQKkpw')

@client.command(aliases = ['help'])
async def Help(ctx):
    
    #DMs author of message with list of commands
    
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.blue()
    )

    embed.set_author(name = 'Help')
    embed.add_field(name = '.8ball (question)', value = 'Fortune teller', inline = False)
    embed.add_field(name = '.kick', value = 'Kicks member', inline = False)
    embed.add_field(name = '.ban', value = 'Bans member', inline = False)
    embed.add_field(name = '.unban', value = 'Unbans a member', inline = False)
    embed.add_field(name = '.join', value = 'Joins your voice channel', inline = False)
    embed.add_field(name = '.leave', value = 'Leaves your voice channel', inline = False)
    embed.add_field(name = '.play', value = 'Plays a song in your channel', inline = False)

    await ctx.author.send(f'{author.name}, you called for the cavalry!', embed = embed)
    await ctx.send(author.mention + ' your message was sent to your DMs!')

@client.command(aliases = ['8ball', '8Ball'])
async def _8Ball(ctx, *, question):

    #awaits a question and then sends a random choice of preset answers
    
    await ctx.send(f'Question: {question}\n{random.choice(eightBallResponses)}')

@client.command(aliases = ['kick'])
@commands.has_permissions(administrator = True)
async def Kick(ctx, member : discord.Member, *, reason = None):

    #kicks a member with an option of adding a reason
    
    await member.kick(reason = reason)
    
@client.command(aliases = ['ban'])
@commands.has_permissions(administrator = True)
async def Ban(ctx, member : discord.Member, *, reason = None):

    #bans a member with an option of adding a reason
    
    await member.ban(reason = reason)

@client.command(aliases = ['unban'])
@commands.has_permissions(administrator = True)
async def Unban(ctx, *, member):

    #unbans a ex-member
    
    banned_users = await ctx.guild.bans()
    member_name , member_discriminator = member.split('#')

    for banned in banned_users:
        
        user = banned.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            
            await ctx.guild.unban(user)
            await ctx.send(f'{user} has been unbanned. He may now rejoin')

@client.command(aliases = ['join'])
async def Join(ctx):

    #bot joins voice channel

    voice_client = ctx.author.guild.voice_client
    
    if voice_client in client.voice_clients:
        
            await ctx.send(f'{ctx.author.mention} I\'m in your voice channel!')
    try:
        
        channel = ctx.message.author.voice.channel
        await channel.connect()
        
    except AttributeError:
        
        if voice_client in client.voice_clients:
            
            await ctx.send('I\'m in your voice channel!')
            
        await ctx.send('You are not in an accessible voice channel!')

@client.command(aliases = ['leave'])
async def Leave(ctx):
    #bot leaves voice channel
    
    voice_client = ctx.author.guild.voice_client
    
    if voice_client in client.voice_clients:
        
        await voice_client.disconnect()
        
    else:
        
        await ctx.send('I\'m not in a voice channel!')

@client.command(aliases = ['play'])
async def Play(ctx, *, url):

    #bot links a youtube song into the channel that the message was sent from
    
    guild = ctx.message.guild
    voice_client = guild.voice_client
    
    player = await voice_client.create_ytdl_player(url)
    players[guild.id] = player
    
    player.start()
    
###############################################

#checks what subject they want

@client.command(aliases = ['resource'])
async def Resource(ctx, *, subject):
    
    author = ctx.message.author
    
    if (subject == Subject.Maths.name):
        await ctx.send(author.mention + f' you have chosen {Subject.Maths.name}. Please now use the .Maths (topic name)'
                        + f' to access the topics of {subject}')
        await ctx.channel.send('**List of Topics:\nAlgebraic Expressions\nQuadratics\nEquations and Inequalities\n'
                        +'Graphs and Transformations\nStraight Line Graphs\nCircles\nAlgebraic Methods\n'
                        + 'Binomial Expansion\nTrigonometric Ratios\nTrigonometric Identities'
                        + 'Vectors\nDifferentiation\nIntegration\nExponentials and Logarithms**')
    elif (subject == Subject.ComputerScience.name):
        await ctx.send(author.mention + f' you have chosen {Subject.ComputerScience.name}. Please now use the .CS (topic name)'
                        + f' to access the topic of {subject}')

#list of subjects currently supported

@client.command(aliases = ['maths'])
async def Maths(ctx, *, topicName):
    
    author = ctx.message.author
    counter = 0

    if topicName in topicList:
        for topic in topicList:
            if topicName == topic:
                await UploadFile(ctx, topicList[counter] + scraper.fileType)
            else:
                counter += 1
    
    #await ctx.send(author.mention + ' ' + TopicChecker(topicName, counter))
    else:
        await ctx.send(author.mention + f' {topicName} is not a topic of Maths!')

@client.command(aliases = ['furthermaths', 'further-maths', 'Furthermaths'])
async def FutherMaths(ctx, *, topicName):
    
    author = ctx.message.author
    counter = 0
    
    if (topicName[0] == 'F'):


        await ctx.send(author.mention + ' we do not currently support this subject')
        #await ctx.send(author.mention + ' ' + TopicChecker(topicName, counter))
    else:
        
        await ctx.send(author.mention + f' {topicName} is not a topic of Further Maths!')

@client.command(aliases = ['cs', 'CS', 'Computer Science'])
async def ComputerScience(ctx, *, topicName):
    
    author = ctx.message.author
    counter = 0
    
    if (topicName[0] == 'C'):
        await ctx.send(author.mention + ' we do not currently support this subject')
        #await ctx.send(author.mention + ' ' + TopicChecker(topicName, counter))
    else:
        
        await ctx.send(author.mention + f' {topicName} is not a topic of Computer Science!')

@client.command()
async def Quit(ctx):
    
    await client.close()

client.run('NjgyOTk1MzMyODE2MDQ0MTEz.Xlv3wA.fHumvXi1XdP_sshfrtd6fUQKkpw')
