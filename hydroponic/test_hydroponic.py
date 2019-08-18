import time
import serial
import os
import json
from datetime import datetime
from servo import Servo
from firebase import Firebase
from timer import Timer

# Servo pin declaration
feed_servo = Servo(18)
pH_servo = Servo(22)

# Change ACM number as found from "ls /dev/tty/ACM*"
ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600

# Setup firebase
# Build file path
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(CURRENT_FOLDER, 'firebase.json')
firebase = Firebase(config_file)
firebase.run()

'''
    Function to perform fish
    feeding at an interval
'''
def fishFeeder():
    try:
        global feed_servo
        feed_servo.rotateRight()
        time.sleep(1)
        feed_servo.rotateCenter()
        time.sleep(1)
    except Exception:
        print("Something went wrong with the fish feeder module.")


def pHSensor():
    try:
        global pH_servo

        read_serial = ser.readline()
        pHValue = float(read_serial.decode().strip())
        print(str(pHValue))

        if (pHValue > 0.0 and pHValue < 14.0):
            if (pHValue <= 6.0):
                # Turn servo to left
                pH_servo.rotateLeft()
            elif (pHValue >= 8.0):
                # Turn servo to right
                pH_servo.rotateRight()

            time.sleep(1)

            # Reset servo to center
            pH_servo.rotateCenter()
            time.sleep(1)

            firebase.pushData({
                "pHValue": 6.25,
                "timestamp": json.dumps(datetime.datetime.now(), default=str)
            })
    except Exception:
        print("Something went wrong with the pH sensor module.")


if __name__ == '__main__':
    timer = Timer()
    while True:
        try:
            pHSensor()
            if (timer.getSecondsDiff() == 10):
                timer.resetInterval()
                fishFeeder()
        except KeyboardInterrupt:
            print("CTRL-C: Terminating program.")
            print("Cleaning up GPIO...")
            pH_servo.rotateCenter()
            feed_servo.rotateCenter()
            time.sleep(1)
            Servo.cleanupGPIO()
            break
