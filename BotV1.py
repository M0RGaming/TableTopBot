import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import random

Client = discord.Client()
client = Bot(command_prefix = "$")
prev = None
auth = "YES"
init = 0
messagei = None

@client.event
async def on_ready():
    print("Bot has started")

@client.event
async def on_message(message):
    #print(str(message.author.id)+ " : "+ str(message.content))
    if message.content == "test":
        await client.send_message(message.channel, "This is a test")
    if message.author.id == "161614687321063434":
        if "chaos bolt" in message.content.lower():
            #await client.send_message(message.channel, "<@204777316621090816> roll 2d8+1d6")
            await client.send_message(message.channel, "```html \n<%s> attacked with Chaos Bolt ```" % (message.author.name))
            hit = random.randint(20, 20)
            damage1 = random.randint(1,8)
            damage2 = random.randint(1,8)
            damage3 = random.randint(1,6)
            if hit == 20:
                await client.send_message(message.channel, "```css [CRIT] ```")
                await client.send_message(message.channel, "```html <%s vs AC><%s damage> ````" % (hit+5, (damage1+damage2+damage3)*2))
                await client.send_message(message.channel, "(%s+5 to hit, 2*(%s+%s+%s) for damage)" % (hit, damage1, damage2, damage3))
                embed = discord.Embed(title="M0RGaming Attacks with Chaos Bolt", description="\n"+str(hit+5)+"vs AC", color=0x542169)
                embed.add_field(name=str((damage1+damage2+damage3)*2)+" Damage", value="\nBreakdown Of Rolls", inline=False)
                embed.add_field(name=""+str(hit)+"+5 to hit", value="2*("+str(damage1)+"+"+str(damage2)+"+"+str(damage3)+") for damage", inline=False)
                await client.send_message(message.channel, embed=embed)
            else:
                await client.send_message(message.channel, "```html <%s vs AC><%s damage> ```" % (hit+5, damage1+damage2+damage3))
                await client.send_message(message.channel, "(%s+5 to hit, %s+%s+%s for damage)" % (hit, damage1, damage2, damage3))


    if "start init" in message.content.lower():
        global messagei
        messagei = await client.send_message(message.channel, "==========Init==========")
        init = 1
        print(messagei)
                            

    if message.content.startswith('<@'):
        #if init == 1:
        userID = message.author.name
        print(userID)
        if userID == "RPBot":
            if "rolled" in message.content:
                user = message.content[2:]
                print(user)
                loop = 1
                x=1
                while loop == 1:
                    x += 1
                    if user[x-1:x] == ">":
                        loop = 0
                user = user[:x-1]
                print(user)
                length = 2+9+len(user)
                roll = message.content[length:]
                print(roll)
                loop = 1
                x = 1
                while not roll[-1:] == ".":
                    roll = roll[:-1]
                roll = roll[:-1]
                roll = roll[2:-2]
                print(roll)

                
                
 #               await client.send_message(message.channel, "==========Init==========\n<@%s> - Init of ***%s***" % (user, roll))
                messagei = await client.edit_message(messagei, messagei.content+"\n<@%s> - Init of ***%s***" % (user, roll))

    return messagei
 #   prev = message.author.name

@client.command()
async def ping(*args):

	await client.say(":ping_pong: Pong!")
	await asyncio.sleep(3)
	await client.say(":warning: This bot was created by **Habchy#1665**, it seems that you have not modified it yet. Go edit the file and try it out!")
    
    
    
client.run("NDM3NDExNTY5NjAxNzQwODIx.Db2pRA.x4zQCJGcj7klEOcJeRRFxyyL7Rk")
