import serial
import keyboard
import math
import time
import struct

JUMP_THRESHOLD = 18
STAND_THRESHOLD = 2
GRAVITY = 9.8
STAND_TIME = 0.05

startedStanding = None
stood = False

def process(t,x,y,z):
    global stood, startedStanding
    a = math.sqrt(x*x+y*y+z*z)
    # print(t,a)
    if a >= JUMP_THRESHOLD and stood:
        print("jump",a)
        keyboard.press_and_release("space")
        stood = False
    elif not stood:
        if abs(a-GRAVITY) <= STAND_THRESHOLD:
            if startedStanding is None:
                startedStanding = t
            elif t >= startedStanding + STAND_TIME:
                stood = True
                print("stood",a,t-startedStanding)
        else:
            startedStanding = None
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

init = False
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
            if not init:
                print("First data point",t,x,y,z)
                init = True
            process(t/1000000000., x,y,z)
                
            pos = 0
        else:
            pos = 0
            