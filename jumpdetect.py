import serial
import keyboard
import math
import time

JUMP_THRESHOLD = 18
FALL_THRESHOLD = 2
RELEASE_TIME = 0.5
FALL_TIME = 0.2

ready = True
lastJump = -RELEASE_TIME

def process(x,y,z):
    global ready, lastJump
    t = time.time()
    a = math.sqrt(x*x+y*y+z*z)
    if a > JUMP_THRESHOLD and ready and lastJump + RELEASE_TIME <= t:
            print("jump",a)
            keyboard.press_and_release("space")
            lastJump = t
            ready = True # todo?
    if a < FALL_THRESHOLD and  lastJump + 0.1 <= t:
        print("fall",a)
        lastJump = -RELEASE_TIME
        ready = True
    #print(ts,x,y,z)

with serial.Serial('COM28', 57600, timeout=5) as ser:
    while True:
        line = ser.readline().decode()   # read a '\n' terminated line
        if line and line[0]=='>':
            try:
                data = map(float,line.strip().split(",")[2:5])
                process(*data)
            except:
                pass
