import discord
import asyncio
from discord.ext import commands
import random
import os
from xml.dom import minidom
import pickle
import sys
from datetime import datetime
import string
import unicodedata
#from git import Repo
#from github import Github


#import lxml
#from lxml import etree
BOT_PREFIX = ("~","/")
desc = "Your Typical DnD bot... except better."
bot = commands.Bot(command_prefix=BOT_PREFIX, description=desc,)


bot.remove_command('help')


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
    rolls.replace("-", "+-")
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

    old_f = sys.stdout
    class F:
        def write(self, x):
            old_f.write(x.replace("\n", " [%s]\n" % str(datetime.now())))
 #            old_f.write("["+str(datetime.now())+"] --- "+x)
    sys.stdout = F()
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
    else:
        await bot.say("Server not yet initialized, run /initserver or /is to initialize the server")

    
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
    else:
        await bot.say("Server not yet initialized, run /initserver or /is to initialize the server")

    
    
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
        pinmessage = stored_info[index][1][4]
        if rinit == 0:
            global messagei
            global idnumber
            global initl
            messagei = await bot.send_message(ctx.message.channel, "```==========Init==========```")
            try:
                if pinmessage == 1:
                    await bot.pin_message(messagei)
            except:
                await bot.send_message(ctx.message.author, "Cannot pin message, probably due to not having the manage message privlage in roles.")
            rinit = 1
            idnumber = 0
            initl = []

            stored_info[index][1][1] = rinit
            stored_info[index][1][0] = messagei
            stored_info[index][1][2] = initl
            stored_info[index][1][3] = idnumber
            
        else:
            await bot.say("Init recording has already begun.")
    else:
        await bot.say("Server not yet initialized, run /initserver or /is to initialize the server")

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
    else:
        await bot.say("Server not yet initialized, run /initserver or /is to initialize the server")

            

@bot.command(name="showinit",aliases=['showi'],pass_context=True)
async def showinit(ctx):
    global stored_info
    sID = ctx.message.server
    index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
    if not index == "":
        index = int(index)
        messagei = stored_info[index][1][0]
        if not messagei == None:
            await bot.say(messagei.content)
        else:
            await bot.say("Init rolling has not occured before, do /si or /startinit to start rolling")

    else:
        await bot.say("Server not yet initialized, run /initserver or /is to initialize the server")



@bot.command(name="roll",pass_context=True,aliases=['r'])
async def roll(ctx, *argst):
    try:
        breakdown = ""
        total = 0
        argsl = list(argst)
        rolls = ''.join(argsl)
        rolls = str.replace(rolls, "-", "+-")
        rollsl = rolls.split('+')
        multiplier = 1
        if debug == True:
            print(rollsl)
        for x in rollsl:
            if not x == "":
                if "d" in x:
                    subtotal = 0
                    #breakdown += "("
                    rollslx = x.split("d")
                    if rollslx[0] == "":
                        rollslx[0] = "1"
                    if rollslx[0] == "-":
                        rollslx[0] = "1"
                        multiplier = -1
                    if debug == True:
                        print(rollslx)
                    for y in range(int(rollslx[0])):
                        roll = random.randint(1,int(rollslx[1]))
                        roll *= multiplier
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
            try:
                await bot.delete_message(ctx.message)
                await bot.say("<@"+str(ctx.message.author.id)+"> Rolled a **"+str(total)+"**. ("+breakdown+") [Command Inputed:"+ctx.message.content+"]")
            except:
                await bot.say("<@"+str(ctx.message.author.id)+"> Rolled a **"+str(total)+"**. ("+breakdown+")")
        else:
            try:
                await bot.delete_message(ctx.message)
                await bot.say("<@"+str(ctx.message.author.id)+"> Rolled a **"+str(total)+"**. [Command Inputed:"+ctx.message.content+"]")
            except:
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
                        #await bot.say("Were you trying to get the spell info of wish?\nFun fact: Wish is so powerfull it breaks this bot.\nDont use ~info wish, just use the wiki\n\nThis message is also pulled up when trying to get the info for any class\nSo please... just use the wiki for classes (and wish)\n\nSo this just in: this message appears when you try to access a file thats too big for discord.\nWhat can you do? Use the wiki.")
                        await bot.say("This message typicaly occurs when one has private messaging disabled.\nDue to the size of the info, we are required to pm you with it.\nTo use this command, allow bots to pm you.")
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
    sID = ctx.message.server
    global stored_info
    index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
    if index == "":
        global messagei
        if debug == True:
            print("starting")
        auth = ctx.message.author.id
        rinit = 0
        initl = []
        idnumber = 0
        pinmessage = 0
        info = (sID,[messagei,rinit,initl,idnumber,pinmessage],[("ID",["NAME","MOD"])])
        stored_info.append(info)
        try:
            await bot.delete_message(ctx.message)
            await bot.say("Server initialized")
        except:
            await bot.say("Server initialized")
        if debug == True:
            print(stored_info)
        print("New Server Initialized - "+str(ctx.message.server.name))
    else:
        await bot.say("Server already initialized")

