import mysql.connector




def login(dbhandler :  mysql.connector.connection_cext.CMySQLConnection,dbhandlercursor : mysql.connector.connection_cext.CMySQLCursorBuffered ,username,userpass,userid):
    dbhandler.commit()
    dbhandlercursor.execute(f"SELECT count(id), id FROM `userinfo` WHERE username = {username} AND password = {userpass} AND discord_id = {userid}")
    result = dbhandlercursor.fetchone()[0]
    print(result)
    if result == 0:
        return -1
    else:
        return result[1]




def makeaccount(dbhandler :  mysql.connector.connection_cext.CMySQLConnection,dbhandlercursor : mysql.connector.connection_cext.CMySQLCursorBufferedDict ,userinfo):
    try:
        dbhandlercursor.execute(f"INSERT INTO user (username,password,discordid) VALUES ('{userinfo['username']}','{userinfo['password']}','{userinfo['discordid']}')")
        return True
    except:
        return False



