import discord
import asyncio
from discord.ext import commands
import random
import os
from xml.dom import minidom
import pickle
import sys
from datetime import datetime
from copy import deepcopy
#import string
#import unicodedata
#from git import Repo
#from github import Github


#import lxml
#from lxml import etree
BOT_PREFIX = ("~","/")
desc = "Your Typical DnD bot... except better."
bot = commands.Bot(command_prefix=BOT_PREFIX, description=desc)


gitUser = os.environ["GitUser"]
gitPass = os.environ["GitPass"]


token = os.environ["Token"]
debugS = os.environ["Debug"]
if debugS == "true":
	debug = True
else:
	debug = False


bot.remove_command('help')


filelocation = os.environ["Location"]


xmlDoc = minidom.parse('db.xml')
corexml = minidom.parse('Core.xml')
spellxml = corexml.getElementsByTagName("spell")


messagei = None
rinit = 0 #if were rolling init at this point
initl = [] #list of all init stuff
idnumber = 0 #id nubmer
#db = etree.parse("db.xml")



### IMPORTANT ###
#stored_info = [(channelID,[vars,(messagei,messagei),(rinit,rinit),(initl,initl),(idnumber,idnumber)],[init, (playerID, data), (playerID, data)]),(channelID,info)]
'''
Top level -> lowest

stored info
(channelID,vars,init)

vars
messages,rinit,initl,idnumber

init
(playerID,data)

storedinfo.append((sID,[messagei,rinit,initl,idnumber,pinmessage],[("ID",["NAME","MOD"])])) # LATEST
'''

#stored_info = [(channelID,[vars,(messagei,messagei),(rinit,rinit),(initl,initl),(idnumber,idnumber)],[init, (playerID, data), (playerID, data)])]
stored_info = []





async def my_background_task():
	await bot.wait_until_ready()
	counter = 0
	#   channel = discord.Object(id='161614687321063434')
	while not bot.is_closed:
		await asyncio.sleep(21600) # task runs every 6 hours
		saveData()
		counter += 1




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
	if debug:
		print(stored_info)

	stored_info = []
	loadData()

	if debug:
		print(stored_info)

	await bot.change_presence(activity=discord.Game(name='Type /help for help'))

	'''
	old_f = sys.stdout
	class F:
		def write(self, x):
			old_f.write(x.replace("\n", " [%s]\n" % str(datetime.now())))
	#            old_f.write("["+str(datetime.now())+"] --- "+x)
	sys.stdout = F()
	'''
#   await bot.change_presence('Type /help for help')
#   await bot.change_presence(game=discord.Game(name='Type /help for help'))
#   await bot.change_status(game=discord.Game(name = "Type /help for help"))

@bot.event
async def wait_until_login():
	await bot.change_presence(activity=discord.Game(name='Type /help for help'))


#@bot.command(name="init",pass_context=True,aliases=['i'])
@bot.command(name="init",aliases=['i'])
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
	sID = ctx.channel
	auth = ctx.author.id
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
					clientid = ctx.author.id
					changedmsg = "```==========Init=========="
					for x in range(0, len(initl)):
						print(initl[x])
						a,b,c = initl[x]
						changedmsg += "\n<"+str(a)+"> Rolled an init of "+str(b)+". (id = "+str(c)+")"
					changedmsg += "```"
					#messagei = await messagei.edit(content=changedmsg)
					await messagei.edit(content=changedmsg)
				else:
					await ctx.send("You are not yet registered")
			else:
				idnumber = idnumber+1
				init = random.randint(1,20)
				init = init+mod
				initl.append((name,init,idnumber))
				initl.sort(key=lambda tup: tup[1], reverse=True)
				clientid = ctx.author.id
				changedmsg = "```==========Init=========="
				for x in range(0, len(initl)):
					print(initl[x])
					a,b,c = initl[x]
					changedmsg += "\n<"+str(a)+"> Rolled an init of "+str(b)+". (id = "+str(c)+")"
				changedmsg += "```"
				#messagei = await messagei.edit(content=changedmsg)
				await messagei.edit(content=changedmsg)
		else:
			await ctx.send("Init Rolling has not started yet")

		stored_info[index][1][1] = rinit
		stored_info[index][1][0] = messagei
		stored_info[index][1][2] = initl
		stored_info[index][1][3] = idnumber
	else:
		await ctx.send("Channel not yet initialized, run /initchannel or /ic to initialize the channel")


