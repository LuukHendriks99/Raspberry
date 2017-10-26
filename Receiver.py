# Save as server.py
# Message Receiver
import RPi.GPIO as GPIO
from socket import *
host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
print ("Checking for break-ins...")
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
while True:
    (data, addr) = UDPSock.recvfrom(buf)
    signal = data.decode('UTF-8')
    if signal == "True":
        GPIO.output(18, GPIO.HIGH)