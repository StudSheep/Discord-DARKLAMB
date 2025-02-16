import discord, os
from json import loads as JSONDecode
from json import dumps as JSONEncode
from time import time

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
client = discord.client.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

def ReadFile(path,obj):
    file = open(path, "r")
    content = file.read()
    if content == '':
        content = {}
    else:
        content = JSONDecode(content)
    if obj:
        content = content[obj]
    file.close()
    return content

def WriteFile(path,content):
    file = open(path, "w")
    file.write(JSONEncode(content))
    file.close()
    return content

def ModifyFile(path,obj,val):
    file = open(path, "w+")
    content = file.read()
    if content == '':
        content = {}
    else:
        content = JSONDecode(content)
    content[obj] = val
    file.write(JSONEncode(content))
    file.close()
    return content

@tree.command(
    name="daily",
    description="Claim your daily reward"
)
async def daily_command(interaction):
    path = 'userdata/'+interaction.user_id
    current = int(time())
    if (ReadFile(path,'daily_time') or 0) > current+(60*60*12):
        await interaction.response.send_message(f"Your daily will be available <t:{current+(60*60*12)}:R>",ephemeral=True)
        return
    streak = 1
    if (ReadFile(path,'daily_time') or 0) < current+(60*60*24):
        streak = ReadFile(path,'daily_streak')+1
    ModifyFile(path,'daily_streak',streak)
    ModifyFile(path,'daily_time',current)
    gold = ReadFile(path,'gold') or 0
    reward = 100+(min(streak,30)^2)
    gold += reward
    ModifyFile(path,'gold',gold)
    await interaction.response.send_message(f"You collected your {str(reward)} worth of daily gold!\n-# {str(streak)} daily streak")

@tree.command(
    name="balance",
    description="Flex yo money"
)
async def balance_command(interaction):
    path = 'userdata/'+interaction.user_id
    gold = ReadFile(path,'gold') or 0
    await interaction.response.send_message(f"You have {str(gold)} gold, epic flex!!")

@tree.command(
    name="duel",
    description="Ask to duel another user"
)
async def duel_command(interaction,member: discord.Member):
    if not interaction.channel:
        await interaction.response.send_message("**Cannot use this command in DMs**",ephemeral=True)
        return
    view = discord.ui.View(timeout=15)
    view.add_item()
    acceptButton = discord.ui.Button(ButtonStyle=discord.ButtonStyle.primary,label='ACCEPT')
    await interaction.response.send_message(interaction.user.mention+" challenged "+member.mention+" in a duel!",view=view)

@client.event
async def on_ready():
    print("ON READY")
    await tree.sync()
    print("TREE SYNC")

@client.event
async def on_guild_join(guild):
    print('GUILD JOINED: '+guild.name)

token = input('BOT TOKEN >> ')
client.run(token)