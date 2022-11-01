import datetime
import threading
import nextcord
import pytz
from nextcord.ext import commands,tasks
import os
import json
import mysql.connector
import connectionmanager
import sys



client = commands.Bot(command_prefix="?",intents=nextcord.Intents.all(),case_insensitive=True,strip_after_prefix=True)
reminder = "Global/reminder.json"
remindChannel = "Global/channel.json"
remindContext = "Global/context.json"
timeStamp = "Global/timestamp.json"
globalVariable = "Global/config.json"
databaseconfig = "Global/db.json"
timezone = pytz.timezone("Etc/GMT+9")
turn1 = datetime.time(tzinfo=timezone,hour=12)
turn2 = datetime.time(tzinfo=timezone,hour=0)
databaseInfo = {}
elapsedTime = 0.0
db : mysql.connector.connection_cext.CMySQLConnection
dbCursor : mysql.connector.connection_cext.CMySQLCursorBufferedDict
server : connectionmanager.ConnectionManager



@client.event
async def on_ready():
    print("Bot is Online")
    EnterCache(address=reminder, collection={}, debug=False)
    EnterCache(address=timeStamp, collection={}, debug=False)
    EnterCache(address=remindChannel, collection={}, debug=False)
    EnterCache(address=remindContext, collection={}, debug=False)
    global databaseInfo
    databaseInfo = LoadCache(databaseconfig,debug=False)
    connectodb()
    global server
    dcchannel = nextcord.utils.get(client.get_all_channels(),id=561541369877757952)
    serverval = BringValue(address=globalVariable,Uvariable="server")
    port = BringValue(address=globalVariable,Uvariable="port")
    server = connectionmanager.ConnectionManager(serverval=serverval,port=port,header=1024,format="utf-8",dbcursor=dbCursor,dbhandler=db,dcchannel=dcchannel,dcclient=client,dcclientloop = client.loop)
    ParallelLoop.start()
    cleartheremovedconnections.start()
    turntick.start()



def connectodb():
    global db
    global dbCursor
    global databaseInfo
    dbinfo = databaseInfo
    db = mysql.connector.connect(host = dbinfo["host"],user = dbinfo["user"],passwd = dbinfo["password"],database = dbinfo["database"])
    db.autocommit = True
    dbCursor = db.cursor(buffered=True,dictionary=True)
    print(f"Connected to {db.database}")
    print(type(dbCursor))







def findmember(id : int):
    member = None
    for s in client.guilds:
        for m in s.members:
            if id == m.id:
                member = m
                break
    return member

@client.command(hidden = True)
async def flushremind(ctx):
    EnterCache(address=reminder,collection={})
    await ctx.send("Remind flushed")

async def remind():
    remindCache = LoadCache(reminder,False)
    newCache = {}
    #print(elapsedTime)
    if len(remindCache) > 0:
        for id in remindCache:

            if remindCache[id] <= elapsedTime:
                length = BringValue(address=timeStamp,Uvariable=id)
                context = BringValue(address=remindContext,Uvariable=id)
                channel = BringValue(address=remindChannel,Uvariable=id)
                await client.get_channel(channel).send(f"Your reminder of \"{context}\" {timeformatter(length)}({length}s) is done <@{id}>.")
            else:
                newCache[id] = remindCache[id]
        EnterCache(address=reminder,collection=newCache,debug=False)


@tasks.loop(minutes=15)
async def cleartheremovedconnections():
    if server.connection:
        for item in server.listofconnections:
            if not item.connected:
                server.listofconnections.remove(item)
                print(f"Removed {item.address}")

def BringValue(address, Uvariable):
    f = open(address, "r")
    variable = json.load(f)
    print(f"Loaded the {address}, {Uvariable}:{variable[Uvariable]}")
    f.close()
    return variable[Uvariable]


@tasks.loop(time=[turn1,turn2])
async def turntick():
    turn = BringValue(address=globalVariable,Uvariable="currentturn")
    newturn = turn + 1
    await nextcord.utils.get(client.get_all_channels(),id=561541369877757952).send(f"Turn {turn} has ended and {newturn} has begun")
    WriteValue(address=globalVariable,Uvariable="currentturn",Value=newturn)

def WriteValue(address, Uvariable, Value):
    a_file = open(address, "r")
    json_object = json.load(a_file)
    a_file.close()
    print(f"Loaded the {address}")
    json_object[Uvariable] = Value
    a_file = open(address, "w")
    print(f"Wrote {Uvariable} : {Value} at {address}")
    json.dump(json_object, a_file, indent=5)
    a_file.close()


def AddValue(address, Uvariable, Value):
    file = open(address, "r")
    variable = json.load(file)
    variable[Uvariable] = Value
    file.close()
    file = open(address, "w")
    json.dump(variable, file, indent=5)
    file.close()
    print(f"Adding new entry {Uvariable} : {Value} to {address} ")