@bot.command(name="addinit",pass_context=True,aliases=['ai'],description="Adds a player to the Inititive database",brief="Adds a player to the Inititive database")
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
            #print(stored_info[index][2])
            try:
                await bot.delete_message(ctx.message)
                await bot.say("<@"+str(auth)+"> has registered charecter: "+name+" with a mod of "+str(mod)+" [Command Inputed:"+ctx.message.content+"]")
            except:
                await bot.say("You have registered charecter: "+name+" with a mod of "+str(mod))

        else:
            await bot.say("You already have a registered charecter")
    else:
        await bot.say("Server not yet initialized, run /initserver or /is to initialize the server")



@bot.command(name="removeinit",pass_context=True,aliases=['ri'])
async def removeinit(ctx):
    
    global stored_info
    sID = ctx.message.server
    auth = ctx.message.author.id
    index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
    if not index == "":
        index = int(index)
        initdb = stored_info[index][2]
        
        y = str([i2 for i2, v2 in enumerate(stored_info[index][2]) if v2[0] == auth])[1:-1]
        if not y == "":
            y = int(y)
            name = stored_info[index][2][y][1][0]
            mod = stored_info[index][2][y][1][1]
            del stored_info[index][2][y]
            #print(stored_info[index][2])
            try:
                await bot.delete_message(ctx.message)
    #            await bot.edit_message(ctx.message,"You have unregistered charecter: "+name+" with a mod of "+str(mod)) 
                await bot.say("<@"+str(auth)+"> has unregistered charecter: "+name+" with a mod of "+str(mod)+" [Command Inputed:"+ctx.message.content+"]")
            except:
                await bot.say("You have unregistered charecter: "+name+" with a mod of "+str(mod))

        else:
            await bot.say("You have no registered charecters for this server")
    else:
        await bot.say("Server not yet initialized, run /initserver or /is to initialize the server")




@bot.command(pass_context=True, hidden=True)
async def store(ctx):
    if str(ctx.message.author.id) == "161614687321063434":
        print("Saving")
        global stored_info
        if debug == True:
            print(repr(stored_info))
        
        pickle.dump( stored_info, open( "save.p", "wb" ) )
    else:
        await bot.say("You do not have the necessary permissions")

@bot.command(pass_context=True, hidden=True)
async def deleteinfo(ctx):
    if str(ctx.message.author.id) == "161614687321063434":
        global stored_info
        print("Deleting")
        stored_info = []
        pickle.dump( stored_info, open( "save.p", "wb" ) )
    else:
        await bot.say("You do not have the necessary permissions")

@bot.command(pass_context=True, hidden=True)
async def exportfile(ctx):
    if str(ctx.message.author.id) == "161614687321063434":
        global stored_info

        print("Saving")
        pickle.dump(stored_info, open("save.p", "wb"))
        print("Exporting")
        #print(repr(stored_info))
        await bot.send_file(ctx.message.author, "save.p")
    else:
        await bot.say("You do not have the necessary permissions")

@bot.command(pass_context=True, hidden=True)
async def importfile(ctx):
    if str(ctx.message.author.id) == "161614687321063434":
        global stored_info
        print(repr(stored_info))
        print("Importing")
        stored_info = pickle.load( open( "save.p", "rb" ) )
        #print(repr(stored_info))
    else:
        await bot.say("You do not have the necessary permissions")

