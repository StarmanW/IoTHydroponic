import time
import serial
import os
import json
from datetime import datetime
from servo import Servo
from firebase import Firebase
from timer import Timer

# Data Structure
data = {}

acidAmount = 1000
alkaliAmount = 1000
foodAmount = 2000

# Servo pin declaration
feed_servo = Servo(22)
pH_servo = Servo(18)

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
        global feed_servo, foodAmount
        feed_servo.rotateRight()
        time.sleep(0.5)
        feed_servo.rotateCenter()
        time.sleep(0.5)
        
        # Update food amount
        foodAmount = foodAmount - 10
        data["feeder"] = {
            "status": "Activated",
            "amount": foodAmount
        }
    except Exception:
        print("Something went wrong with the fish feeder module.")


def pHSensor():
    try:
        global pH_servo, data, acidAmount, alkaliAmount

        read_serial = ser.readline()
        pHValue = float(read_serial.decode().strip())
        print(str(pHValue))

        if (pHValue > 0.0 and pHValue < 14.0):
            if (pHValue <= 6.0):
                pH_servo.rotateLeft()
                acidAmount = acidAmount - 3 
            elif (pHValue >= 8.0):
                pH_servo.rotateRight()
                alkaliAmount = acidAmount - 3
                
            time.sleep(0.5)

            # Reset servo to center
            pH_servo.rotateCenter()
            time.sleep(0.5)
        
            data["pH"] = {
                "pHValue": pHValue,
                "acidAmount": acidAmount, 
                "alkaliAmount": alkaliAmount
            }
    except Exception as ex:
        print(ex);
        print("Something went wrong with the pH sensor module.")

def pushDataToFirebase():
    global data
    firebase.pushData({
        "pH": data["pH"],
        "feeder": data["feeder"] if "feeder" in data else "",
        "timestamp": json.dumps(datetime.now(), default=str)
    })
    data.clear()
    
if __name__ == '__main__':
    timer = Timer()
    while True:
        try:
            pHSensor()
            if (timer.getSecondsDiff() == 10 or timer.getSecondsDiff() > 10):
                timer.resetInterval()
                fishFeeder()
            pushDataToFirebase()
        except KeyboardInterrupt:
            print("CTRL-C: Terminating program.")
            print("Cleaning up GPIO...")
            pH_servo.rotateCenter()
            feed_servo.rotateCenter()
            time.sleep(1)
            Servo.cleanupGPIO()
            break
