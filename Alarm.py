import RPi.GPIO as GPIO
import time
import pygame
from socket import *

host = "192.168.42.2"
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)

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
while True:
    if first2 == True:
        print("uit")
        first2 = False
    GPIO.output(18, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    if GPIO.input(25) and GPIO.input(16):
        both +=1
    else:
        both = 0
    if both == 100:
        first = True
        both = 0
        both3 = 0
        while True:
            GPIO.output(18, GPIO.HIGH)
            GPIO.output(23, GPIO.LOW)
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
                GPIO.output(23, GPIO.HIGH)
                counter = 0
                while counter < 100:
                    time.sleep(0.1)
                    if GPIO.input(16):
                        GPIO.output(18, GPIO.HIGH)
                        GPIO.output(23, GPIO.LOW)
                        pygame.mixer.music.stop()
                        break
                    counter += 1
                if counter == 100:
                    data = bytes("True", 'UTF-8')
                    UDPSock.sendto(data, addr)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("match0.wav")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    both2 = 0
                    while True:
                        if GPIO.input(25) and GPIO.input(16):
                            both2 += 1
                        else:
                            both2 = 0
                        if both2 == 100:
                            both2 = 0
                            first = True
                            break
                        time.sleep(0.1)
            if both3 == 100:
                both3 = 0
                first2 = True
                break
            time.sleep(0.1)

    time.sleep(0.1)