import socket
import threading
import time

from cryptography.fernet import Fernet

header = 64
format = "utf-8"
disconnectmessage = "#DISCONNECT#"
serverval = "127.0.0.1"
port = 5050
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((serverval, port))
print("Connecting uwu")


def send(data: str):
    message = data.encode("utf-8")
    #cipher = BringValue(address="Global/config.json", Uvariable="packagecipher")
    cipher = "xlabPMzN6Mveph05zgDZOxaYD9gCM7rYRWSP-wLiXfI="
    #f = Fernet(cipher)
    #message = f.encrypt(message)
    socket.send(message)

def pingeverynowandthen():
    while True:
        send("PING#1")
        time.sleep(50)

def BringValue(address, Uvariable):
    f = open(address, "r")
    #variable = json.load(f)
    #print(f"Loaded the {address}, {Uvariable}:{variable[Uvariable]}")
    f.close()
    return #variable[Uvariable]

#threading.Thread(target=pingeverynowandthen())





while True:
    msg = input("Input: ")
    send(msg)
    if msg == disconnectmessage:
        socket.close()
        break

