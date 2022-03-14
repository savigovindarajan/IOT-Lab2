
from camera import camera_stream
from time import sleep
import socket

from temp_monitor import measure_temp



HOST = "192.168.86.206" # IP address of your Raspberry PI
PORT = 65432  

from concurrent.futures import thread
import threading
from lib.motor import Motor
from lib.pwm import PWM
from lib.pin import Pin
import json
import traceback
import time

fwd_speed = 30
bwd_speed = 15
turn_speed = 10
distance = 0

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
        global distance
        print("in drive")
        if data == b"F":
            print("forward")
            forward(fwd_speed)
            time.sleep(0.1)
            stop()
            distance += 1
        elif data == b"D":
            print("backward")
            backward(bwd_speed)
            time.sleep(0.1)
            stop()
            distance += 1
        elif data == b"L":
            print("left")
            turn_left(turn_speed)
            time.sleep(0.1)
            stop()
            distance += 1
        elif data == b"R":
            print("right")
            turn_right(turn_speed)
            time.sleep(0.1)
            stop()
            distance += 1
        elif data == b"S":
            print("stop")
            stop()
            time.sleep(0.1)
def destroy():
    print("Interrupted")

        # Port to listen on (non-privileged ports are > 1023)
def main():
    global distance
    # camera_thread = threading.Thread(target=camera_stream, args=(HOST,9000, ))
    # camera_thread.daemon = True
    # camera_thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        client, clientInfo = s.accept()
        print("server recv from: ", clientInfo)

        background_thread = threading.Thread(target=receive_and_drive, args=(client, ))
        background_thread.daemon = True
        background_thread.start()

        try:
            while 1: 
                time.sleep(2)
                data = {}
                data['temp'] = measure_temp() 
                data['distance'] = distance
                data['speed'] = fwd_speed
                jsonString  = json.dumps(data)
                client.sendall(jsonString.encode('utf-8')) # Echo back to client
                
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print("Closing socket")
        finally: 
            client.close()
            s.close()   

def receive_and_drive(client):
    while 1:
        print("in loop")
        data = client.recv(1024)      # receive 1024 Bytes of message in binary format
        print(data)
        if data != b"":
            drive(data) 

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()


