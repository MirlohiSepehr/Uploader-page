import time, json 
from datetime import datetime
from includes.Modules import *


    
def give_config():
    with open('config/config.json', 'r') as member_list:
        config_list = json.load(member_list)
        return config_list
def is_member_exists(name):
    with open('database/member-info.json', 'r') as member_list:
        main_list = json.load(member_list)
        for member in main_list:
            if int(member['name']) == int(name):
                return True

def save_member(member):
    with open('database/member-info.json', 'r') as member_list:
        main_list = json.load(member_list)
        main_list.append(member)
        with open('database/member-info.json', 'w') as member_list_change:
            json.dump(main_list, member_list_change)

            member_list_change.close()

        member_list.close()

def save_time(name): 
    with open('database/member-info.json', 'r') as file: 
        file_to_read = json.load(file)
        for member in file_to_read: 
            if member['name'] == name: 
                member['voice-timer'] = time.time()
                with open('database/member-info.json', 'w') as file2: 
                    json.dump(file_to_read, file2)

                    file2.close()
        
        file.close()

def calculate_time(name): 
    current_time = time.time()
    with open('database/member-info.json', 'r') as file: 
        file_to_read = json.load(file)
        for member in file_to_read: 
            if member['name'] == int(name):
                if member['voice-timer'] != 0:
                    cal = (current_time - int(member['voice-timer'])) / 30
                    balance = 0
                    if member['boost']:
                        balance = cal * 15
                    else:
                        balance = cal * 7
                    new_balance = int(member['xp']) + balance
                    member['xp'] = int(new_balance)
                    with open('database/member-info.json', 'w') as file2: 
                        json.dump(file_to_read, file2)

                        file2.close()
        file.close()

def still_on_voice_channel(name):
    current_time = time.time()
    with open('database/member-info.json', 'r') as file: 
        file_to_read = json.load(file)
        for find in file_to_read:
            if find['name'] == int(name):
                find['voice-timer'] = current_time
                find['xp'] = find['xp'] + 50
                with open('database/member-info.json', 'w') as file2: 
                    json.dump(file_to_read, file2)


                    file2.close()
        file.close()

def get_user_wallet(name):
    with open('database/member-info.json', 'r') as file: 
        file_to_read = json.load(file)
        for member in file_to_read:
            if member['name'] == int(name):
                return member['wallet']


def give_current_time(Hour = True, mint = False, sec = False):
    if Hour:
        Hour = "%H"
    else:
        Hour = ""
    if mint:
        mint = "%M"
    else: 
        mint = ""
    if sec: 
        sec = "%S"
    else: 
        sec = ""
    new = datetime.now()

    making_current_time = new.strftime(Hour+":"+mint+":"+sec)
    return making_current_time

def give_default_roles():
    with open('config/config.json', 'r') as file: 
        file_to_read = json.load(file)
        Server = file_to_read['Server']
        return Server['default-roles']

def save_chat_points(name, amount):
    with open('database/member-info.json', 'r') as file: 
        file_to_read = json.load(file)
        for member in file_to_read:
            if member['name'] == int(name):
                member['xp'] = int(amount) * 2
                with open('database/member-info.json', 'w') as file2: 
                    json.dump(file_to_read, file2)
def remove_default_role(role):
    counter = 0
    with open('config/config.json', 'r') as file: 
        file_to_read = json.load(file)
        Server = file_to_read['Server'] 
        for rolename in Server['default-roles']:
            if int(rolename) == int(role):
                del Server['default-roles'][counter]
            else:
                counter =+ 1
        with open('config/config.json', 'w') as file2: 
            json.dump(file_to_read, file2)


def add_default_role(role): 
    with open('config/config.json', 'r') as file: 
        file_to_read = json.load(file)
        Server = file_to_read['Server']
        Server['default-roles'].append(role)
        with open('config/config.json', 'w') as file2: 
                    json.dump(file_to_read, file2)
            
def is_default_role_exists(role):
    with open('config/config.json', 'r') as file: 
        file_to_read = json.load(file)
        Server = file_to_read['Server']
        for rolename in Server['default-roles']:
            if int(role) == int(rolename):
                return True               

