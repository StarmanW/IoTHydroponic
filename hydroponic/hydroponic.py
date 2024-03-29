import time
import serial
import os
import json
from servo import Servo
from firebase import Firebase
from timer import Timer
from grove_rgb_lcd import *
from grovepi import *

class Hydroponic():
    def __init__(self, config, firebase):
        self.config = config
        self.firebase = firebase
        self.data = {}

        self.led = 3
        pinMode(self.led, "OUTPUT")

        # Set solutions and food amount
        self.acidAmount = self.config["acidAmount"]
        self.alkaliAmount = self.config["alkaliAmount"]
        self.foodAmount = self.config["foodAmount"]

        # Set rate for solutions and food
        self.acidRate = self.config["acidRate"]
        self.alkaliRate = self.config["alkaliRate"]
        self.foodRate = self.config["foodRate"]

        # Setup servos
        self.pHServo = Servo(self.config["pHServoPin"])
        self.feederServo = Servo(self.config["feederServoPin"])
        self.feederInterval = self.config["feederInterval"]

        # Setup board
        self.ser = serial.Serial(
            self.config["acmNumber"], self.config['baudrate'])
        self.ser.baudrate = self.config['baudrate']

    def run(self):
        timer = Timer()
        while True:
            try:
                self.pHSensor()
                if (self.foodAmount < 0):
                    self.blinkLed()
                if (self.checkTimerOver(timer) and self.foodAmount > 0):
                    timer.resetInterval()
                    self.feeder()
                self.pushDataToFirebase()
            except KeyboardInterrupt:
                print("Terminating hydroponic farm {}...".format(
                    self.config["id"]))
                print("Cleaning up GPIO...")
                self.cleanup()
                break

    def feeder(self):
        try:
            self.feederServo.rotateRight()
            time.sleep(0.5)
            self.feederServo.rotateCenter()
            time.sleep(0.5)

            # Update food amount
            self.foodAmount = self.foodAmount - self.foodRate
            self.data["feeder"] = {
                "status": "Active",
                "amount": self.foodAmount
            }
        except Exception:
            print("Something went wrong with the fish feeder module.")
    
    def pHSensor(self):
            try:
                prevPHValue = 0.0
                acidStatus = "Inactive"
                alkaliStatus = "Inactive"

                read_serial = self.ser.readline()
                pHValue = float(read_serial.decode().strip())
                print("{}. PH Value = {}".format(self.config["id"], pHValue))
                setRGB(0, 128, 64)
                setRGB(0, 255, 0)
                setText("Farm {}\npH: {}".format(self.config["id"], pHValue))
                
                if (pHValue > 0.0 and pHValue < 14.0):
                    if (pHValue <= 6.0):
                        self.pHServo.rotateLeft()
                        self.acidAmount = self.acidAmount - self.acidRate
                        acidStatus = "Active"
                    elif (pHValue >= 8.0):
                        self.pHServo.rotateRight()
                        self.alkaliAmount = self.alkaliAmount - self.alkaliRate
                        alkaliStatus = "Active"

                    prevPHValue = pHValue
                    time.sleep(0.5)

                    # Reset servo to center
                    self.pHServo.rotateCenter()
                    time.sleep(0.5)

                    self.data["pH"] = {
                        "pHValue": pHValue,
                        "acidAmount": self.acidAmount,
                        "alkaliAmount": self.alkaliAmount,
                        "acidStatus": acidStatus,
                        "alkaliStatus": alkaliStatus
                    }
                else:
                    self.data["pH"] = {
                        "pHValue": prevPHValue,
                        "acidAmount": self.acidAmount,
                        "alkaliAmount": self.alkaliAmount,
                        "acidStatus": acidStatus,
                        "alkaliStatus": alkaliStatus
                    }
            except Exception:
                print("Something went wrong with the pH sensor module.")

    def pushDataToFirebase(self):
        defaultFeederData = {
            "status": "Inactive",
            "amount": self.foodAmount
        }
        
        self.firebase.pushData({
            "pH": self.data["pH"],
            "feeder": self.data["feeder"] if "feeder" in self.data else defaultFeederData,
            "timestamp": round(time.time() * 1000)
        })
        self.data.clear()

    def checkTimerOver(self, timer):
        return timer.getSecondsDiff() == self.feederInterval or timer.getSecondsDiff() > self.feederInterval

    def blinkLed(self):
        digitalWrite(self.led, 1)
        time.sleep(1)       
        digitalWrite(self.led, 0)
        time.sleep(1)

    def cleanup(self):
        self.pHServo.rotateCenter()
        self.feederServo.rotateCenter()
        self.pHServo.cleanupGPIO()
        self.feederServo.cleanupGPIO()
