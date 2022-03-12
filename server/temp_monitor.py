import os
import time

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        print(temp)
        return (temp.replace("temp=",""))