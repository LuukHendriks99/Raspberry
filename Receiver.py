# Save as server.py
# Message Receiver
import RPi.GPIO as GPIO
from socket import *
import select
import time
client1 = "192.168.42.1"
self = ""
port = 13000
buf = 1024
receive_addr = (self, port)
send_addr = (client1, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(receive_addr)
print ("Checking for break-ins...")
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #knopje rechts
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #knopje links

connection_counter = 0
both_buttons = 0
inbraak = False

while True:
    data = bytes("connected", 'UTF-8')
    UDPSock.sendto(data, send_addr)
    if connection_counter == 5:
        GPIO.output(18, GPIO.HIGH)
        connection_counter = 0
    readers, _, _ = select.select([UDPSock], [], [], 0.1)
    time.sleep(0.1)
    for reader in readers:
        data = reader.recv(buf)
        signal = data.decode('UTF-8')
        if signal == "True":
            GPIO.output(18, GPIO.HIGH)
            inbraak = True
        if signal == "connected" and inbraak == False:
            connection_counter = 0
            GPIO.output(18, GPIO.LOW)
            continue
    if GPIO.input(23) and GPIO.input(24):
        both_buttons += 1
    else:
        both_buttons = 0
    if both_buttons == 50:
        data = bytes("Reset", 'UTF-8')
        UDPSock.sendto(data, send_addr)
        GPIO.output(18, GPIO.LOW)
        inbraak = False
    connection_counter += 1