@bot.command(name="deleteinit",pass_context=True,aliases=['di'])
async def deleteinit(ctx, id):
	global stored_info
	#print(stored_info)
	sID = ctx.channel
	auth = ctx.author.id
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
			#messagei = await messagei.edit(changedmsg)
			await messagei.edit(content=changedmsg)

			stored_info[index][1][2] = initl
			stored_info[index][1][0] = messagei

		else:
			await ctx.send("Id not found")
	else:
		await ctx.send("Channel not yet initialized, run /initchannel or /ic to initialize the channel")



#  except:
#       await ctx.send("Invalid use of this command, Correct Way to use is: ~di [id]")



@bot.command(name="startinit",pass_context=True,aliases=['si'])
async def startinit(ctx):
	global stored_info
	#print(stored_info)
	sID = ctx.channel
	auth = ctx.author.id
	index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
	if not index == "":
		index = int(index)
		rinit = stored_info[index][1][1]
		pinmessage = stored_info[index][1][4]
		if rinit == 0:
			global messagei
			global idnumber
			global initl
			messagei = await ctx.send("```==========Init==========```")
			try:
				if pinmessage == 1:
					await bot.pin_message(messagei)
			except:
				await ctx.author.send("Cannot pin message, probably due to not having the manage message privlage in roles.")
			rinit = 1
			idnumber = 0
			initl = []

			stored_info[index][1][1] = rinit
			stored_info[index][1][0] = messagei
			stored_info[index][1][2] = initl
			stored_info[index][1][3] = idnumber

		else:
			await ctx.send("Init recording has already begun.")
	else:
		await ctx.send("Channel not yet initialized, run /initchannel or /ic to initialize the channel")

@bot.command(name="endinit",aliases=['ei'],pass_context=True)
async def endinit(ctx):
	global stored_info
	sID = ctx.channel
	index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
	if not index == "":
		index = int(index)
		rinit = stored_info[index][1][1]

		if rinit == 1:
			rinit = 0
			await ctx.send("Init recording has stoped")
		else:
			await ctx.send("Init recording is not started.")

		stored_info[index][1][1] = rinit
	else:
		await ctx.send("Channel not yet initialized, run /initchannel or /ic to initialize the channel")



