import discord
from discord.ext import commands
import random
import os
from xml.dom import minidom
#import lxml
#from lxml import etree
BOT_PREFIX = ("~","/")
bot = commands.Bot(command_prefix=BOT_PREFIX, description='A bot that greets the user back.',case_insensitive=True)

xmlDoc = minidom.parse('db.xml')
corexml = minidom.parse('core.xml')
spellxml = corexml.getElementsByTagName("spell")
debug = False


messagei = None
rinit = 0
#db = etree.parse("db.xml")



def internal_roll(*argst):
    total = 0
    argsl = list(argst)
    rolls = ''.join(argsl)
    rollsl = rolls.split('+')
    if debug == True:
        print(rollsl)
    for x in rollsl:
        if "d" in x:
            subtotal = 0
            rollslx = x.split("d")
            if rollslx[0] == "":
                rollslx[0] = "1"
            if debug == True:
                print(rollslx)
            for x in range(int(rollslx[0])):
                roll = random.randint(1,int(rollslx[1]))
                subtotal += roll
            if debug == True:
                print(subtotal)
            total += subtotal
        else:
            total += int(x)
            if debug == True:
                print(int(x))
    if debug == True:
        print(total)
    return total



@bot.event
async def on_message(message):
    message.content = message.content.lower()
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
 #   await bot.change_presence('Type /help for help')
 #   await bot.change_presence(game=discord.Game(name='Type /help for help'))    
 #   await bot.change_status(game=discord.Game(name = "Type /help for help"))

@bot.event
async def wait_until_login():
    await bot.change_presence(game=discord.Game(name='Type /help for help'))
        
@bot.command(name="init",pass_context=True,aliases=['i'])
async def init(ctx, namel="xml", *argst):
    try:
        if debug == True:
            print(argst)
        '''
        try:
            mod = int(argst[-1])
            del argst[-1]
        except:
            mod = 0
            '''
        if debug == True:
            print(argst)
        #print(mod)
        argsl = list(argst)
        argsl.insert(0,namel)
        if debug == True:
            print(argsl)
        try:
            mod = int(argsl[-1])
            del argsl[-1]
        except:
            mod = 0
            
        name = ' '.join(argsl)
        if debug == True:
            print(argsl)
            print(mod)
        global rinit
        global messagei
        if rinit == 1:
            if name == "xml":
                playerl = xmlDoc.getElementsByTagName("player")
                y = 0
                for x in playerl:
                    if x.getElementsByTagName("discordid")[0].childNodes[0].nodeValue == ctx.message.author.id:
                        if debug == True:
                            print("FOUND HIM")
                        mod = int(x.getElementsByTagName("init")[0].childNodes[0].nodeValue)
                        if debug == True:
                            print(mod)
                        name = str(x.getElementsByTagName("name")[0].childNodes[0].nodeValue)
                        init = random.randint(1,20)+mod
                        clientid = ctx.message.author.id
                        messagei = await bot.edit_message(messagei, messagei.content[:-3]+"\n<"+name+"> Rolled an init of "+str(init)+"```")
                    else:
                        y += 1
                if y == len(playerl):
                    await bot.say("Not found in database, use the command ~i [mod] [name]")
     #           mod = et.xpath("/db/player/
    #            init = random.randinit(1,20)
                #print("xml Here")
            else:
                init = random.randint(1,20)
                init = init+mod
                clientid = ctx.message.author.id
                messagei = await bot.edit_message(messagei, messagei.content[:-3]+"\n<"+name+"> Rolled an init of "+str(init)+"```")
        else:
            await bot.say("Init Rolling has not started yet")
    except:
        await bot.say("<@"+str(ctx.message.author.id)+"> entered an invalid expression.\nThe correct way to use this command is: ~init [name] [init mod]")
    
@bot.command(name="startinit",pass_context=True,aliases=['si'])
async def si(ctx):
    if debug == True:
        print("Stage1")
    global rinit
    if rinit == 0:
        if debug == True:
            print("stage2")
        global messagei
        messagei = await bot.send_message(ctx.message.channel, "```==========Init==========```")
        await bot.pin_message(messagei)
        rinit = 1
    else:
        await bot.say("Init recording has already begun.")

@bot.command(name="endinit",aliases=['ei'])
async def endinit():
    global rinit
    if rinit == 1:
        rinit = 0
        await bot.say("Init recording has stoped")
    else:
        await bot.say("Init recording is not started.")

@bot.command(name="showinit",aliases=['showi'])
async def showinit():
    global messagei
    await bot.say(messagei.content)

@bot.command(name="roll",pass_context=True,aliases=['r'])
async def roll(ctx, *argst):
    try:
        breakdown = ""
        total = 0
        argsl = list(argst)
        rolls = ''.join(argsl)
        rollsl = rolls.split('+')
        if debug == True:
            print(rollsl)
        for x in rollsl:
            if "d" in x:
                subtotal = 0
                #breakdown += "("
                rollslx = x.split("d")
                if rollslx[0] == "":
                    rollslx[0] = "1"
                if debug == True:
                    print(rollslx)
                for x in range(int(rollslx[0])):
                    roll = random.randint(1,int(rollslx[1]))
                    subtotal += roll
                    breakdown += str(roll)+" + "
                breakdown = breakdown[:-3]
                if debug == True:
                    print("code")
                #breakdown += ")+"
                if "+" in breakdown:
                    breakdown += " = "+str(subtotal)+",   "
                else:
                    breakdown += ",   "
                total += subtotal
            else:
                total += int(x)
                breakdown += str(x)+",   "
        if debug == True:        
            print(total)
        breakdown = breakdown[:-4]
        if "," in breakdown or "+" in breakdown:
            await bot.say("<@"+str(ctx.message.author.id)+"> Rolled a **"+str(total)+"**. ("+breakdown+")")
        else:
            await bot.say("<@"+str(ctx.message.author.id)+"> Rolled a **"+str(total)+"**.")
        if debug == True:
            print(breakdown)
        #await bot.say(breakdown)
    except:
        await bot.say("<@"+str(ctx.message.author.id)+"> specified an invalid dice expression.")

