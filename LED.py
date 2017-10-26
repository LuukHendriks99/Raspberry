import RPi.GPIO as GPIO
import time
import tkinter

top = tkinter.Tk()

frame1 = tkinter.Frame(top, width=300, height=300)

frame1.pack(fill=None)


def helloCallBack():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(18, GPIO.LOW)


b = tkinter.Button(frame1, text="LED aan", command=helloCallBack)
b.pack(pady=20, padx=20)
top.mainloop()