def LoadCache(address,debug = True):
    file = open(address, "r")
    variable = json.load(file)
    file.close()
    if debug:
        print(f"Loaded {variable} to ram from {address}")
    return variable


def EnterCache(address, collection,debug = True):
    file = open(address, "w")
    json.dump(collection, file, indent=5)
    file.close()
    if debug:
        print(f"Loaded the {collection} in ram to the disk.")


def EraseDefaults(address, Uvariable):
    currentCache = LoadCache(address)
    default = BringValue(address=globalVariable, Uvariable=Uvariable)
    newCache = {}
    totalRemoved = 0
    for x in currentCache:
        if currentCache[x] != default:
            newCache[x] = currentCache[x]
        else:
            totalRemoved += 1
    EnterCache(address=address, collection=newCache)
    print(f"{totalRemoved} entries removed from {address}")

@tasks.loop(seconds=1)
async def ParallelLoop():
    IncrementTime()
    try:
        await remind()
    except:
       print("Remind error")





def IncrementTime():
    global elapsedTime
    elapsedTime+=1


@client.command(hidden=True)
async def shutdown(ctx):
    await ctx.send("Bot is shutting down.")
    await client.close()
    server.end()
    sys.exit()


def externalUnload(extension):
    client.unload_extension(extension)
    print(f"unloaded {extension} ")


def timeformatter(entry: float):
    text = "Days"
    time = int(round(entry/ (24*3600),1))  # day
    if time == 0:
        time = int(round(entry/3600,1))
        text = "Hours"
    if time == 0:
        time = int(round(entry/60,1))  # minutes
        text = "Minutes"
    if time == 0:
        time = entry  # second
        text = "Seconds"
    text = f"{time} {text}"

    return text


@client.command(hidden=True)
async def ping(ctx):
    await ctx.send(f"Bot Latency = {round(client.latency, 2)}ms")
    print(f"Bot Latency = {round(client.latency, 2)}ms")


@client.command(hidden=True)
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    print(f"loaded {extension} ")
    await ctx.send(f"loaded {extension}")


@client.command(hidden=True)
async def reload(ctx, extension):
    await unload(ctx, extension)
    await load(ctx, extension)



@client.command(hidden=True)
async def flushtoken(ctx):
    EnterCache(address="Token.json",collection={})



@client.command(hidden=True)
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    print(f"unloaded {extension} ")
    await ctx.send(f"unloaded {extension}")


def leaderboard(address, number=10, order=True,symbol = ""):
    all = LoadCache(address=address)
    a = sorted(all, key=all.get, reverse=order)
    length = len(a)
    if length > number:
        length = number
    number = 1
    t = """"""
    for x in range(length):
        t = t + f"""{number:,}. <@{a[number - 1]}> - {all[a[number - 1]]:,} {symbol}

"""
        number = number + 1
    if t is None:
        t = "No data"

    return t


def getTotal(address):
    cache = LoadCache(address)
    total = 0
    for key in cache:
        total += cache[key]

    return total

def restartservers():
    dcchannel = nextcord.utils.get(client.get_all_channels(),id=561541369877757952)
    global server
    db.close()
    connectodb()
    server.end()
    serverval = BringValue(address=globalVariable, Uvariable="server")
    port = BringValue(address=globalVariable, Uvariable="port")
    server = connectionmanager.ConnectionManager(serverval=serverval, port=port, header=64, format="utf-8",
                                                 dbcursor=dbCursor, dbhandler=db, dcchannel=dcchannel,
                                                 dcclient=client.loop)


def inspectVariable(author, uvariable, address):
    try:
        value = BringValue(address=address, Uvariable=f"{author}")
    except:
        value = BringValue(address=globalVariable, Uvariable=uvariable)
        AddValue(address=address, Uvariable=f"{author}", Value=value)


def getrank(address, author):
    rank = 0
    cache = LoadCache(address)
    rankSuffix = ["th", "st", "nd", "rd"]
    s = sorted(cache, key=cache.get, reverse=True)

    for x in range(len(s)):

        if author == s[x]:
            rank += 1
            break
        rank += 1

    if rank % 10 in [1, 2, 3] and rank not in [11, 12, 13]:
        t = f"{rank}{rankSuffix[rank % 10]}"
    else:
        t = f"{rank}{rankSuffix[0]}"
    return t

def attempt(s):
    client.load_extension(s)

for filename in os.listdir('./Cogs'):
    if filename.endswith(".py"):
        attempt(f"Cogs.{filename[:-3]}")
        print(f"Loaded {filename[:-3]}")
try:
    token = BringValue("Token.json", "Token")
except:
    token = ""

if token == "":
    print("Token in the Token.json file is missing, please enter the bot token by hand:")
    token = input()
    WriteValue("Token.json", "Token", token)


client.run(token)

print(threading.active_count())