def is_default_role_banned(role):
    with open('config/config.json', 'r') as file: 
        file_to_read = json.load(file)
        Server = file_to_read['Server']
        for rolename in Server['not-default']:
            if int(role) == int(rolename):
                return True
def calculate_points(name, points):
    pass

def make_private_user(name, channel_ID):
    with open('database/private_voice.json', 'r') as file: 
        file_to_read = json.load(file)
        for member in file_to_read:
            if int(name) == member['name']:
                return False
                break
        payload = {"name": int(name), "channel_ID": [int(channel_ID)], "channel_count": 1}
        file_to_read.append(payload)
        with open('database/private_voice.json', 'w') as file2: 
            json.dump(file_to_read, file2)

def change_private_user_count(name):
    count = 0
    with open('database/private_voice.json', 'r') as file: 
        file_to_read = json.load(file)
        for member in file_to_read:
            if int(name) == member['name']:
                member['channel_count'] = int(member['channel_count']) + 1
                count = member['channel_count']
        with open('database/private_voice.json', 'w') as file2: 
            json.dump(file_to_read, file2)

    return count;

def change_private_user_channels(name, channel):
    with open('database/private_voice.json', 'r') as file: 
        file_to_read = json.load(file)
        for member in file_to_read:
            if int(name) == member['name']:
                member['channel_ID'].append(channel)
        with open('database/private_voice.json', 'w') as file2: 
            json.dump(file_to_read, file2)


        
def is_private_user_exists(name):
    with open('database/private_voice.json', 'r') as file: 
        file_to_read = json.load(file)
        for member in file_to_read:
            if int(member['name']) == int(name):
                return True

def give_private_info(name):
    with open('database/private_voice.json', 'r') as file: 
        file_to_read = json.load(file)
        for member in file_to_read:
            if int(member['name']) == int(name):
                return member

def del_private_info(name, channel):
    counter = 0
    counter2 = 0
    with open('database/private_voice.json', 'r') as file: 
        file_to_read = json.load(file)
        for member in file_to_read:
            for channel_name in member['channel_ID']:
                if int(channel_name) == int(channel):
            
                    if len(member['channel_ID']) == 1:
                        del file_to_read[counter]
                    else: 
                        for channels in member['channel_ID']:
                            if int(channels) == int(channel):
                                del member['channel_ID'][counter2]
                            else:
                                counter2 =+ 1
                
            counter =+ 1 
                
        with open('database/private_voice.json', 'w') as file2:
            json.dump(file_to_read, file2)

def is_private_channel_exist(channel):
    with open('database/private_voice.json', 'r') as file: 
        file_to_read = json.load(file)
        for info in file_to_read:
            for channels in info['channel_ID']:
                if int(channels) == int(channel):
                    return True
            
        
def get_user_profile_url(name):
    with open('database/member-info.json', 'r') as file: 
        file_to_read = json.load(file)
        for member in file_to_read:
            if member['name'] == int(name):
                return str(member['avatar'])

def get_user_level(name):
    with open('database/member-info.json', 'r') as file: 
        file_to_read = json.load(file)
        for member in file_to_read:
            if member['name'] == int(name):
                return str(member['level'])

def get_default_roles():
  
    with open('config/config.json', 'r') as file:
        file_to_read = json.load(file)
        return file_to_read['Server']['default-roles']

def check_xp_for_lvl(name, defaultPoints):
    with open("database/member-info.json", 'r') as file:
        file_to_read = json.load(file)
        for member in file_to_read:
            if member['name'] == int(name):
                current_xp = member['xp']
                if int(current_xp) > int(defaultPoints):

                    if int(member['level']) == 0:
                        member['xp'] = int(current_xp) - int(defaultPoints)
                        member['level'] = int(member['level']) + 1
                    else:
                        must_add = 100 * int(member['level'])
                        must_min = must_add + int(defaultPoints)
                        member['xp'] = int(current_xp) - must_min
                        member['level'] = int(member['level']) + 1

def calculate_voice_xp(name):
    with open("database/member-info.json", 'r') as file:
        file_to_read = json.load(file)
        for member in file_to_read:
            if member['name'] == int(name):
                curre

# def get_current_status():
#     with open("database/member-info.json", "r") as file:
#         file_to_read = json.load(file)
        