@bot.command(name="showinit",aliases=['showi'],pass_context=True)
async def showinit(ctx):
	global stored_info
	sID = ctx.channel
	index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
	if not index == "":
		index = int(index)
		messagei = stored_info[index][1][0]
		if not messagei == None:
			await ctx.send(messagei.content)
		else:
			await ctx.send("Init rolling has not occured before, do /si or /startinit to start rolling")

	else:
		await ctx.send("Channel not yet initialized, run /initchannel or /ic to initialize the channel")



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
		if debug:
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
					if debug:
						print(rollslx)
					for y in range(int(rollslx[0])):
						roll = random.randint(1,int(rollslx[1]))
						roll *= multiplier
						subtotal += roll
						breakdown += str(roll)+" + "
					breakdown = breakdown[:-3]
					if debug:
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

		if debug:
			print(total)
		breakdown = breakdown[:-4]
		if "," in breakdown or "+" in breakdown:
			try:
				await bot.delete_message(ctx)
				await ctx.send("<@"+str(ctx.author.id)+"> Rolled a **"+str(total)+"**. ("+breakdown+") [Command Inputed:"+ctx.message.content+"]")
			except:
				await ctx.send("<@"+str(ctx.author.id)+"> Rolled a **"+str(total)+"**. ("+breakdown+")")
		else:
			try:
				await bot.delete_message(ctx)
				await ctx.send("<@"+str(ctx.author.id)+"> Rolled a **"+str(total)+"**. [Command Inputed:"+ctx.message.content+"]")
			except:
				await ctx.send("<@"+str(ctx.author.id)+"> Rolled a **"+str(total)+"**.")
		if debug:
			print(breakdown)
		#await ctx.send(breakdown)
	except:
		await ctx.send("<@"+str(ctx.author.id)+"> specified an invalid dice expression.")




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
		if debug:
			print(argst)
		#print(mod)
		argsl = list(argst)
		argsl.insert(0,spell)
		if debug:
			print(argsl)
		try:
			slot = str(int(argsl[-1]))
			del argsl[-1]
		except:
			slot = "min"

		spell = ' '.join(argsl)
		if debug:
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
				clientid = ctx.author.id
				if not damage == "N/A":
					await ctx.send("<@"+str(ctx.author.id)+"> Attacked with "+spell+":\n"+str(hit)+" vs AC\n"+str(damage)+" Damage")
				else:
					await ctx.send("<@"+str(ctx.author.id)+"> Used "+spell+":\n"+str(hit)+" vs DC")
				break
			else:
				y += 1
		if y == len(spellxml):
			await ctx.send("Spell not found in database")
		if debug:
			print(spell)
			print(slot)
	except:
		await ctx.send("<@"+str(ctx.author.id)+"> entered an invalid expression.\nThe correct way to use this command is: ~cast [spell name] [spell slot]")


@bot.command(name="info",pass_context=True,aliases=['db','spellinfo','sinfo'])
async def info(ctx, *name):
	argst = name
	del name
	if debug:
		print(argst)
	#print(mod)
	argsl = list(argst)
	name = ' '.join(argsl)

	exit = False

	cID = ctx.author
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

					if debug:
						print(x)
					name = x.getElementsByTagName("name")[0].childNodes[0].nodeValue
					#type = x.getElementsByTagName("type")[0].childNodes[0].nodeValue
					if debug:
						print(name)
					#                    await ctx.send(name+" "+type)

					final += "```"
					if debug:
						print(final)
					try:
						if "\n" in final:
							if debug:
								print("yes")
								print(final.rfind("\n"))


						while len(final) > 2000-3:
							ind = final[:2000-3].rfind("\n")
							if debug:
								print(ind)
							await cID.send(final[:ind]+"```")
							final = "```"+final[ind:]

						else:
							await cID.send(final)
					except:
						#await ctx.send("Were you trying to get the spell info of wish?\nFun fact: Wish is so powerfull it breaks this bot.\nDont use ~info wish, just use the wiki\n\nThis message is also pulled up when trying to get the info for any class\nSo please... just use the wiki for classes (and wish)\n\nSo this just in: this message appears when you try to access a file thats too big for discord.\nWhat can you do? Use the wiki.")
						await ctx.send("This message typicaly occurs when one has private messaging disabled.\nDue to the size of the info, we are required to pm you with it.\nTo use this command, allow bots to pm you.")
					exit = True
					break
				#else:
		a += 1
	if a == len(corexml.childNodes) and exit == False:
		await ctx.send("Thing not found in database")
	if debug:
		print(name)



