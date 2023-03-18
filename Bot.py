import discord, time
from lib.config import *
from discord.ext import commands, tasks
from discord.ui import Button, View

#--------------------Variables---------------------
client_info = give_config()['client']
TOKEN = client_info['bot-token']
PREFIX = client_info['bot-prefix']
currently_on_voice = []
default_roles_list = give_default_roles()
#--------------------------------
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=PREFIX, intents=intents)
client.remove_command('help')
#-----------------------------Events
@client.event
async def on_member_join(member):
    channel = client.get_channel(1018134189373136939)
    if not member.bot: 
        for guild in client.guilds:
            for role in guild.roles:
                for d_role in default_roles_list:
                    if role.id == d_role:
                        await member.add_roles(role)
                

@client.event
async def on_ready():
    refresh_member_list.start()
    print(f'Logged in as: {client.user.name}')
    print(f'With ID: {client.user.id}')


    for guild in client.guilds: 
        for channel in guild.channels:
            check_channel = channel.voice_channels
            for voice_ch in check_channel:
                channel_id = voice_ch.id
                make_channel = client.get_channel(int(channel_id))
                if make_channel.members:
                    for member in make_channel.members:
                        if not member.bot:
                            still_on_voice_channel(int(member.id))


@client.event
async def on_voice_state_update(member, before, after):
    if after.channel == None:
        calculate_time(member.id)
    if before.channel == None:
        save_time(member.id)
#-----------------------------Tasks


@tasks.loop(seconds=60)
async def refresh_member_list():
    

    for guild in client.guilds:
        for member in guild.members:
            if not member.bot:
                if not is_member_exists(member.id):
                    payload = {"name" : member.id, "avatar": str(member.avatar),"wallet": 0, "level": 0,"boost": False, "voice-timer": 0, "xp": 0, "premium": False, "premium-date": 0, }
                    resulte = save_member(payload)
                    print(resulte)

#---------------------------Commands
@client.command()
async def AtaNoobe(ctx): 
    await ctx.send('Malume ke hast!')

@client.command()
async def test(ctx):
    await ctx.send('Send something: ')
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel 
        

    msg = await client.wait_for("message", check= check, timeout = 20)

    if msg.content:
        await ctx.send(msg.content)
            
        
#-----------------Main Commands------------------
@client.command()
async def clear(ctx, amount : int): 
    await ctx.channel.purge(limit=amount+1)
    embed= discord.Embed(title='', description='', color=discord.Color.from_rgb(231,225,212))
    embed.add_field(name="**Clear Warn**", value=f"**{str(amount)}** was amount of cleaning!")
    await ctx.send(embed=embed)
    time.sleep(2)
    await ctx.channel.purge(limit=1)

@client.command()
async def myWallet(ctx):
    current_wallet = get_user_wallet(ctx.author.id)
    embed = discord.Embed(title= "", description= "Time: **"+give_current_time(True, True, True)+"**", color= discord.Color.from_rgb(231,225,212))
    embed.add_field(name="**Current Wallet:**", value="Your current wallet is: **"+ str(current_wallet)+"** MP")
    await ctx.send(embed = embed)

