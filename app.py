import discord
import asyncio
from discord.ext import commands
import random
import os
from xml.dom import minidom
import pickle
#from git import Repo
#from github import Github

#import lxml
#from lxml import etree
BOT_PREFIX = ("~","/")
bot = commands.Bot(command_prefix=BOT_PREFIX, description='Your Typical DnD bot... except better.',case_insensitive=True)

xmlDoc = minidom.parse('db.xml')
corexml = minidom.parse('Core.xml')
spellxml = corexml.getElementsByTagName("spell")
debug = False


messagei = None
rinit = 0 #if were rolling init at this point
initl = [] #list of all init stuff
idnumber = 0 #id nubmer
#db = etree.parse("db.xml")



### IMPORTANT ###
#stored_info = [(serverID,[vars,(messagei,messagei),(rinit,rinit),(initl,initl),(idnumber,idnumber)],[init, (playerID, data), (playerID, data)]),(serverID,info)]
stored_info = []


            
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



async def my_background_task():
    await bot.wait_until_ready()
    counter = 0
 #   channel = discord.Object(id='161614687321063434')
    while not bot.is_closed:
        await asyncio.sleep(21600) # task runs every 6 hours
        global stored_info
        pickle.dump( stored_info, open( "save.p", "wb" ) )
        counter += 1
        #await bot.send_message(channel, counter)
        print("Saving")
        
        



@bot.event
async def on_message(message):
    x = 0
    for x in range(0, len(message.content)):
        if message.content[x-1:x] == " ":
            break
    if not x==len(message.content):
        x = x-1
        
    message.content = message.content[:x].lower() + message.content[x:]
    await bot.process_commands(message)

@bot.event
async def on_ready():
    global stored_info
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    if debug == True:
        print(stored_info)
    stored_info = pickle.load( open( "save.p", "rb" ) )
    if debug == True:
        print(stored_info)
 #   await bot.change_presence('Type /help for help')
 #   await bot.change_presence(game=discord.Game(name='Type /help for help'))    
 #   await bot.change_status(game=discord.Game(name = "Type /help for help"))

@bot.event
async def wait_until_login():
    await bot.change_presence(game=discord.Game(name='Type /help for help'))
        

@bot.command(name="init",pass_context=True,aliases=['i'])
async def init(ctx, name="xml", *mod):
    
    namel = name
    del name
    argst = mod
    del mod
    argsl = list(argst)
    argsl.insert(0,namel)
    try:
        mod = int(argsl[-1])
        del argsl[-1]
    except:
        mod = 0
    name = ' '.join(argsl)
    
    global stored_info
    sID = ctx.message.server
    auth = ctx.message.author.id
    index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
    if not index == "":
        index = int(index)
        
        rinit = stored_info[index][1][1]
        messagei = stored_info[index][1][0]
        initl = stored_info[index][1][2]
        idnumber = stored_info[index][1][3]
        initdb = stored_info[index][2]
    
        if rinit == 1:
            if name == "xml":

                y = str([i2 for i2, v2 in enumerate(stored_info[index][2]) if v2[0] == auth])[1:-1]
                if not y == "":
                    idnumber += 1
                    y = int(y)
                    mod = stored_info[index][2][y][1][1]
                    name = stored_info[index][2][y][1][0]
                    
                    init = random.randint(1,20)+mod                    
                    initl.append((name,init,idnumber))
                    initl.sort(key=lambda tup: tup[1], reverse=True)
                    clientid = ctx.message.author.id
                    changedmsg = "```==========Init=========="
                    for x in range(0, len(initl)):
                        a,b,c = initl[x]
                        changedmsg += "\n<"+str(a)+"> Rolled an init of "+str(b)+". (id = "+str(c)+")"
                    changedmsg += "```"
                    messagei = await bot.edit_message(messagei, changedmsg)
                else:
                    await bot.say("You are not yet registered")                    
            else:
                idnumber = idnumber+1
                init = random.randint(1,20)
                init = init+mod
                initl.append((name,init,idnumber))
                initl.sort(key=lambda tup: tup[1], reverse=True)
                clientid = ctx.message.author.id
                changedmsg = "```==========Init=========="
                for x in range(0, len(initl)):
                    a,b,c = initl[x]
                    changedmsg += "\n<"+str(a)+"> Rolled an init of "+str(b)+". (id = "+str(c)+")"
                changedmsg += "```"
                messagei = await bot.edit_message(messagei, changedmsg)            
        else:
            await bot.say("Init Rolling has not started yet")

        stored_info[index][1][1] = rinit
        stored_info[index][1][0] = messagei
        stored_info[index][1][2] = initl
        stored_info[index][1][3] = idnumber

    
