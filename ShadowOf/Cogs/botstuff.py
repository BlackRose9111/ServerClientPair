from datetime import datetime

import nextcord
from nextcord import Interaction, Embed, SlashOption, Member, User
from nextcord.ext import commands
import connectionmanager
import main
import pytz



class Botstuff(commands.Cog):
    def __init__(self, client):
        self.client = client


    # main.dbCursor.execute("SELECT * FROM user WHERE discord_id = %s",(text,))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=nextcord.Game("Server is online"))
        print("Loaded Bottstuff")


    @commands.command()
    async def sendmessagetoallclients(self,ctx,message):
        main.server.sendallclients(message)
        await ctx.send(f"Sending {message} to all clients")


    @commands.command()
    async def counttheconnections(self,ctx):
        await ctx.send(f"{len(main.server.listofconnections)} on server at {main.server.serverval}:{main.server.port}")

    @commands.command()
    async def listallconnections(self,ctx):

        t = main.server.getallconnections()
        if not t:
            t = "No connections"

        vembed = Embed(title="Connection List", description=t, colour=0x0000FF)
        await ctx.send(embed = vembed)

    @commands.command()
    async def restarttheserver(self,ctx):
        await ctx.send("Restarting the server. All connections will be ceased.")
        main.restartservers()
        await ctx.send("Finished restarting.")

    @commands.command()
    async def gamestatus(self,ctx):
        serverstatus = main.server.connection
        dbstatus = main.db.is_connected()
        gameversion = main.BringValue(address=main.globalVariable,Uvariable="gameversion")
        connectedplayercount = main.server.onlineplayercount()
        elapsed = main.timeformatter(main.elapsedTime)

        t = f""""""
        if serverstatus:
            t+=f"""**Server Status:** Online

"""
        else:
            t += f"""**Server Status:** Offline

"""
        if dbstatus:
            t += f"""**Database Status:** Online

    """
        else:
            t += f"""**Database Status:** Offline

"""
        t+= f"""**Game Version:** \"{gameversion}\"
        
        **Online Player Count:** {connectedplayercount}
        
        **Elapsed Time:** {elapsed}
"""
        vembed = Embed(title="Server Stats",description=t,colour=0xFF0000)
        vembed.set_footer(text="Coming soon",icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed = vembed)



def setup(client):
    client.add_cog(Botstuff(client))