@bot.command(name="lightningbolt",pass_context=True,aliases=['lb'])
async def lightningbolt(ctx):
    hit = internal_roll("d20+5")
    if debug == True:
        print(hit)
    damage = internal_roll("8d6")
    if debug == True:
        print(damage)
    await bot.say("<@"+str(ctx.message.author.id)+"> Attacked with lightning bolt:\n"+str(hit)+" vs AC\n"+str(damage)+" Damage")


@bot.command(name="cast",pass_context=True,aliases=['c'])
async def cast(ctx, spell, *slott):
    try:
        slot = "min"
        '''
        try:
            mod = int(argst[-1])
            del argst[-1]
        except:
            mod = 0
            '''
        argst = slott
        if debug == True:
            print(argst)
        #print(mod)
        argsl = list(argst)
        argsl.insert(0,spell)
        if debug == True:
            print(argsl)
        try:
            slot = str(int(argsl[-1]))
            del argsl[-1]
        except:
            slot = "min"
            
        spell = ' '.join(argsl)
        if debug == True:
            print(spell)
            print(slot)
        y = 0
        for x in spellxml:
            if x.getElementsByTagName("name")[0].childNodes[0].nodeValue.lower() == spell.lower():
                level = x.getElementsByTagName("level")[0].childNodes[0].nodeValue
                hit = internal_roll("d20")
                try:
                    damage = internal_roll(x.getElementsByTagName("roll")[0].childNodes[0].nodeValue)
                except:
                    damage = "N/A"
                clientid = ctx.message.author.id
                if not damage == "N/A":
                    await bot.say("<@"+str(ctx.message.author.id)+"> Attacked with "+spell+":\n"+str(hit)+" vs AC\n"+str(damage)+" Damage")
                else:
                    await bot.say("<@"+str(ctx.message.author.id)+"> Used "+spell+":\n"+str(hit)+" vs DC")
                break
            else:
                y += 1
        if y == len(spellxml):
            await bot.say("Spell not found in database")
        if debug == True:
            print(spell)
            print(slot)
    except:
        await bot.say("<@"+str(ctx.message.author.id)+"> entered an invalid expression.\nThe correct way to use this command is: ~cast [spell name] [spell slot]")

       
@bot.command(name="spellinfo",pass_context=True,aliases=['sinfo'])
async def spellinfo(ctx, *spell):
    argst = spell
    del spell
    if debug == True:
        print(argst)
    #print(mod)
    argsl = list(argst)
    spell = ' '.join(argsl)
    
    cID = ctx.message.author
    y = 0
    final = "```==========Spell Info========="
    first = 1
    for x in spellxml:
        if x.getElementsByTagName("name")[0].childNodes[0].nodeValue.lower() == spell.lower():
            #print(x.childNodes)
            for z in x.childNodes:
                #print(z.nodeType)
                
                if z.nodeType == 1:
                    if not z.nodeName == "#text":
                        #print(z)
                        #print(z.nodeName)
                        try:
                            if not z.nodeName == "text":
                                final += "\n"+str(z.nodeName)+": "+str(z.childNodes[0].nodeValue)
                                #print(z.childNodes[0].nodeValue)
      #                          await bot.send_message(cID, z.nodeName+": "+z.childNodes[0].nodeValue)
                            else:
                                if first == 1:
                                    final += "\n"
                                    first = 0
                                final += "\n"+str(z.childNodes[0].nodeValue)
                        except:
                            final += "\n"
                            #print(" ")
 #                           await bot.send_message(cID, "text: ")
            #for z in x.getElements:
#                await bot.send_message(cID, z.nodeName+": "+str(z.childNodes[0].nodeValue))
            '''
            await bot.send_message(cID, "Level: " +
            await bot.send_message(cID, "School: " +
            await bot.send_message(cID, "Ritual: "
            
            if not damage == "N/A":
                await bot.say("<@"+str(ctx.message.author.id)+"> Attacked with "+spell+":\n"+str(hit)+" vs AC\n"+str(damage)+" Damage")
            else:
                await bot.say("<@"+str(ctx.message.author.id)+"> Used "+spell+":\n"+str(hit)+" vs DC")
            break
        '''
            final += "```"
            if debug == True:
                print(final)
            await bot.send_message(cID, final)
            break
        else:
            y += 1
    if y == len(spellxml):
        await bot.say("Spell not found in database")
    if debug == True:
        print(spell)
    #print(slot)
   
    #await bot.send_message(ctx.message.author, "Spell info")

'''
@bot.command()
async def chaosbolt():
'''    
        
bot.run("NDM4MTM5ODUwNTQ2MjE2OTcx.DcARFA.2SYJJFyqMhTTsU6D9aXPqXDmRbQ")