@bot.command(name="help",aliases=['h'])
async def help(command="None"):
    
    commandlist = []
    commandlist.append(("roll","r","Anyone can use to roll standard dice expressions"))
    commandlist.append(("cast","c","Anyone can use to cast a spell (rolls dice for Hit and Damage)"))
    commandlist.append(("info","db","Anyone can use to get info for any core \"Thing\" inside DnD"))
    
    helptxt = "```css"+"\n"+"[Your Typical DnD bot... except better.]"+"```"
    helptxt += "```md"+"\n[Command Group][Basic]\n"
    helptxt += "\n</roll (r)> <Anyone can use to roll standard dice expressions>"
    helptxt += "\n</cast (c)> <Anyone can use to cast a spell (rolls dice for Hit and Damage)>"
    helptxt += "\n</info (db)> <Anyone can use to get info for any core \"Thing\" inside DnD>"
    helptxt += "```"
    helptxt += "```md"+"\n[Command Group][Init]\n"
    helptxt += "\n</initserver (is)> <GM uses to enable init commands on the server>"
    helptxt += "\n</startinit (si)> <GM uses to start init rolling>"
    helptxt += "\n</endinit (ei)> <GM uses to end init rolling>"
    helptxt += "\n</deleteinit (di)> <GM uses to remove someone (by id) from the current init list>"
    helptxt += "\n</showinit (showi)> <Anyone can use this to show the current init list>"
    helptxt += "\n</init (i)> <Anyone can use this to add themselves to the current init list>"
    helptxt += "\n</addinit (ai)> <Players can use this to add their init mod to the bot database [syntax is /ai (name) (mod)]>"
    helptxt += "\n</removeinit (ri)> <Players can use this to remove their character from the bot database>"
    helptxt += "\n</togglepin (tp)> <GM uses to toggle pinning init list (Default = Off)>"
    helptxt += "```"
    await bot.say(helptxt)

@bot.command(name="togglepin",aliases=['tp'],pass_context=True)
async def togglepin(ctx):
    global stored_info
    sID = ctx.message.server
    auth = ctx.message.author.id
    index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
    if not index == "":
        index = int(index)
        pinmessage = stored_info[index][1][4]
        if pinmessage == 0:
            pinmessage = 1
            try:
                await bot.delete_message(ctx.message)
                await bot.say("Pins Turned On")
            except:
                await bot.say("Pins Turned On")
        else:
            pinmessage = 0
            try:
                await bot.delete_message(ctx.message)
                await bot.say("Pins Turned Off")
            except:
                await bot.say("Pins Turned Off")

        stored_info[index][1][4] = pinmessage
    else:
        await bot.say("Server not yet initialized, run /initserver or /is to initialize the server")

        
@bot.command(name="d20",pass_context=True)
async def d20(ctx, mod=0):
    roll = random.randint(1,20)
    try:
        roll = mod+roll
        await bot.say("<@"+str(ctx.message.author.id)+"> Rolled a "+str(roll))
    except:
        await bot.say("Invalid d20 expression, do no have + inside the expression")
    


@bot.command(name="test",pass_context=True)
async def test(ctx):
    messagec = await bot.say("Enter Char Name")
    messagei = await bot.wait_for_message(author=ctx.message.author)
    messagec = await bot.edit_message(messagec, messagei.content)
    await bot.delete_message(messagei)
    num = ["0⃣","1⃣","2⃣","3⃣","4⃣","5⃣","6⃣","7⃣","8⃣","9⃣"]
    messagec = await bot.edit_message(messagec, messagec.content+"\nPlease Enter Your init\nInit: ")
    for x in num:
        await bot.add_reaction(messagec,x)

    await bot.add_reaction(messagec,u"\U0001F51A")
    await bot.add_reaction(messagec,u"\u23EA")
    
    end = False
    while end == False:
        res = await bot.wait_for_reaction(message=messagec,user=ctx.message.author)
        emoji = res.reaction.emoji
        if emoji == u"\U0001F51A":
            await bot.say("Complete")
            end = True
        elif emoji == u"\u23EA":
            messagec = await bot.edit_message(messagec, messagec.content[:-1])
        else:
            for x in range(0, len(num)):
                if emoji == num[x]:
                    messagec = await bot.edit_message(messagec, messagec.content+str(x))
     #   await bot.edit_message(messagec, messagec.content+" "+res.reaction.emoji)
     
    
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