@client.command()
async def Role(ctx):

    #------------------------------- Buttons Section
    add_role_key = Button(label="Add", style=discord.ButtonStyle.green)
    role_list_key = Button(label="Default roles List", style=discord.ButtonStyle.green)
    remove_role_key = Button(label="Remove", style=discord.ButtonStyle.red)
    guide_role_key = Button(label="Guideline", style=discord.ButtonStyle.grey)
    #------------------------------- Embed section
    embed = discord.Embed(title="", description= "Time: **"+give_current_time(True, True, True)+"**", color=discord.Color.from_rgb(231,225,212))
    embed.add_field(name="**Role Editor**", value="Please select the option you want to make the changes with")
    #---
    help_embed = discord.Embed(title="A short guide:", description="", color = discord.Color.from_rgb(231,225,212))
    help_embed.add_field(name="Add", value="You can use this one to append some role to default-roles list, this list will check and if someone trying to join our server will get this role automatically!", inline= True)
    help_embed.add_field(name="Remove", value="This one can remove a role from default-roles list!", inline = False)

    #-------------------------------- function and config section ---
    async def give_guide_page(interaction):
        await interaction.response.edit_message(view = None, embed = help_embed)

    async def give_add_page(interaction):

        alert_embed = discord.Embed(title="", description="Time: **"+give_current_time(True, True, True)+"**", color= discord.Color.from_rgb(231,225,212))
        alert_embed.add_field(name="Alert", value="Send the role name or role id you want to **add**: ")
        await interaction.response.edit_message(embed = alert_embed, view = None)
        def check(m: discord.Message):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        message = await client.wait_for("message", check = check, timeout = 20)
        if message.content:
            rolename = int(message.content)
            if type(rolename) is int:
                add_default_role(int(rolename))
                await ctx.send("The role has appended!")


    async def give_remove_field(interaction):
        alert_embed = discord.Embed(title="", description="Time: **"+give_current_time(True, True, True)+"**", color= discord.Color.from_rgb(231,225,212))
        alert_embed.add_field(name="Alert", value="Send the role name or role id you want to **remove**: ")
        await interaction.response.edit_message(view = None, embed = alert_embed)
        def check(m: discord.Message):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        message = await client.wait_for("message", check = check, timeout = 20)
        if message.content:
            rolename = int(message.content)
            if type(rolename) is int:
                remove_default_role(int(rolename))
                await ctx.send("The role has removed!")

    async def give_roles_list(interaction):
        counter = 1
        default_roles = get_default_roles()
        alert_embed = discord.Embed(title="", description= f"Time: **{give_current_time(True, True, True)}**", color = discord.Color.from_rgb(231,225,212))
        for role in default_roles:
            for guild in client.guilds:
                for role_name in guild.roles:
                    if role == role_name.id:
                        alert_embed.add_field(name=f"Number {counter}", value= role_name.name)
                        counter = counter + 1

        await interaction.response.edit_message(view = None, embed = alert_embed)
    #-------------------- Other workings ---
    add_role_key.callback = give_add_page
    remove_role_key.callback = give_remove_field
    guide_role_key.callback = give_guide_page
    role_list_key.callback = give_roles_list
    view = View(timeout= None)
    view.add_item(add_role_key)
    view.add_item(role_list_key)
    view.add_item(remove_role_key)
    view.add_item(guide_role_key)

    await ctx.send(embed = embed, view= view)

@client.command()
async def shop(ctx):
    embed = discord.Embed(title = "Shop", description = "", color= discord.Color.from_rgb(231,225,212))
    embed.add_field(name = "Forgive us!", value="This command is still in progress")

    await ctx.send(embed =embed)
@client.command()
async def profile(ctx):
    profile_embed = discord.Embed(title="Profile status:", description=f"Time:  **{give_current_time(True,True,True)}**", color= discord.Color.from_rgb(231,225,212))
    profile_embed.add_field(name="Your username:", value=f"{ctx.author.mention}", inline=True)
    profile_embed.add_field(name="Your current wallet:", value=f"{get_user_wallet(ctx.author.id)}", inline=False)
    profile_embed.add_field(name="Your current Level:", value=get_user_level(ctx.author.id), inline=True)
    profile_embed.set_image(url = get_user_profile_url(ctx.author.id))
    profile_embed.set_footer(text = "Marshmallow Moderation")

    await ctx.send(embed = profile_embed)


@client.command()
async def roles(ctx):
    if ctx.author.id == 767030513088331797:
        # file = discord.File('images/discord-colour-roles.gif')
        roles_menu = discord.Embed(title="Colour Menu", description="", color= discord.Color.from_rgb(0,51,102))
        roles_menu.add_field(name="Colours", value="Normal colour roles that everyone can achive it you can see the list and choose one of them by using this key!", inline=False)
        roles_menu.add_field(name="Premium Colours", value="if you have Premium you can have a spesific colour by using this key", inline=False)
        roles_menu.set_image(url="https://s2.uupload.ir/files/discord-colour-roles_v5l7.gif")

        await ctx.send(embed =roles_menu)
        colour_btn = Button(label = "Colours", style= discord.ButtonStyle.gray)
        spesific_btn = Button(label = "Spesific Colours", style= discord.ButtonStyle.gray)

        # Callback functions 
        async def colours_callback(interaction):
            pass


client.run(TOKEN)
