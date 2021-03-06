import RPi.GPIO as GPIO
import time
import pygame
from socket import *

host = "192.168.42.2"
self = ""
port = 13000
buf = 1024
addr = (host, port)
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
first2 = True

def check_message():
    if UDPSock.recv != None:
        (data, addr) = UDPSock.recvfrom(buf)
        signal = data.decode('UTF-8')
        if signal == "Reset":
            return True
        else:
            return False
    else:
        return False

while True:
    if first2 == True:
        print("uit")
        first2 = False
    GPIO.output(18, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    orange = False
    pygame.mixer.music.stop()
    reset = False
    if GPIO.input(25) and GPIO.input(16):
        both +=1
    else:
        both = 0
    if both == 50:
        first = True
        both = 0
        both3 = 0
        while True:
            both2 = 0
            GPIO.output(18, GPIO.HIGH)
            GPIO.output(23, GPIO.LOW)
            orange = False
            pygame.mixer.music.stop()
            if first == True:
                print("aan")
                time.sleep(5)
                first = False
            if GPIO.input(25) and GPIO.input(16):
                both3 += 1
            elif GPIO.input(25) == True:
                both3 = 0
                pygame.mixer.music.stop()
                pygame.mixer.music.load("beep1.ogg")
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play(-1)
                GPIO.output(18, GPIO.LOW)
                counter = 0
                while counter < 100:
                    #reset = check_message()
                    #if reset == True:
                        #break
                    time.sleep(0.1)
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
                if counter == 100:
                    GPIO.output(23, GPIO.HIGH)
                    orange = True
                    data = bytes("True", 'UTF-8')
                    UDPSock.sendto(data, addr)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("match0.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    both2 = 0
                    while True:
                        #reset = check_message()
                        #if reset == True:
                            #first = True
                            #break
                        if GPIO.input(25) and GPIO.input(16):
                            both2 += 1
                        else:
                            both2 = 0
                        if both2 == 50:
                            first = True
                            pygame.mixer.music.stop()
                            break
                        time.sleep(0.1)
            if both3 == 50:
                both3 = 0
                first2 = True
                break
            time.sleep(0.1)

    time.sleep(0.1)