@bot.command(name="initchannel",pass_context=True,aliases=['ic'])
async def initchannel(ctx):
	sID = ctx.channel
	global stored_info
	index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
	if index == "":
		global messagei
		if debug:
			print("starting")
		auth = ctx.author.id
		rinit = 0
		initl = []
		idnumber = 0
		pinmessage = 0
		info = (sID,[messagei,rinit,initl,idnumber,pinmessage],[("ID",["NAME","MOD"])],[("ID",["NAME","MACRO"])])
		stored_info.append(info)
		try:
			await bot.delete_message(ctx)
			await ctx.send("Channel initialized")
		except:
			await ctx.send("Channel initialized")
		if debug:
			print(stored_info)
		print("New Channel initialized - "+str(ctx.channel))
	else:
		await ctx.send("Channel already initialized")

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
	sID = ctx.channel
	auth = ctx.author.id
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
				await bot.delete_message(ctx)
				await ctx.send("<@"+str(auth)+"> has registered charecter: "+name+" with a mod of "+str(mod)+" [Command Inputed:"+ctx.message.content+"]")
			except:
				await ctx.send("You have registered charecter: "+name+" with a mod of "+str(mod))

		else:
			await ctx.send("You already have a registered charecter")
	else:
		await ctx.send("Channel not yet initialized, run /initchannel or /ic to initialize the channel")



@bot.command(name="removeinit",pass_context=True,aliases=['ri'])
async def removeinit(ctx):

	global stored_info
	sID = ctx.channel
	auth = ctx.author.id
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
				await bot.delete_message(ctx)
				#            await bot.edit_message(ctx,"You have unregistered charecter: "+name+" with a mod of "+str(mod))
				await ctx.send("<@"+str(auth)+"> has unregistered charecter: "+name+" with a mod of "+str(mod)+" [Command Inputed:"+ctx.message.content+"]")
			except:
				await ctx.send("You have unregistered charecter: "+name+" with a mod of "+str(mod))

		else:
			await ctx.send("You have no registered charecters for this channel")
	else:
		await ctx.send("Channel not yet initialized, run /initchannel or /ic to initialize the channel")




@bot.command(pass_context=True, hidden=True)
async def store(ctx):
	if str(ctx.author.id) == "161614687321063434":
		saveData()
	else:
		await ctx.send("You do not have the necessary permissions")

@bot.command(pass_context=True, hidden=True)
async def deleteinfo(ctx):
	if str(ctx.author.id) == "161614687321063434":
		deleteData()
	else:
		await ctx.send("You do not have the necessary permissions")

@bot.command(pass_context=True, hidden=True)
async def exportfile(ctx):
	if str(ctx.author.id) == "161614687321063434":
		exportData()
		await bot.send_file(ctx.author, "save.p")
		os.system("rm save.p")
	else:
		await ctx.send("You do not have the necessary permissions")

@bot.command(pass_context=True, hidden=True)
async def importfile(ctx):
	if str(ctx.author.id) == "161614687321063434":
		loadData()
	else:
		await ctx.send("You do not have the necessary permissions")

@bot.command(name="help",aliases=['h'])
async def help(ctx,command="None"):
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
	helptxt += "\n</initchannel (ic)> <GM uses to enable init commands on the channel>"
	helptxt += "\n</startinit (si)> <GM uses to start init rolling>"
	helptxt += "\n</endinit (ei)> <GM uses to end init rolling>"
	helptxt += "\n</deleteinit (di)> <GM uses to remove someone (by id) from the current init list>"
	helptxt += "\n</showinit (showi)> <Anyone can use this to show the current init list>"
	helptxt += "\n</init (i)> <Anyone can use this to add themselves to the current init list>"
	helptxt += "\n</addinit (ai)> <Players can use this to add their init mod to the bot database [syntax is /ai (name) (mod)]>"
	helptxt += "\n</removeinit (ri)> <Players can use this to remove their character from the bot database>"
	helptxt += "\n</togglepin (tp)> <GM uses to toggle pinning init list (Default = Off)>"
	helptxt += "```"
	helptxt += "```md"+"\n[Command Group][Macro]\n"
	helptxt += "\n</macrostore (ms)> <Anyone can use to save \"roll templates\" [syntax is /ms (name) (macro)]>"
	helptxt += "\n</macrouse (mu)> <Anyone can use to activate a saved \"roll template\" [syntax is /mu (name) (macro)]>"
	helptxt += "\n</macrolist (ml)> <Anyone can use to list all saved \"roll templates\" for the channel>"
	helptxt += "\n</macroview (mv)> <Anyone can use to see a saved \"roll template\" without running it [syntax is /mv (name)]>"
	helptxt += "\n</macrodelete (md)> <Anyone can use to delete a saved \"roll template\" [syntax is /md (name)]>"
	helptxt += "```"
	await ctx.channel.send(helptxt)