@bot.command(name="deleteinit",pass_context=True,aliases=['di'])
async def deleteinit(ctx, id):
    global stored_info
    #print(stored_info)
    sID = ctx.message.server
    auth = ctx.message.author.id
    index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
    if not index == "":
        index = int(index)
        messagei = stored_info[index][1][0]
        initl = stored_info[index][1][2]
        #print(initl)
        
        y = str([i2 for i2, v2 in enumerate(stored_info[index][1][2]) if str(v2[2]) == str(id)])[1:-1]
        if not y == "":
            y = int(y)
            initl.remove(initl[y])
            #print(initl)
            changedmsg = "```==========Init=========="
            for x in range(0, len(initl)):
                a,b,c = initl[x]
                changedmsg += "\n<"+str(a)+"> Rolled an init of "+str(b)+". (id = "+str(c)+")"
            changedmsg += "```"
            messagei = await bot.edit_message(messagei, changedmsg)
            
            stored_info[index][1][2] = initl
            stored_info[index][1][0] = messagei
            
        else:
            await bot.say("Id not found")

    
    
 #  except:
 #       await bot.say("Invalid use of this command, Correct Way to use is: ~di [id]")
        
        

@bot.command(name="startinit",pass_context=True,aliases=['si'])
async def startinit(ctx):
    global stored_info
    #print(stored_info)
    sID = ctx.message.server
    auth = ctx.message.author.id
    index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
    if not index == "":
        index = int(index)
        rinit = stored_info[index][1][1]
        if rinit == 0:
            global messagei
            global idnumber
            global initl
            messagei = await bot.send_message(ctx.message.channel, "```==========Init==========```")
            await bot.pin_message(messagei)
            rinit = 1
            idnumber = 0
            initl = []

            stored_info[index][1][1] = rinit
            stored_info[index][1][0] = messagei
            stored_info[index][1][2] = initl
            stored_info[index][1][3] = idnumber
            
        else:
            await bot.say("Init recording has already begun.")

@bot.command(name="endinit",aliases=['ei'],pass_context=True)
async def endinit(ctx):
    global stored_info
    sID = ctx.message.server
    index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
    if not index == "":
        index = int(index)
        rinit = stored_info[index][1][1]
        
        if rinit == 1:
            rinit = 0
            await bot.say("Init recording has stoped")
        else:
            await bot.say("Init recording is not started.")

        stored_info[index][1][1] = rinit

            

@bot.command(name="showinit",aliases=['showi'],pass_context=True)
async def showinit(ctx):
    global stored_info
    sID = ctx.message.server
    index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
    if not index == "":
        index = int(index)
        messagei = stored_info[index][1][0]
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

       
@bot.command(name="info",pass_context=True,aliases=['db','spellinfo','sinfo'])
async def info(ctx, *name):
    argst = name
    del name
    if debug == True:
        print(argst)
    #print(mod)
    argsl = list(argst)
    name = ' '.join(argsl)

    exit = False
    
    cID = ctx.message.author
    a = 0
    final = "```==========Info========="
    first = 1
    for y in corexml.childNodes:
        for x in y.childNodes:
            if x.nodeType == 1:
                if x.getElementsByTagName("name")[0].childNodes[0].nodeValue.lower() == name.lower():
                    for z in x.childNodes:
                        #print(z.nodeType)
                        
                        if z.nodeType == 1:
                            if not z.nodeName == "#text":
                                #print(z)
                                #print(z.nodeName)
                                try:
                                    if not z.nodeName == "text":
                                        final += "\n"+str(z.nodeName.capitalize())+": "+str(z.childNodes[0].nodeValue)
                                        for b in z.childNodes:
                                            if b.nodeType == 1:
                                                try:
                                                    if not b.nodeName == "text":
                                                        final += "\n        "+str(b.nodeName.capitalize())+": "+str(b.childNodes[0].nodeValue)
                                                    else:
                                                        if first == 1:
                                                            final += "\n"
                                                            first = 0
                                                        final += "\n"+str(b.childNodes[0].nodeValue)
                                                except:
                                                    final += "\n"
                                        #print(z.childNodes[0].nodeValue)
              #                          await bot.send_message(cID, z.nodeName+": "+z.childNodes[0].nodeValue)
                                    else:
                                        if first == 1:
                                            final += "\n"
                                            first = 0
                                        final += "\n"+str(z.childNodes[0].nodeValue)
                                except:
                                    final += "\n"

                    if debug == True:
                        print(x)
                    name = x.getElementsByTagName("name")[0].childNodes[0].nodeValue
                    #type = x.getElementsByTagName("type")[0].childNodes[0].nodeValue
                    if debug == True:
                        print(name)
