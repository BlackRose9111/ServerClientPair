import asyncio

import nextcord
from nextcord.ext import commands
from nextcord import ButtonStyle, Interaction, Embed, utils
import hashlib
import game


class RegisterButtons(nextcord.ui.View):
    def __init__(self,userinfo,dbhandler,dbcursor,dcloop):
        super().__init__(timeout=600,loopy=dcloop)
        self.userinfo = userinfo
        self.dbhandler = dbhandler
        self.dbcursor = dbcursor
        self.dcloop = dcloop

    @nextcord.ui.button(label="Register",style=ButtonStyle.green)
    async def register(self, button : nextcord.Button,interaction : Interaction):

        if interaction.user.id == self.userinfo["discordid"]:
            self.userinfo['password'] = self.hashpassword(self.userinfo['password'])
            condition = game.makeaccount(dbhandler=self.dbhandler,dbhandlercursor=self.dbcursor,userinfo=self.userinfo)
            if condition:
                asyncio.run_coroutine_threadsafe(coro=interaction.send("Registered. You can log in now."),loop=self.dcloop)
            else:
                asyncio.run_coroutine_threadsafe(coro=interaction.send("Registration failed, this username or discord id may be taken."),
                                                 loop=self.dcloop)
            for a in self.children:
                a.disabled = True
            asyncio.run_coroutine_threadsafe(
                coro=interaction.edit(view=self),
                loop=self.dcloop)

            self.stop()


    @nextcord.ui.button(label="Cancel",style=ButtonStyle.red)
    async def cancel(self, button : nextcord.Button,interaction : Interaction):

        if interaction.user.id == self.userinfo["discordid"]:
            for child in self.children:
                child.disabled = True
            asyncio.run_coroutine_threadsafe(
                coro=interaction.edit(view=self),
                loop=self.dcloop)
            self.stop()


    def hashpassword(self,text):
        text = hashlib.sha256(text)
        return text


