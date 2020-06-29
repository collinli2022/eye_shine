import RPi.GPIO as GPIO
import time

class servoControl:
    def __init__(self, pinNum):
        GPIO.setmode(GPIO.BOARD) # <-- GPIO PIN BASED ON BOARD
        GPIO.setup(pinNum, GPIO.OUT)
        self.__servo = GPIO.PWM(pinNum, 50) # GPIO pinNum for PWM with 50Hz
        self.__servo.start(2.5) # angle 0
        self.__angle = 0

    def cal(self, deg1):
        deg = abs(float(deg1))
        dc = 0.056*deg + 2.5
        return dc

    def angle(self, deg):
        self.__angle = deg
        self.__servo.ChangeDutyCycle(self.cal(deg))
        time.sleep(0.5)


# just for testing servo with slider
# One slider control all servos cuz I don't know how to make 2 sliders together SAD!
from tkinter import *


pins = [37, 38] # put the pins in here BASED ON THE BOARD

bam = [] # TO store the servoControl classes for the pins

# JUST REALIZED
# This only goes from 0-100... not 0 - 180 bruh mmt 
# wait... fixed it with simple algebra by scaling 100 to 180 mmt

for i in pins:
    bam.append(servoControl(i))

def sel():
    for i in bam:
        a = int(var.get())/100*180 # debugging purposes
        print(a)
        selection = "Angle = " + str(a)
        i.angle(int(a))

    label.config(text = selection)

root = Tk()
var = DoubleVar()
scale = Scale( root, variable = var )
scale.pack(anchor = CENTER)

button = Button(root, text = "Enter", command = sel)
button.pack(anchor = CENTER)

label = Label(root)
label.pack()

root.mainloop()



