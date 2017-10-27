import RPi.GPIO as GPIO
import time
import pygame
from socket import *
import select

# For connections between pi's
server = "192.168.42.2"
self = ""
port = 13000
buf = 1024
addr = (server, port)
receive_addr = (self, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(receive_addr)

# Starts pygame.mixer for music/sounds
pygame.mixer.init()
pygame.mixer.music.stop()

# Activates GPIO ports for LED and switches
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Some vars
both = 0
elevator = 0
connected = 0
reset = False


# Checks if there are incoming messages
def check_message():
    readers, _, _ = select.select([UDPSock], [], [], 0.1)
    time.sleep(0.1)
    for reader in readers:
        data = reader.recv(buf)
        signal = data.decode('UTF-8')
        if signal == "Reset":  # Resets alarm
            return True
        elif signal == "connected":  # Checks connection between pi's
            global connected
            connected = 0
        else:
            return False
    return False


# Sends message to confirm connection
def connected_function():
    data = bytes("connected", 'UTF-8')
    UDPSock.sendto(data, addr)


# Main while loop which is active if the alarm is OFF
while True:
    connected += 1
    reset = check_message()
    connected_function()
    GPIO.output(18, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    orange = False
    pygame.mixer.music.stop()
    reset = False
    if GPIO.input(25) and GPIO.input(16):  # Checks if both buttons are pressed
        both += 1 # Increases counter by 1
    else:  # Resets counter if buttons are released
        both = 0
    if both == 50 or connected > 5:  # If buttons are pressed for 5 seconds continuously or when connection is broken for more than 0.5 seconds alarm turns ON
        first = True
        both = 0
        both3 = 0
        while True:  # While loop which is active if the alarm is ON
            connected += 1
            reset = check_message()
            connected_function()
            both2 = 0
            GPIO.output(18, GPIO.HIGH)
            GPIO.output(23, GPIO.LOW)
            orange = False
            pygame.mixer.music.stop()

            if first == True and connected < 5:  # If this is the first loop and there is a connection, elevator music is played
                elevator = 0
                pygame.mixer.music.load("elevator.wav")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
                while elevator < 100: #Plays music for 10 seconds
                    connected += 1
                    reset = check_message()   # Making sure there is still a connection while elevator music is playing
                    connected_function()
                    first = False
                    elevator += 1
                pygame.mixer.music.stop()
            if GPIO.input(25) and GPIO.input(16):  # Checks if both buttons are pressed
                both3 += 1  # Increases counter by 1
            elif GPIO.input(25) == True or connected > 5:  # Checks for break-ins or lost connection more than five seconds
                both3 = 0
                pygame.mixer.music.stop()
                pygame.mixer.music.load("beep1.ogg")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                GPIO.output(18, GPIO.LOW)
                counter = 0
                while counter < 100 and connected < 5:  # Loop which makes sure there's time to disable the alarm if you have a connection
                    connected += 1
                    connected_function()
                    reset = check_message()
                    if reset == True:  # Returns to the ON while loop when the server sends reset
                        break
                    if counter % 5 == 0:  # Flashing orange light
                        if orange == False:
                            GPIO.output(23, GPIO.HIGH)
                            orange = True
                        elif orange == True:
                            GPIO.output(23, GPIO.LOW)
                            orange = False
                    if GPIO.input(16):  # Checks if the alarm is disabled
                        break
                    counter += 1
                if counter == 100 or connected > 5:  # Makes the alarm go off after 10 seconds or if there's no connection
                    GPIO.output(23, GPIO.HIGH)
                    orange = True
                    data = bytes("True", 'UTF-8')
                    UDPSock.sendto(data, addr)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("alarm.wav")
                    pygame.mixer.music.set_volume(0.1)
                    pygame.mixer.music.play(-1)
                    both2 = 0
                    while True:  # While loop which is active if the alarm is going off
                        connected += 1
                        connected_function()
                        reset = check_message()
                        if reset == True:  # Returns to the ON while loop when the server sends reset
                            first = True
                            break
                        if GPIO.input(25) and GPIO.input(16):  # Checks if both buttons are pressed
                            both2 += 1 # Increases counter by 1
                        else:  # Resets counter if buttons are released
                            both2 = 0
                        if both2 == 50:  # Returns to ON loop if buttons are pressed for 5 seconds continuously
                            first = True
                            pygame.mixer.music.stop()
                            break
            else:  # Resets counter if buttons are released
                both3 = 0
            if both3 == 50:  # Returns to OFF loop if buttons are pressed for 5 seconds continuously
                both3 = 0
                break