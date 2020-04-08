import serial
import keyboard
import math
import time
import struct

JUMP_THRESHOLD = 18
STAND_THREASHOLD = 4
STAND_TIME = 0.2

ready = False
lastJump = -RELEASE_TIME
jumpStarted = None
MIN_JUMP_TIME = 0.1

def process(t,x,y,z):
    global lastJump, jumpStarted
    a = math.sqrt(x*x+y*y+z*z)
    if a > JUMP_THRESHOLD and ready:
        if jumpStarted is not None and jumpStarted + MIN_JUMP_TIME <= t:
            print("jump",a)
            keyboard.press_and_release("space")
            lastJump = t
            jumpStarted = None
        elif jumpStarted is None:
            print("start")
            jumpStarted = t
    else:
        if jumpStarted:
            print("reset",t-jumpStarted)
        jumpStarted = None
"""    
    
    if a > JUMP_THRESHOLD and ready and lastJump + RELEASE_TIME <= t:
            print("jump",a,t-lastJump,x,y,z)
            keyboard.press_and_release("space")
            lastJump = t
            ready = True # todo?
    if a < FALL_THRESHOLD and  lastJump + 0.1 <= t:
        print("fall",a,t-lastJump)
        lastJump = -RELEASE_TIME
        ready = True
    #print(ts,x,y,z)
"""
pos = 0    
    
with serial.Serial('COM28', 57600, timeout=5) as ser:
    while True:
        b = ser.read(1)
        if b == b'S':
            pos = 1
        elif b == b'e' and pos == 1:
            pos = 2
        elif b == b'n' and pos == 2:
            pos = 3
        elif b == b's' and pos == 3:
            data = ser.read(8+4*3)
            t,x,y,z=struct.unpack(">qfff",data)
            process(t/1000000000., x,y,z)
            pos = 0
        else:
            pos = 0