#                    await bot.say(name+" "+type)
                
                    final += "```"
                    if debug == True:
                        print(final)
                    try:
                        if "\n" in final:
                            if debug == True:
                                print("yes")
                                print(final.rfind("\n"))
                            

                        while len(final) > 2000-3:
                            ind = final[:2000-3].rfind("\n")
                            if debug == True:
                                print(ind)
                            await bot.send_message(cID, final[:ind]+"```")
                            final = "```"+final[ind:]
                            
                        else:
                            await bot.send_message(cID, final)
                    except:
                        await bot.say("Were you trying to get the spell info of wish?\nFun fact: Wish is so powerfull it breaks this bot.\nDont use ~info wish, just use the wiki\n\nThis message is also pulled up when trying to get the info for any class\nSo please... just use the wiki for classes (and wish)\n\nSo this just in: this message appears when you try to access a file thats too big for discord.\nWhat can you do? Use the wiki.")
                    exit = True
                    break
                #else:
        a += 1
    if a == len(corexml.childNodes) and exit == False:
        await bot.say("Thing not found in database")
    if debug == True:
        print(spell)



@bot.command(name="initserver",pass_context=True,aliases=['is'])
async def initserver(ctx):
    global messagei
    if debug == True:
        print("starting")
    sID = ctx.message.server
    auth = ctx.message.author.id
    global stored_info
    rinit = 0
    initl = []
    idnumber = 0
    info = (sID,[messagei,rinit,initl,idnumber],[("ID",["NAME","MOD"])])
    stored_info.append(info)
    if debug == True:
        print(stored_info)


@bot.command(name="addinit",pass_context=True,aliases=['ai'])
async def addinit(ctx, name, *mod):
    
    namel = name
    del name
    argst = mod
    del mod
    argsl = list(argst)
    argsl.insert(0,namel)
    try:
        mod = int(argsl[-1])
        del argsl[-1]
    except:
        mod = 0
    name = ' '.join(argsl)

    name = str(name)
    mod = int(mod)
    
    global stored_info
    sID = ctx.message.server
    auth = ctx.message.author.id
    index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
    if not index == "":
        index = int(index)
        initdb = stored_info[index][2]
        
        y = str([i2 for i2, v2 in enumerate(stored_info[index][2]) if v2[0] == auth])[1:-1]
        if y == "":
            info = (auth, [name, mod])
            stored_info[index][2].append(info)
            print(stored_info[index][2])
        else:
            await bot.say("You already have a registered charecter")
    else:
        await bot.say("Server is not registered")


@bot.command(pass_context=True)
async def store(ctx):
    if str(ctx.message.author.id) == "161614687321063434":
        print("Saving")
        global stored_info
        if debug == True:
            print(repr(stored_info))
        
        pickle.dump( stored_info, open( "save.p", "wb" ) )
    else:
        await bot.say("You do not have the nessicary permissions")

@bot.command(pass_context=True)
async def deleteinfo(ctx):
    if str(ctx.message.author.id) == "161614687321063434":
        global stored_info
        print("Deleting")
        stored_info = []
        pickle.dump( stored_info, open( "save.p", "wb" ) )
    else:
        await bot.say("You do not have the nessicary permissions")
'''
@bot.command(pass_context=True)
async def i2(ctx):
    global stored_info
    sID = ctx.message.server
    auth = ctx.message.author.id
    index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
    if not index == "":
        index = int(index)
        print(index)
        y = str([i2 for i2, v2 in enumerate(stored_info[index][2]) if v2[0] == auth])[1:-1]
        if not y == "":
            y = int(y)
            print(stored_info[index][2][y][1][1])
    else:
        print("index does not exist")

'''




bot.loop.create_task(my_background_task())
bot.run("NDM4MTM5ODUwNTQ2MjE2OTcx.DcARFA.2SYJJFyqMhTTsU6D9aXPqXDmRbQ") #actual       
#bot.run("NDM4NDkxMDQ1MTEwNDgwODk2.DcFYJA.q3ivDLI__109cqRWL7sds6ZPwnI") # Test
