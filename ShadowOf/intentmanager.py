import asyncio
import hashlib
import json
import mysql.connector
import nextcord.utils
from nextcord import Embed
from nextcord.ext import commands
from nextcord.ext.commands import Bot


import visual


class intentmanager():
    def __init__(self,dcclient : Bot ,maineventloop,databaseconnector : mysql.connector.MySQLConnection,databasecursor : mysql.connector.connection_cext.CMySQLCursorBufferedDict,defaultdisconnect : str):
        self.maineventloop : asyncio.AbstractEventLoop= maineventloop
        self.db = databaseconnector
        self.cursor = databasecursor
        self.defaultdisconnect = defaultdisconnect
        self.dcclient = dcclient
        self.loggedin = False
        self.loggeduserid: str
        self.loggeduserpass: str
        self.databaseid = -1

#GET&0.01 Chay-Gow&STATE&@{}

    def getgamestate(self):
        pass


    def intention(self,package : str):
        if package == self.defaultdisconnect:
            return self.defaultdisconnect
        if package == "PING#1":
            return "ACCEPTED#1"
        formatted :list = package.split(sep="&")
        try:
            header = formatted[0]
            versiondetails = formatted[1]
        except:
            return "DROP#1"
        version = self.BringValue("Global/config.json",Uvariable="gameversion")
        if version != versiondetails:
            return self.defaultdisconnect

        match(header):
            case "GET":
                return
            case "LOGIN":
                return
            case "CREATEACCOUNT":
                #CREATEACCOUNT&version&@{"username" : username,"password" : passwordunhashed, "discordid" : discordid}
                print(formatted[2])
                try:
                    userinfo: dict = self.jsonize(formatted[2])
                    result: str = self.createaccounthandler(userinfo)
                    return result
                except:
                    return "FAIL#-1"
            case "SET":
                return
            case "PING":
                return "ACCEPTED#1"
            case _:
                return "DROP#1"

    def BringValue(self,address, Uvariable):
        f = open(address, "r")
        variable = json.load(f)
        print(f"Loaded the {address}, {Uvariable}:{variable[Uvariable]}")
        f.close()
        return variable[Uvariable]

    def createaccounthandler(self, userinfo : dict):
        self.cursor.execute(f"SELECT count(userid) as 'useramount' FROM user WHERE username='{userinfo['username']}'")
        result = self.cursor.fetchone()["useramount"]
        if result != 0:
            return "FAIL#-1"
        self.cursor.execute(f"SELECT count(userid) as 'useramount' FROM user WHERE discordid='{userinfo['discordid']}'")
        result = self.cursor.fetchone()["useramount"]
        if result != 0:
            return "FAIL#-2"
        view = visual.RegisterButtons(dbcursor=self.cursor,dbhandler=self.db,userinfo=userinfo,
                                      dcloop=self.maineventloop)

        try:
            user = nextcord.utils.get(self.dcclient.users,id=int(userinfo["discordid"]))
        except:
            return "FAIL#-3"
        vembed = Embed(title="Create a Shadow of Defeat Account",description=f"{userinfo['username']} You are at the final step of making an account.",colour=0x00FF00)
        try:
            asyncio.run_coroutine_threadsafe(coro=user.send(embed=vembed,view=view),loop=self.maineventloop)
            return "SUCCESS#1"
        except:
            return "FAIL#-3"

    def jsonize(self,text : str):
        #text = text.replace("@","",1)
        result = json.loads(text)
        return result

    def hashpassword(self,unhashed):
        text = hashlib.sha256(unhashed)
        return text

