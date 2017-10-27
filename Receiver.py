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

while True: #Main program loop
    data = bytes("connected", 'UTF-8')
    UDPSock.sendto(data, send_addr)
    if connection_counter == 5: #Checks if the connection has been lost for five seconds
        GPIO.output(18, GPIO.HIGH)
        connection_counter = 0
    readers, _, _ = select.select([UDPSock], [], [], 0.1) #Checks if there are any messages waiting in UDPSock and if so puts UDPSock in a the list readers
    time.sleep(0.1)
    for reader in readers: # Goes through list readers which will be empty if there are no messages
        data = reader.recv(buf)
        signal = data.decode('UTF-8')
        if signal == "True": #Check is the received messages says True
            GPIO.output(18, GPIO.HIGH)
            inbraak = True
        if signal == "connected" and inbraak == False: # Checks if the received message is connected and if there is no inbraak
            connection_counter = 0
            GPIO.output(18, GPIO.LOW)
            continue
    if GPIO.input(23) and GPIO.input(24): # Checks if both buttons are pressed down
        both_buttons += 1 # Increases counter by 1
    else: # Resets counter if buttons are released
        both_buttons = 0
    if both_buttons == 50: # Sends a message to reset the client if both buttons have been pressed down for five seconds
        data = bytes("Reset", 'UTF-8')
        UDPSock.sendto(data, send_addr)
        GPIO.output(18, GPIO.LOW)
        inbraak = False
    connection_counter += 1