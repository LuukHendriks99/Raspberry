import RPi.GPIO as GPIO
import time
import pygame
from socket import *
import select

server = "192.168.42.2"
self = ""
port = 13000
buf = 1024
addr = (server, port)
receive_addr = (self, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(receive_addr)

pygame.mixer.init()
pygame.mixer.music.stop()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

both = 0
elevator = 0
connected = 0

def check_message():
    readers,_,_ = select.select([UDPSock],[],[],0.1)
    for reader in readers:
        data = reader.recv(buf)
        signal = data.decode('UTF-8')
        if signal == "Reset":
            return True
        elif signal == "connected":
            global connected
            connected = 0
        else:
            return False
    return False

def connected_function():
    data = bytes("connected", 'UTF-8')
    UDPSock.sendto(data, addr)

while True:
    connected += 1
    reset = check_message()
    connected_function()
    GPIO.output(18, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    orange = False
    pygame.mixer.music.stop()
    reset = False
    if GPIO.input(25) and GPIO.input(16):
        both +=1
    else:
        both = 0
    if both == 50 or connected > 5:
        first = True
        both = 0
        both3 = 0
        while True:
            connected += 1
            reset = check_message()
            connected_function()
            both2 = 0
            GPIO.output(18, GPIO.HIGH)
            GPIO.output(23, GPIO.LOW)
            orange = False
            pygame.mixer.music.stop()

            if first == True and connected < 5:
                elevator = 0
                pygame.mixer.music.load("elevator.wav")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
                while elevator < 100:
                    connected += 1
                    reset = check_message()
                    connected_function()
                    time.sleep(0.1)
                    first = False
                    elevator += 1
                pygame.mixer.music.stop()
            if GPIO.input(25) and GPIO.input(16):
                both3 += 1
            elif GPIO.input(25) == True or connected > 5:
                both3 = 0
                pygame.mixer.music.stop()
                pygame.mixer.music.load("beep1.ogg")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                GPIO.output(18, GPIO.LOW)
                counter = 0
                while counter < 100 and connected < 5:
                    connected += 1
                    reset = check_message()
                    connected_function()
                    reset = check_message()
                    if reset == True:
                        break
                    if counter % 5 == 0:
                        if orange == False:
                            GPIO.output(23, GPIO.HIGH)
                            orange = True
                        elif orange == True:
                            GPIO.output(23, GPIO.LOW)
                            orange = False
                    if GPIO.input(16):
                        break
                    counter += 1
                if counter == 100 or connected > 5:
                    GPIO.output(23, GPIO.HIGH)
                    orange = True
                    data = bytes("True", 'UTF-8')
                    UDPSock.sendto(data, addr)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("alarm.wav")
                    pygame.mixer.music.set_volume(0.1)
                    pygame.mixer.music.play(-1)
                    both2 = 0
                    while True:
                        connected += 1
                        connected_function()
                        reset = check_message()
                        if reset == True:
                            first = True
                            break
                        if GPIO.input(25) and GPIO.input(16):
                            both2 += 1
                        else:
                            both2 = 0
                        if both2 == 50:
                            first = True
                            pygame.mixer.music.stop()
                            break
            if both3 == 50:
                both3 = 0
                break
            time.sleep(0.1)

    time.sleep(0.1)