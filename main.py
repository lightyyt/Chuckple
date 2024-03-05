#pylint:disable= '\*'. String constant might be missing an r prefix.
#pylint:disable=W0105
#pylint:disable=W0603


#--------------------IMPORTS--------------------#
import discord, asyncio
import joke
import sqlite3
from re import sub


#Quick Code for Clearing the Screen
from os import system as t1, name as t2
if t2 == "nt":
	t1("cls")
else:
	t1("clear")
del t1, t2


#--------------------DATABASE--------------------#
cndb = sqlite3.connect("server_configs.db")
conf = cndb.cursor()

try:
	conf.execute("CREATE TABLE prefs(srv, translateit, more_joke_info )")
except sqlite3.OperationalError: pass

#--------------------BOT--------------------#
#---------------INTENTS---------------#
intents = discord.Intents.default()
intents.message_content = True

#---------------CLIENT---------------#
ping = ""
client = discord.Client(intents=intents)
@client.event
async def on_ready():
	print(f'Connected to {client.user}')
	for server in client.guilds:
		query = conf.execute('SELECT * FROM prefs WHERE srv = '+str(server.id))
		
		if query.fetchone() == None:
			print("Server: "+server.name+" has not had a config made. making one...")
			conf.execute("INSERT INTO prefs VALUES ("+str(server.id)+",0,0)")
			cndb.commit()
			
#---------------COMMANDS---------------#
@client.event
async def on_message(message):
	global ping
	#If Bot Ping hasnt been Set
	if ping == "@<None>" or ping == "":
		ping = "<@"+str(client.application_id)+">"
	if message.author == client.user:
		return #if msg was made by the bot
	
	#INFO COMMAND
	if message.content.lower() == ping:
		await message.channel.send('Hello, <@'+str(message.author.id)+'>! \nIf you want to ask me what i can do, just say "@me, what can you do?"')
	
	#HELP COMMAND
	if message.content.lower() == ping+", what can you do?":
		#MESSAGE SPLIT INTO ARRAY
		msg = [
			"Hello, <@"+str(message.author.id)+">!",
			"I can do:",
			"1. Make a joke with @me, tell me a joke!",
			"And at some point, i can:",
			"2. Help you learn your language, with @me, open translate-it!",
			"3. Do smalltalk with you. For more info, say: @me, smalltalk info!"
		]
		"""
			OLD, UNPERFORMANT CODE
		msgform = ""
		for line in msg:
			msgform = msgform + line + "\n"
		"""
		await message.channel.send("\n".join(msg))
	
	#Joke Command
	print(message.jump_url)
	if sub("/!|\?|\.|,|\"|\'|:|;|\+|-|_|#|\\|\||\*|&/gm",
	"",
	message.content.lower()).startswith(ping+" tell me a joke"):
		j = joke.joke()
		#id = j["id"]
		#type = j["type"]
		setup = j["setup"]
		punchline = j["punchline"]
		async with message.channel.typing():   
			await asyncio.sleep(10)
		
		await message.channel.send(setup)
		
		async with message.channel.typing():
			await asyncio.sleep(5)
		
		await message.channel.send(punchline)

client.run('TOKEN')
ping = "@<"+str(client.application_id)+">"