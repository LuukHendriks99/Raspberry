# Save as client.py
# Message Sender
import os
from socket import *
host = "192.168.42.2" # set to IP address of target computer
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
    tekst = input("Hier moet tekst: ")
    data = bytes(tekst, 'UTF-8')
    UDPSock.sendto(data, addr)
    if tekst == "exit":
        print("Einde")
        break
UDPSock.close()
os._exit(0)