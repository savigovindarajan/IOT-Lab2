
import socket

HOST = "192.168.1.36" # IP address of your Raspberry PI
PORT = 65432  
from pickle import FALSE
from random import randrange
import time
from lib.motor import Motor
from lib.servo import Servo
from lib.ultrasonic import Ultrasonic 
from lib.pwm import PWM
from lib.pin import Pin
#import picar
speed = 0
direction = ""
fwd_speed = 30
bwd_speed = 15
turn_speed = 10
ultrasonic_servo_offset = 0 

ANGLE_RANGE = 180
STEP = 18
us_step = STEP
angle_distance = [0,0]
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
scan_list = []

# Init Ultrasonic
us = Ultrasonic(Pin('D8'), Pin('D9'))

# Init Servo
servo = Servo(PWM("P0"), offset=ultrasonic_servo_offset)

# Init motors
left_front = Motor(PWM("P13"), Pin("D4"), is_reversed=False) # motor 1
right_front = Motor(PWM("P12"), Pin("D5"), is_reversed=False) # motor 2
left_rear = Motor(PWM("P8"), Pin("D11"), is_reversed=False) # motor 3
right_rear = Motor(PWM("P9"), Pin("D15"), is_reversed=False) # motor 4

########################################################
# Motors
def forward(power):
    left_front.set_power(power)
    left_rear.set_power(power)
    right_front.set_power(power)
    right_rear.set_power(power)

def backward(power):
    left_front.set_power(-power)
    left_rear.set_power(-power)
    right_front.set_power(-power)
    right_rear.set_power(-power)

def turn_left(power):
    left_front.set_power(-power)
    left_rear.set_power(-power)
    right_front.set_power(power)
    right_rear.set_power(power)

def turn_right(power):
    left_front.set_power(power)
    left_rear.set_power(power)
    right_front.set_power(-power)
    right_rear.set_power(-power)

def stop():
    left_front.set_power(0)
    left_rear.set_power(0)
    right_front.set_power(0)
    right_rear.set_power(0)

def set_motor_power(motor, power):
    if motor == 1:
        left_front.set_power(power)
    elif motor == 2:
        right_front.set_power(power)
    elif motor == 3:
        left_rear.set_power(power)
    elif motor == 4:
        right_rear.set_power(power)

def drive(data):
        print("in drive")
        if data == b"F":
            print("forward")
            forward(fwd_speed)
        elif data == b"D":
            print("backward")
            backward(bwd_speed)
        elif data == b"L":
            print("left")
            turn_left(turn_speed)
        elif data == b"R":
            print("right")
            turn_right(turn_speed)
        elif data == b"S":
            print("stop")
            forward(0)

        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            print(data)
            if data != b"":
                drive(data)                
                client.sendall(data) # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()    

