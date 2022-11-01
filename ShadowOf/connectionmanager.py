import asyncio
import threading
import socket
import mysql.connector
import nextcord
import connectedclient



class ConnectionManager:
    def __init__(self,
                 serverval,
                 port,
                 header = 1024,
                 format = "utf-8",
                 disconnectmessage = "#DISCONNECT#",
                 dbcursor : mysql.connector.connection_cext.CMySQLCursorBuffered = None,
                 dbhandler = None,
                 dcchannel = None,
                 dcclientloop = None,
                 dcclient = None
                 ):
        self.server : socket.socket
        self.serverval = serverval
        self.port = port
        self.MainServerThread : threading.Thread
        self.buffersize = header
        self.format = format
        self.disconnectmessage = disconnectmessage
        self.listofconnections : list = list()
        self.connection = True
        self.dbcursor = dbcursor
        self.dbhandler = dbhandler
        self.channel : nextcord.TextChannel = dcchannel
        self.dcclientloop : asyncio.AbstractEventLoop = dcclientloop
        self.dcclient = dcclient
        self.startsocket()


    def sendallclients(self,msg : str):
        for item in self.listofconnections:
            if item.connected:
                item.send(msg)


    async def removedroppedconnections(self):
        while True:
            for item in self.listofconnections:
                if not item.connected:
                    self.listofconnections.remove(item)
            await asyncio.sleep(120.0)


    def startsocket(self):
        port = self.port
        serverval = self.serverval
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((serverval, port))
        self.MainServerThread = threading.Thread(target=self.start)
        self.MainServerThread.daemon = True
        self.MainServerThread.start()
        #asyncio.run_coroutine_threadsafe(coro=self.channel.send("Shadow of Defeat Game Server is Online"), loop=self.dcclientloop)





        print(f"Server is Online at {self.serverval}:{port}")




    def start(self):
        self.server.listen()
        while self.connection:
            conn, addr = self.server.accept()
            self.listofconnections.append(connectedclient.client(address=addr,
                                                                 connection=conn,
                                                                 format=self.format,
                                                                 disconnectmessage=self.disconnectmessage,
                                                                 timeout=360,
                                                                 buffersize=self.buffersize,
                                                                 dbcursor=self.dbcursor,
                                                                 dcchannel=self.channel,
                                                                 dcclientloop=self.dcclientloop,
                                                                 dbhandler=self.dbhandler,
                                                                 dcclient=self.dcclient)
                                          )


    def ceaseallclientactivities(self):
        for item in self.listofconnections:
            item.disconnect()

    def onlineplayercount(self):
        i = 0
        for item in self.listofconnections:
            if item.intentmanager.loggedin:
                i+=1

        return i

    def getallconnections(self):
        t = f""""""
        i = 0
        for item in self.listofconnections:

            t+= f"""{item.show()} {i+1} 

"""
            i+=1
        if i > 0:
            return t
        else:
            return False

    def end(self):

        self.ceaseallclientactivities()
        self.server.close()
        self.connection = False
        self.MainServerThread.join()
        print("Shutting server down.")