@bot.command(name="togglepin",aliases=['tp'],pass_context=True)
async def togglepin(ctx):
	global stored_info
	sID = ctx.channel
	auth = ctx.author.id
	index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
	if not index == "":
		index = int(index)
		pinmessage = stored_info[index][1][4]
		if pinmessage == 0:
			pinmessage = 1
			try:
				await bot.delete_message(ctx)
				await ctx.send("Pins Turned On")
			except:
				await ctx.send("Pins Turned On")
		else:
			pinmessage = 0
			try:
				await bot.delete_message(ctx)
				await ctx.send("Pins Turned Off")
			except:
				await ctx.send("Pins Turned Off")

		stored_info[index][1][4] = pinmessage
	else:
		await ctx.send("Channel not yet initialized, run /initchannel or /ic to initialize the channel")


@bot.command(name="d20",pass_context=True)
async def d20(ctx, mod=0):
	roll = random.randint(1,20)
	try:
		roll = mod+roll
		await ctx.send("<@"+str(ctx.author.id)+"> Rolled a "+str(roll))
	except:
		await ctx.send("Invalid d20 expression, do no have + inside the expression")




@bot.command(name="macrouse",pass_context=True,aliases=['mu'])
async def macrouse(ctx,name):
	global stored_info
	sID = ctx.channel
	auth = ctx.author
	index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
	if not index == "":
		index = int(index)
		if debug:
			print(index)
		y = str([i2 for i2, v2 in enumerate(stored_info[index][3]) if v2[0] == auth])[1:-1]
		if not y == "":
			y = int(y)
			try:
				outputl = deepcopy(stored_info[index][3][y][1][name])

				leftBracket = "[~AgStBsafV=["
				rightBracket = "]=GsafGjsA+]"

				commands = "```css" + "\nCommands Used {from first to last} : ["
				commandlen = len(commands)

				ind = 0
				for x in outputl:
					try:
						if rightBracket in x and leftBracket in x:
							x = x.replace(leftBracket, "")
							x = x.replace(rightBracket, "")
							nx = str(internal_roll(x))
							commands += x + ", "
							outputl[ind] = "<" + nx + ">"
						ind += 1
					except:
						print("Failed to do roll")

				output = ''.join(outputl)

				if debug:
					print(output)

				try:
					await bot.delete_message(ctx)
					await ctx.send("<@{}> used a macro: \'{}\'".format(auth.id,name))
					await ctx.send(output)
				except:
					await ctx.send("<@{}> used a macro: \'{}\'".format(auth.id,name))
					await ctx.send(output)

				if debug:
					print(commands)
				if not commandlen == len(commands):
					if debug:
						print("commandlen: " + str(commandlen))
						print("commandlength: " + str(len(commands)))
					commands = commands[:-2]
					commands += "]```"
					# commands = commands.replace("[", "<")
					# commands = commands.replace("]", ">")
					await ctx.send(commands)
			except KeyError:
				await ctx.send("This macro does not exist")
		else:
			if debug:
				print(stored_info[index][3])




	else:
		await ctx.send("Channel not yet initialized, run /initchannel or /ic to initialize the channel")


