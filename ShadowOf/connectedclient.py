import json
import socket
import concurrent.futures
import asyncio
import threading
import mysql.connector
import nextcord.channel
from cryptography.fernet import Fernet

import game
import intentmanager

import visual


class client:
    def __init__(self, address: str,
                 connection: socket.socket,
                 format,
                 disconnectmessage,
                 timeout=60,
                 dbhandler=None,
                 dbcursor: mysql.connector.connection_cext.CMySQLCursorBuffered = None,
                 dcchannel=None,
                 dcclientloop=None,
                 dcclient = None,
                 buffersize = 1024
                 ):

        self.address = address
        self.connection: socket.socket = connection
        self.connected = True
        self.buffersize = buffersize
        self.format = format
        self.disconnectmessage = disconnectmessage
        self.connectiontimeout = timeout
        self.dcchannel: nextcord.channel.TextChannel = dcchannel
        self.dbhandler = dbhandler
        self.dbCursor: mysql.connector.connection_cext.CMySQLCursorBuffered = dbcursor
        self.asynced: asyncio.tasks
        self.dcclientloop = dcclientloop
        self.dcclient = dcclient
        self.thread: threading.Thread = threading.Thread(target=self.handleclient, daemon=True)
        self.thread.start()
        self.intentmanager : intentmanager.intentmanager = intentmanager.intentmanager(dcclient=dcclient,
                                                                                       maineventloop=dcclientloop,
                                                                                       databasecursor=self.dbCursor,
                                                                                       defaultdisconnect=self.disconnectmessage,
                                                                                       databaseconnector=self.dbhandler)






    def handleclient(self):
        print(f"New connection established {self.address}")
        while self.connected:
            try:
                self.connection.settimeout(self.connectiontimeout)
                msg = self.connection.recv(self.buffersize)
                print(msg)
                #cipher = self.BringValue(address="Global/config.json",Uvariable="packagecipher")
                #f = Fernet(cipher)
                #msg = f.decrypt(msg).decode()
                msg = msg.decode()
            except Exception as e:
                print(f"{e} error")
                self.disconnect()
                break
            print(f"{self.address} sent {msg}, {len(msg)}")
            if msg == self.disconnectmessage:
                print(f"{self.address} disconnected.")
                self.disconnect()
                break
            else:
                response = self.intentmanager.intention(package=msg)
                self.send(response)





    def intentmanagerdepcracated(self,package):
        messagesplit = package.split("#")
        intent = messagesplit[0]
        match (intent):
            case "PING":
                print("Received ping")
                self.send("ACCEPTED#1")
            case "REGISTER":
                if len(messagesplit) != 4:
                    self.send("DROP#-1")
                    print("Package dropped.")
                else:
                    userid = int(messagesplit[1])
                    userpass = messagesplit[2]
                    username = messagesplit[3]
                    #view = visual.RegisterButtons(,dbhandler=self.dbhandler, dbcursor=self.dbCursor,dcloop=self.dcclientloop)
                    user = self.findmember(id=userid)
                    vembed = nextcord.Embed(title="Registration",
                                            description=f"{username} to finish your registration, please confirm.",
                                            colour=0xFF0000)
                    asyncio.run_coroutine_threadsafe(coro=user.send("Test"), loop=self.dcclientloop)
                    #asyncio.run_coroutine_threadsafe(coro=user.send(embed=vembed, view=view), loop=self.dcclientloop)
            case _:
                print("Unrecognised package pattern, package dropped")
                print(package)
                self.send("DROP#1")




    def BringValue(self,address, Uvariable):
        f = open(address, "r")
        variable = json.load(f)
        print(f"Loaded the {address}, {Uvariable}:{variable[Uvariable]}")
        f.close()
        return variable[Uvariable]
    def send(self,data: str):
        message = data.encode(self.format)
        #cipher = self.BringValue(address="Global/config.json",Uvariable="packagecipher")
        #f = Fernet(cipher)
        #message = f.encrypt(message)
        self.connection.send(message)

        print(f"Sending {data} to {self.address}")
    def senddepracated(self, data : str):
        msg_length = str(len(data)).encode(self.format)
        message = data.encode(self.format)
        msg_length += b" " * (self.buffersize - len(msg_length))
        self.connection.send(msg_length)
        self.connection.send(message)


        print(f"Sending {data} to {self.address}")

    def disconnect(self):
        try:
            self.send(self.disconnectmessage)
        except:
            print("Disconnect Message could not be delivered.")
        self.connection.close()
        self.connected = False
        #self.thread.join()

    def findmember(self,id: int):
        member = None
        for s in self.dcclient.guilds:
            for m in s.members:
                if id == m.id:
                    member = m
                    break
        return member


    def show(self):
        str = f"{self.address} - {self.connected}"
        return str
