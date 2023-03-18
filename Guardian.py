import discord, time
from lib.config import *
from discord.ext import commands, tasks

#------------Variables 
client_info = give_config()['client2']
PREFIX = client_info['bot-prefix']
TOKEN = client_info['bot-token']


#----------------Making Client

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=PREFIX, intents=intents)
client.remove_command('help')


#-------------------Events
@client.event
async def on_ready():
    print('Bot has connected!')

@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(1018134189373136939)
    #Colour roles-------------------------------------
    if int(payload.channel_id) == 1018400549458169876:
        pass

@client.event
async def on_voice_state_update(member, before, after):
    member_list = []
    bot_list = []
    text_channel = client.get_channel(1018134189373136939)
    if before.channel == None: 
        
        if int(after.channel.id) == 1018477653440864296:
            
            if not is_private_user_exists(member.id):
                for guild in client.guilds:
                    for category in guild.categories:
                        if int(category.id) == 1018477346996617267:
                            
                            channel = await guild.create_voice_channel(str(member.name)+"'s Voice", category = category)
            
                            await member.move_to(channel)
                            make_private_user(member.id, channel.id)
            else:
                for guild in client.guilds:
                    for category in guild.categories:
                        if int(category.id) == 1018477346996617267:
                            count = change_private_user_count(member.id)
                            channel = await guild.create_voice_channel(str(member.name)+f"'s Voice {count}", category = category)
                            await member.move_to(channel)
                            change_private_user_channels(member.id, channel.id)
                            

                    
    if after.channel == None:
        del_channel_id = int(before.channel.id)
        if is_private_channel_exist(del_channel_id):

            del_channel = client.get_channel(del_channel_id)
            for check in del_channel.members:
                if check.bot:
                    bot_list.append(check.name)
                else: 
                    member_list.append(check.name)
            
            if not member_list and not bot_list:
                await del_channel.delete()
                del_private_info(member.id ,del_channel_id)

            if not member_list and bot_list:
                await del_channel.delete()
                del_private_info(member.id ,del_channel_id)
    if before.channel and after.channel:
        
        if int(before.channel.id) != int(after.channel.id):
            if int(after.channel.id) == 1018477653440864296:
                if not is_private_user_exists(member.id):
                    for guild in client.guilds:
                        for category in guild.categories:
                            if int(category.id) == 1018477346996617267:
                                channel = await guild.create_voice_channel(str(member.name)+"'s Voice", category = category)
                
                                await member.move_to(channel)
                                make_private_user(member.id, channel.id)
                else:
                    for guild in client.guilds:
                        for category in guild.categories:
                            if int(category.id) == 1018477346996617267:
                                count = change_private_user_count(member.id)
                                channel = await guild.create_voice_channel(str(member.name)+f"'s Voice {count}", category = category)
                                await member.move_to(channel)
                                change_private_user_channels(member.id, channel.id)
            del_channel_id = int(before.channel.id)
            if is_private_channel_exist(del_channel_id):        
                if int(before.channel.id) == del_channel_id:

                    del_channel = client.get_channel(del_channel_id)
                    for check in del_channel.members:
                        if check.bot:
                            bot_list.append(check.name)
                        else: 
                            member_list.append(check.name)
                    
                    if not member_list and not bot_list:
                        await del_channel.delete()
                        del_private_info(member.id, del_channel_id)

                    if not member_list and bot_list:
                        await del_channel.delete()
                        del_private_info(member.id, del_channel_id)



    
        

@client.event
async def on_message(message):
    channel = client.get_channel(1018134189373136939)
    if not message.author.bot:
        point_amount = len(message.content)
        save_chat_points(message.author.id, int(point_amount))
        

client.run(TOKEN)