@bot.command(name="macrostore",pass_context=True,aliases=['ms'])
async def macrostore(ctx, name):


	sID = ctx.channel
	print(ctx)
	message = ctx.message.content
	output = message[message.index(name)+len(name):]
	if debug:
		print("~~~~~")
		print(output)
		#await ctx.send(output)
		print("~~~~~")

	'''
	argst = output
	del output
	if debug:
		print(argst)
	#print(mod)
	argsl = list(argst)
	output = ' '.join(argsl)
	'''
	#print(output)

	exit = False

	auth = ctx.author

	'''
	if "```" in output:
		index = output.find("```")
		await ctx.send(index)
		index += 3
	'''

	leftBracket = "[~AgStBsafV=["
	rightBracket = "]=GsafGjsA+]"

	output = output.replace("\\n", "\n")
	output = output.replace("</roll>", rightBracket+"</roll>")
	output = output.replace("<roll>", "<roll>"+leftBracket)
	output = output.replace("</roll>", "<roll>")
	outputl = output.split('<roll>')
	if debug:
		print(outputl)




	savel = deepcopy(outputl)



	#info = (sID,[messagei,rinit,initl,idnumber,pinmessage],[("ID",["NAME","MOD"])],[("ID",["NAME","MACRO"])])

	index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
	if not index == "":
		index = int(index)

		y = str([i2 for i2, v2 in enumerate(stored_info[index][3]) if v2[0] == auth])[1:-1]
		if y == "":
			info = (auth, {name: savel})
			stored_info[index][3].append(info)

		else:
			if debug:
				print(stored_info[index][3])
			stored_info[index][3][int(y)][1][name] = savel

		try:
			await bot.delete_message(ctx)
			await ctx.send("<@{}> created a new macro; \'{}\'".format(auth.id,name))
		except:
			await ctx.send("<@{}> created a new macro; \'{}\'".format(auth.id,name))

	else:
		await ctx.send("Channel not yet initialized, run /initchannel or /ic to initialize the channel")


@bot.command(name="macrolist",aliases=['ml'])
async def macrolist(ctx):


	sID = ctx.channel
	message = ctx.message.content
	auth = ctx.author



	#info = (sID,[messagei,rinit,initl,idnumber,pinmessage],[("ID",["NAME","MOD"])],[("ID",["NAME","MACRO"])])

	index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
	if not index == "":
		index = int(index)

		y = str([i2 for i2, v2 in enumerate(stored_info[index][3]) if v2[0] == auth])[1:-1]
		if y == "":
			#info = (auth, {name: savel})
			#stored_info[index][3].append(info)
			await auth.send("Sorry, You have no macros on the channel: <#{}>".format(sID.id))

		else:
			if debug:
				print(stored_info[index][3])
			#stored_info[index][3][int(y)][1][name] = savel
			final = "You have the following macros on the channel <#{}>:\n".format(sID.id)
			for x in stored_info[index][3][int(y)][1]:
				final += x
				final += ", "
			final = final[:-2]

			await auth.send(final)

	else:
		await ctx.send("Channel not yet initialized, run /initchannel or /ic to initialize the channel")



@bot.command(name="macrodelete",pass_context=True,aliases=['md'])
async def macrodelete(ctx,name):
	global stored_info
	sID = ctx.channel
	auth = ctx.author
	index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
	if not index == "":
		index = int(index)
		if debug:
			print(index)
		y = str([i2 for i2, v2 in enumerate(stored_info[index][3]) if v2[0] == auth])[1:-1]
		if not y == "":
			y = int(y)

			try:
				stored_info[index][3][y][1].pop(name)
				await ctx.send("<@{}> deleted a macro: \'{}\'".format(auth.id,name))

			except KeyError:
				await ctx.send("This macro does not exist")

		else:
			if debug:
				print(stored_info[index][3])




	else:
		await ctx.send("Channel not yet initialized, run /initchannel or /ic to initialize the channel")






@bot.command(name="macroview",pass_context=True,aliases=['mv'])
async def macroview(ctx,name):
	global stored_info
	sID = ctx.channel
	auth = ctx.author
	index = str([i for i, v in enumerate(stored_info) if v[0] == sID])[1:-1]
	if not index == "":
		index = int(index)
		if debug:
			print(index)
		y = str([i2 for i2, v2 in enumerate(stored_info[index][3]) if v2[0] == auth])[1:-1]
		if not y == "":
			y = int(y)
			try:
				outputl = deepcopy(stored_info[index][3][y][1][name])
				output = ''.join(outputl)

				leftBracket = "[~AgStBsafV=["
				rightBracket = "]=GsafGjsA+]"
				output = output.replace(rightBracket, "</roll>")
				output = output.replace(leftBracket, "<roll>")

				if debug:
					print(output)
				await auth.send("This is the macro \'{}\' on the channel <#{}>".format(name,sID.id))
				await auth.send(output)

			except KeyError:
				await ctx.send("This macro does not exist")
		else:
			if debug:
				print(stored_info[index][3])

	else:
		await ctx.send("Channel not yet initialized, run /initchannel or /ic to initialize the channel")









def internal_roll(*argst):
	total = 0
	argsl = list(argst)
	rolls = ''.join(argsl)
	rolls.replace("-", "+-")
	rollsl = rolls.split('+')
	if debug:
		print(rollsl)
	for x in rollsl:
		if "d" in x:
			subtotal = 0
			rollslx = x.split("d")
			if rollslx[0] == "":
				rollslx[0] = "1"
			if debug:
				print(rollslx)
			for x in range(int(rollslx[0])):
				roll = random.randint(1,int(rollslx[1]))
				subtotal += roll
			if debug:
				print(subtotal)
			total += subtotal
		else:
			total += int(x)
			if debug:
				print(int(x))
	if debug:
		print(total)
	return total


def saveData():
	print("Saving Data")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	global stored_info
	if debug:
		print(repr(stored_info))

	os.system("git clone https://github.com/M0RGaming/TableTopBot.git saves")
	os.system("cd saves && git config user.email 'ttb@m0rgaming.ga' && git config user.name 'TableTopBot'")
	os.system("cd saves && git checkout storage")
	pickle.dump( stored_info, open( "saves/save.p", "wb" ) )
	os.system("cd saves && git add save.p && git commit -m 'Saving Info' && git push https://{}:{}@github.com/M0RGaming/TableTopBot.git".format(gitUser,gitPass))
	os.system("rm -r saves")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def loadData():
	global stored_info
	stored_info = []
	print(repr(stored_info))
	print("Loading Data")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

	os.system("git clone https://github.com/M0RGaming/TableTopBot.git saves")
	os.system("cd saves && git checkout storage")
	stored_info = pickle.load( open( "saves/save.p", "rb" ) )
	os.system("rm -r saves")
	if debug:
		print(repr(stored_info))
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


def deleteData():
	global stored_info
	print("Deleting Data")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	stored_info = []
	if debug:
		print(repr(stored_info))

	os.system("git clone https://github.com/M0RGaming/TableTopBot.git saves")
	os.system("cd saves && git config user.email 'ttb@m0rgaming.ga' && git config user.name 'TableTopBot'")
	os.system("cd saves && git checkout storage")
	pickle.dump( stored_info, open( "saves/save.p", "wb" ) )
	os.system("cd saves && git add save.p && git commit -m 'Deleting Info' && git push https://{}:{}@github.com/M0RGaming/TableTopBot.git".format(gitUser,gitPass))
	os.system("rm -r saves")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def exportData():
	global stored_info
	saveData()
	print(repr(stored_info))
	print("Exporting Data")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

	os.system("git clone https://github.com/M0RGaming/TableTopBot.git saves")
	os.system("cd saves && git checkout storage")
	os.system("cp saves/save.p .")
	os.system("rm -r saves")
	if debug:
		print(repr(stored_info))
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

@bot.command(name="displayData",aliases=['dd'])
async def displayData(ctx):
	global stored_info
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	await ctx.send(repr(stored_info))
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


bot.loop.create_task(my_background_task())
bot.run(token) # Run token
